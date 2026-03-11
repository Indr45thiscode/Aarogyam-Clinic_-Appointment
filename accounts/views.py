from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import datetime

def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')

        # Check if locked
        if user_obj.is_locked():
            remaining = user_obj.locked_until - timezone.now()
            mins = int(remaining.total_seconds() // 60) + 1
            messages.error(request, f'Account locked. Try again in {mins} minute(s).')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Reset failed attempts
            user.failed_login_attempts = 0
            user.locked_until = None
            user.save()

            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)  # Browser close = logout
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            return redirect_by_role(user)
        else:
            # Increment failed attempts
            user_obj.failed_login_attempts += 1
            max_attempts = getattr(settings, 'LOGIN_MAX_ATTEMPTS', 5)
            lockout_minutes = getattr(settings, 'LOGIN_LOCKOUT_MINUTES', 15)

            if user_obj.failed_login_attempts >= max_attempts:
                user_obj.locked_until = timezone.now() + timedelta(minutes=lockout_minutes)
                user_obj.failed_login_attempts = 0
                user_obj.save()
                messages.error(request, f'Too many failed attempts. Account locked for {lockout_minutes} minutes.')
            else:
                remaining = max_attempts - user_obj.failed_login_attempts
                user_obj.save()
                messages.error(request, f'Invalid password. {remaining} attempt(s) remaining.')

    return render(request, 'accounts/login.html')


def redirect_by_role(user):
    if user.role == 'admin':
        return redirect('/dashboard/')
    elif user.role == 'staff':
        return redirect('/dashboard/')
    elif user.role == 'patient':
        return redirect('/patient-dashboard/')
    return redirect('/dashboard/')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied!')
        return redirect('/dashboard/')
    return render(request, 'accounts/patient_dashboard.html', {'user': request.user})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

            send_mail(
                subject='Clinic Dashboard - Password Reset',
                message=f'Hi {user.username},\n\nPassword reset link:\n{reset_link}\n\nLink 24 tasant expire hoil.\n\nClinic Dashboard Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link tumchya email var pathavla ahe!')
        except User.DoesNotExist:
            messages.error(request, 'Ya email ne konta account nahi!')

    return render(request, 'accounts/forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'Passwords match nahi zale!')
            elif len(password1) < 8:
                messages.error(request, 'Password minimum 8 characters pahije!')
            else:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password successfully changed! Login kara.')
                return redirect('/login/')
        return render(request, 'accounts/reset_password.html', {'valid': True})
    else:
        return render(request, 'accounts/reset_password.html', {'valid': False})