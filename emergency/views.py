import math
import secrets

from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import Emergency, EmergencyAlert
from accounts.models import User
from django.db.models import Count
from django.db.models import Count, Q
from django.utils.dateparse import parse_date


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


@login_required
def sos(request, emergency_type='SOS'):

    if request.method == 'POST':

        # -----------------------------------------
        # 1. GET CURRENT GPS LOCATION
        # -----------------------------------------

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not latitude or not longitude:

            messages.error(
                request,
                'Unable to get your current location. Please try again.'
            )

            return redirect('sos')


        # -----------------------------------------
        # 2. CREATE EMERGENCY
        # -----------------------------------------

        emergency = Emergency.objects.create(
            user=request.user,
            emergency_type=emergency_type,
            status='ACTIVE',
            latitude=latitude,
            longitude=longitude
        )


        # -----------------------------------------
        # 3. GOOGLE MAPS LOCATION
        # -----------------------------------------

        maps_link = (
            f"https://www.google.com/maps?q="
            f"{emergency.latitude},{emergency.longitude}"
        )


        # -----------------------------------------
        # 4. EMERGENCY CONTACT ALERTS
        # -----------------------------------------

        contacts = request.user.emergency_contacts.filter(
            email_verified=True
        )


        for contact in contacts:

            alert = EmergencyAlert.objects.create(
                emergency=emergency,
                alert_type='CONTACT',
                recipient_email=contact.email,
                status='PENDING',
                location_shared=True
            )


            send_mail(
                '🚨 SOS Emergency Alert',

                f'''
EMERGENCY ALERT

{request.user.username} has triggered an SOS emergency.

Emergency Type:
SOS

Current Location:

Latitude: {emergency.latitude}
Longitude: {emergency.longitude}

Google Maps:
{maps_link}

Please contact the person immediately.

Safety & Emergency System
''',

                None,

                [contact.email],

                fail_silently=False
            )


            alert.status = 'SENT'
            alert.save()


        # -----------------------------------------
        # 5. FIND NEARBY HELPERS
        # -----------------------------------------
        
# Find nearby registered users

        # 5. FIND NEARBY REGISTERED USERS
        helpers = User.objects.filter(
            is_active=True,
            latitude__isnull=False,
            longitude__isnull=False
        ).exclude(
            id=request.user.id
        ).exclude(
            email=''
        )

        

        for helper in helpers:
            distance = calculate_distance(
                emergency.latitude,
                emergency.longitude,
                helper.latitude,
                helper.longitude
            )

            if distance <= 5 and helper.email:
                # Generate a secure token for this helper
                token = secrets.token_urlsafe(32)

                alert = EmergencyAlert.objects.create(
                    emergency=emergency,
                    alert_type='HELPER',
                    recipient_email=helper.email,
                    status='PENDING',
                    location_shared=False,
                    acceptance_token=token,
                    token_created_at=timezone.now()
                )

                accept_url = request.build_absolute_uri(
                    reverse(
                        'accept_emergency_email',
                        kwargs={'token': token}
                    )
                )

                send_mail(
                    subject='SOS - Nearby Emergency Alert',
                    message=(
                        'A nearby user needs emergency assistance.\n\n'
                        f'Emergency type: {emergency.emergency_type}\n'
                        f'Approximate distance: {distance:.2f} km\n\n'
                        f'Accept emergency: {accept_url}\n\n'
                        'The exact location will be shared after acceptance.'
                    ),
                    from_email=None,
                    recipient_list=[helper.email],
                    fail_silently=False,
                    html_message=f"""
                        <h2>🚨 Nearby Emergency Alert</h2>
                        <p>A nearby user needs emergency assistance.</p>
                        <p><strong>Type:</strong> {emergency.emergency_type}</p>
                        <p><strong>Approximate distance:</strong>
                           {distance:.2f} km</p>
                        <p>
                            <a href="{accept_url}"
                               style="background-color:#15803d;
                               color:white;padding:12px 20px;
                               text-decoration:none;border-radius:6px;
                               display:inline-block;">
                                Accept Emergency
                            </a>
                        </p>
                        <p>The exact location will be shared after acceptance.</p>
                    """
                )

                alert.status = 'SENT'
                alert.save(update_fields=['status'])

        messages.success(
            request,
            'SOS alert has been processed successfully.'
        )

        return redirect(
            'sos_success',
            emergency_id=emergency.id
        )
    
    if emergency_type == 'ACCIDENT':
     return render(request, 'emergency/accident_confirm.html')    

    return render(request, 'emergency/sos_confirm.html')

@login_required
def sos_success(request, emergency_id):

    emergency = get_object_or_404(
        Emergency,
        id=emergency_id,
        user=request.user
    )


    return render(
        request,
        'emergency/sos_success.html',
        {
            'emergency': emergency
        }
    )


@login_required
def resolve_emergency(request, emergency_id):
    emergency = get_object_or_404(
        Emergency,
        id=emergency_id,
        user=request.user
    )

    if request.method == 'POST':
        if emergency.status == 'ACTIVE':
            emergency.status = 'RESOLVED'
            emergency.save(update_fields=['status'])

            messages.success(
                request,
                'Emergency has been marked as resolved.'
            )
        else:
            messages.info(
                request,
                'This emergency has already been resolved.'
            )

        return redirect(
            'sos_success',
            emergency_id=emergency.id
        )

    return redirect(
        'sos_success',
        emergency_id=emergency.id
    )



from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def accept_emergency_email(request, token):
    alert = get_object_or_404(
        EmergencyAlert,
        acceptance_token=token,
        alert_type='HELPER'
    )
    # Check whether the emergency has already been resolved.
    if alert.emergency.status != 'ACTIVE':
     return render(
        request,
        'emergency/accept_email.html',
        {
            'alert': alert,
            'emergency': alert.emergency,
            'maps_link': None,
            'can_accept': False,
            'unavailable_message':
                'This emergency has already been resolved.'
        },
        status=410
    )

    # Acceptance links expire after 30 minutes.
    if (
        not alert.token_created_at
        or (timezone.now() - alert.token_created_at).total_seconds() > 1800
    ):
        return render(
            request,
            'emergency/accept_expired.html',
            status=410
        )

    if request.method == 'POST':
        if alert.status == 'ACCEPTED':
            messages.info(request, 'This emergency was already accepted.')

        elif alert.status != 'SENT':
            messages.error(request, 'This alert is no longer available.')

        elif alert.emergency.status != 'ACTIVE':
            messages.error(request, 'This emergency is no longer active.')

        elif EmergencyAlert.objects.filter(
            emergency=alert.emergency,
            alert_type='HELPER',
            status='ACCEPTED'
        ).exists():
            messages.error(
                request,
                'Another helper has already accepted this emergency.'
            )

        else:
            alert.status = 'ACCEPTED'
            alert.location_shared = True
            alert.save(update_fields=['status', 'location_shared'])
            messages.success(
                request,
                'Emergency accepted. Location access is now enabled.'
            )

    emergency = alert.emergency
    maps_link = None

    if alert.status == 'ACCEPTED' and alert.location_shared:
        maps_link = (
            f'https://www.google.com/maps?q='
            f'{emergency.latitude},{emergency.longitude}'
        )

    return render(
        request,
        'emergency/accept_email.html',
        {
            'alert': alert,
            'emergency': emergency,
            'maps_link': maps_link,
        }
    )


@login_required
def emergency_history(request):

    # Get emergencies belonging to the logged-in user
    emergencies = Emergency.objects.filter(
        user=request.user
    ).prefetch_related(
        'alerts'
    ).order_by('-created_at')

    # Get filter values from the URL
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    status = request.GET.get('status', '')

    # Filter by starting date
    if start_date:
        parsed_start_date = parse_date(start_date)

        if parsed_start_date:
            emergencies = emergencies.filter(
                created_at__date__gte=parsed_start_date
            )

    # Filter by ending date
    if end_date:
        parsed_end_date = parse_date(end_date)

        if parsed_end_date:
            emergencies = emergencies.filter(
                created_at__date__lte=parsed_end_date
            )

    # Filter by emergency status
    if status in ['ACTIVE', 'RESOLVED']:
        emergencies = emergencies.filter(
            status=status
        )

    return render(
        request,
        'emergency/emergency_history.html',
        {
            'emergencies': emergencies,
            'start_date': start_date,
            'end_date': end_date,
            'selected_status': status,
        }
    )

@login_required
def emergency_statistics(request):
    emergencies = Emergency.objects.filter(user=request.user)

    stats = emergencies.aggregate(
        total=Count('id'),
        active=Count('id', filter=Q(status='ACTIVE')),
        resolved=Count('id', filter=Q(status='RESOLVED')),
        sos=Count('id', filter=Q(emergency_type='SOS')),
        accident=Count('id', filter=Q(emergency_type='ACCIDENT')),
    )

    return render(
        request,
        'emergency/emergency_statistics.html',
        {'stats': stats}
    )