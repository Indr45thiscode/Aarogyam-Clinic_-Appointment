from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from appointments.models import Doctor, Appointment
from functools import wraps
from django.shortcuts import redirect

def admin_or_staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if request.user.role == 'patient':
            return redirect('/patient-dashboard/')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_or_staff_required
def dashboard(request):
    context = {
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
        'pending_count': Appointment.objects.filter(status='pending').count(),
        'recent_appointments': Appointment.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)