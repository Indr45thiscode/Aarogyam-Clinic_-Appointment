from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment, Doctor
from patients.models import Patient
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json

@login_required
def analytics(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    pending_count = Appointment.objects.filter(status='pending').count()
    confirmed_count = Appointment.objects.filter(status='confirmed').count()
    completed_count = Appointment.objects.filter(status='completed').count()
    cancelled_count = Appointment.objects.filter(status='cancelled').count()

    status_data = {
        'labels': ['Pending', 'Confirmed', 'Completed', 'Cancelled'],
        'data': [pending_count, confirmed_count, completed_count, cancelled_count],
        'colors': ['#f59e0b', '#10b981', '#6366f1', '#ef4444']
    }

    top_doctors = Doctor.objects.annotate(
        apt_count=Count('appointment')
    ).order_by('-apt_count')[:5]

    monthly_data = Appointment.objects.annotate(
        month=TruncMonth('appointment_date')
    ).values('month').annotate(count=Count('id')).order_by('month')[:6]

    months = [m['month'].strftime('%b %Y') if m['month'] else '' for m in monthly_data]
    month_counts = [m['count'] for m in monthly_data]

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'status_data': json.dumps(status_data),
        'top_doctors': top_doctors,
        'months': json.dumps(months),
        'month_counts': json.dumps(month_counts),
    }
    return render(request, 'analytics/analytics.html', context)

@login_required
def reports(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    appointments = Appointment.objects.all().order_by('-appointment_date')

    total_doctors = doctors.count()
    total_patients = patients.count()
    total_appointments = appointments.count()
    pending_count = appointments.filter(status='pending').count()
    confirmed_count = appointments.filter(status='confirmed').count()
    completed_count = appointments.filter(status='completed').count()
    cancelled_count = appointments.filter(status='cancelled').count()

    context = {
        'doctors': doctors,
        'patients': patients,
        'appointments': appointments,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'analytics/reports.html', context)