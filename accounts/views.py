import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from .forms import SignupForm
from .models import User


def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # -------------------------
            # Password
            # -------------------------

            user.set_password(
                form.cleaned_data['password']
            )

            # -------------------------
            # Location
            # -------------------------

            user.latitude = request.POST.get(
                'latitude'
            )

            user.longitude = request.POST.get(
                'longitude'
            )

            user.location_type = request.POST.get(
                'location_type'
            )

            user.location_address = request.POST.get(
                'location_address'
            )

            # -------------------------
            # Email OTP
            # -------------------------

            otp = str(
                random.randint(100000, 999999)
            )

            user.otp = otp

            user.otp_created_at = timezone.now()

            user.email_verified = False

            user.save()

            # -------------------------
            # Send OTP
            # -------------------------

            send_mail(

                'Safety System - Email Verification',

                f'''
Hello {user.username},

Your Safety & Emergency System
verification OTP is:

{otp}

Please enter this OTP to verify
your email address.

Do not share this OTP with anyone.
''',

                None,

                [user.email],

                fail_silently=False
            )

            # Store user ID temporarily
            request.session[
                'verification_user_id'
            ] = user.id

            messages.success(
                request,
                'OTP has been sent to your email.'
            )

            return redirect(
                'verify_email'
            )

    else:

        form = SignupForm()

    return render(
        request,
        'accounts/signup.html',
        {
            'form': form
        }
    )


def verify_email(request):

    user_id = request.session.get(
        'verification_user_id'
    )

    if not user_id:

        messages.error(
            request,
            'Verification session expired.'
        )

        return redirect('signup')

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        messages.error(
            request,
            'User does not exist.'
        )

        return redirect('signup')

    if request.method == 'POST':

        entered_otp = request.POST.get(
            'otp'
        )

        if entered_otp == user.otp:

            user.email_verified = True

            user.otp = None

            user.otp_created_at = None

            user.save()

            # Remove session value
            request.session.pop(
                'verification_user_id',
                None
            )

            messages.success(
                request,
                'Email verified successfully!'
            )

            return redirect('login')

        else:

            messages.error(
                request,
                'Invalid OTP. Please try again.'
            )

    return render(
        request,
        'accounts/verify_email.html'
    )



from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.email_verified:
                messages.error(
                    request,
                    'Please verify your email before logging in.'
                )

                request.session['verification_user_id'] = user.id

                return redirect('verify_email')

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('profile')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'accounts/login.html'
    )


@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )


@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return render(
                request,
                'accounts/login.html'
            )

        # Email verification check
        if not user.email_verified:

            messages.error(
                request,
                'Please verify your email first.'
            )

            request.session['verification_user_id'] = user.id

            return redirect('verify_email')

        # Login user
        login(request, user)

        messages.success(
            request,
            'Login successful!'
        )

        # Role-based redirect

        if user.role == 'SUPERADMIN':

            return redirect('superadmin_dashboard')

        elif user.role == 'ADMIN':

            return redirect('admin_dashboard')

        else:

            return redirect('user_dashboard')

    return render(
        request,
        'accounts/login.html'
    )

@login_required
def user_dashboard(request):

    if request.user.role != 'USER':

        messages.error(
            request,
            'You are not authorized to access this dashboard.'
        )

        return redirect('role_dashboard')

    return render(
        request,
        'accounts/user_dashboard.html'
    )

@login_required
def admin_dashboard(request):

    if request.user.role != 'ADMIN':

        messages.error(
            request,
            'You are not authorized to access this dashboard.'
        )

        return redirect('role_dashboard')

    return render(
        request,
        'accounts/admin_dashboard.html'
    )

@login_required
def superadmin_dashboard(request):

    if request.user.role != 'SUPERADMIN':

        messages.error(
            request,
            'You are not authorized to access this dashboard.'
        )

        return redirect('role_dashboard')

    return render(
        request,
        'accounts/superadmin_dashboard.html'
    )

@login_required
def role_dashboard(request):

    if request.user.role == 'SUPERADMIN':

        return redirect('superadmin_dashboard')

    elif request.user.role == 'ADMIN':

        return redirect('admin_dashboard')

    else:

        return redirect('user_dashboard')

@login_required
def profile(request):

    return render(
        request,
        'accounts/profile.html'
    )

@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')


def home(request):

    return render(
        request,
        'home.html')