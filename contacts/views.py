import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone

from .models import EmergencyContact
from .forms import EmergencyContactForm


@login_required
def contacts_list(request):
    contacts = EmergencyContact.objects.filter(
        user=request.user
    )

    return render(
        request,
        'contacts/contacts.html',
        {'contacts': contacts}
    )


@login_required
def add_contact(request):

    if request.method == 'POST':

        form = EmergencyContactForm(request.POST)

        if form.is_valid():

            contact = form.save(commit=False)

            # Assign logged-in user
            contact.user = request.user

            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))

            contact.verification_otp = otp
            contact.otp_created_at = timezone.now()
            contact.email_verified = False

            contact.save()

            # Send OTP to emergency contact email
            send_mail(
                'Safety System - Emergency Contact Verification',

                f'''
Hello {contact.name},

You have been added as an emergency contact
by {request.user.username}.

Your verification OTP is:

{otp}

Please enter this OTP on the
Safety & Emergency System verification page.

Do not share this OTP with anyone.
''',

                None,

                [contact.email],

                fail_silently=False
            )

            messages.success(
                request,
                'Verification OTP has been sent to the contact email.'
            )

            # Send contact ID to verification URL
            return redirect(
                'verify_contact',
                contact_id=contact.id
            )

    else:

        form = EmergencyContactForm()

    return render(
        request,
        'contacts/add_contact.html',
        {'form': form}
    )


@login_required
def verify_contact(request, contact_id):

    # Get only the contact belonging to logged-in user
    contact = get_object_or_404(
        EmergencyContact,
        id=contact_id,
        user=request.user
    )

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        # Compare entered OTP with saved OTP
        if entered_otp == contact.verification_otp:

            contact.email_verified = True

            # Remove OTP after successful verification
            contact.verification_otp = None
            contact.otp_created_at = None

            contact.save()

            messages.success(
                request,
                'Emergency contact email verified successfully.'
            )

            return redirect('contacts_list')

        else:

            messages.error(
                request,
                'Invalid OTP. Please try again.'
            )

    return render(
        request,
        'contacts/verify_contact.html',
        {'contact': contact}
    )


@login_required
def delete_contact(request, contact_id):

    contact = get_object_or_404(
        EmergencyContact,
        id=contact_id,
        user=request.user
    )

    if request.method == 'POST':

        contact.delete()

        messages.success(
            request,
            'Emergency contact deleted successfully.'
        )

        return redirect('contacts_list')

    return render(
        request,
        'contacts/delete_contact.html',
        {'contact': contact}
    )