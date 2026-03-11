from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Doctor, Appointment, TIME_SLOTS, Prescription, Medicine
from patients.models import Patient
import datetime


def public_home(request):
    doctors = Doctor.objects.all()
    success = False
    error = None

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        doctor_id = request.POST.get('doctor', '').strip()
        preferred_date = request.POST.get('preferred_date', '').strip()
        time_slot = request.POST.get('time_slot', '').strip()

        if not patient_name or not phone or not doctor_id or not preferred_date or not time_slot:
            error = 'All fields are required!'
        elif len(phone) != 10 or not phone.isdigit():
            error = 'Enter a valid 10-digit mobile number!'
        else:
            existing = Appointment.objects.filter(
                doctor_id=doctor_id,
                appointment_date=preferred_date,
                time_slot=time_slot
            ).exists()

            if existing:
                error = 'This time slot is already booked! Please select another time.'
            else:
                patient, created = Patient.objects.get_or_create(
                    phone=phone,
                    defaults={
                        'first_name': patient_name.split()[0],
                        'last_name': ' '.join(patient_name.split()[1:]) if len(patient_name.split()) > 1 else 'N/A',
                        'age': 0,
                        'gender': 'O',
                        'address': 'Not provided',
                        'email': f'{phone}@aarogyam.com',
                    }
                )
                Appointment.objects.create(
                    patient=patient,
                    doctor_id=doctor_id,
                    appointment_date=preferred_date,
                    time_slot=time_slot,
                    status='pending',
                    patient_name=patient_name,
                    patient_phone=phone,
                    notes='Booked via website'
                )
                success = True

    context = {
        'doctors': doctors,
        'success': success,
        'error': error,
        'time_slots': TIME_SLOTS,
        'today': datetime.date.today().isoformat(),
    }
    return render(request, 'public/home.html', context)


@login_required
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('first_name')
    return render(request, 'doctors/list.html', {'doctors': doctors})

@login_required
def doctor_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        bio = request.POST.get('bio', '')
        experience_years = request.POST.get('experience_years', 0)

        if Doctor.objects.filter(email=email).exists():
            messages.error(request, 'A doctor with this email already exists!')
            return render(request, 'doctors/add.html', {'form_data': request.POST})

        Doctor.objects.create(
            first_name=first_name, last_name=last_name,
            specialization=specialization, phone=phone,
            email=email, bio=bio, experience_years=experience_years
        )
        messages.success(request, f'Dr. {first_name} {last_name} added successfully!')
        return redirect('doctor_list')
    return render(request, 'doctors/add.html')

@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.first_name = request.POST.get('first_name')
        doctor.last_name = request.POST.get('last_name')
        doctor.specialization = request.POST.get('specialization')
        doctor.phone = request.POST.get('phone')
        doctor.email = request.POST.get('email')
        doctor.bio = request.POST.get('bio', '')
        doctor.experience_years = request.POST.get('experience_years', 0)
        doctor.save()
        messages.success(request, f'Dr. {doctor.first_name} {doctor.last_name} updated!')
        return redirect('doctor_list')
    return render(request, 'doctors/edit.html', {'doctor': doctor})

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = str(doctor)
        doctor.delete()
        messages.success(request, f'{name} deleted!')
        return redirect('doctor_list')
    return render(request, 'doctors/delete_confirm.html', {'doctor': doctor})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-created_at')
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def appointment_add(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        time_slot = request.POST.get('time_slot')
        notes = request.POST.get('notes')

        existing = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot
        ).exists()

        if existing:
            messages.error(request, 'This time slot is already booked!')
            return render(request, 'appointments/add.html', {
                'doctors': doctors, 'patients': patients, 'time_slots': TIME_SLOTS
            })

        Appointment.objects.create(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot,
            notes=notes
        )
        messages.success(request, 'Appointment booked successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/add.html', {
        'doctors': doctors, 'patients': patients, 'time_slots': TIME_SLOTS
    })

@login_required
def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.status = request.POST.get('status')
        appointment.save()
        messages.success(request, 'Status updated!')
        return redirect('appointment_list')
    return render(request, 'appointments/update_status.html', {'appointment': appointment})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted!')
        return redirect('appointment_list')
    return render(request, 'appointments/delete_confirm.html', {'appointment': appointment})


def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')

    if not doctor_id or not date:
        return JsonResponse({'slots': [s[0] for s in TIME_SLOTS]})

    booked_slots = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=date
    ).values_list('time_slot', flat=True)

    available = [
        {'value': slot[0], 'label': slot[1], 'booked': slot[0] in booked_slots}
        for slot in TIME_SLOTS
    ]
    return JsonResponse({'slots': available})


@login_required
def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    prescription = None
    try:
        prescription = appointment.prescription
    except Prescription.DoesNotExist:
        pass

    if request.method == 'POST':
        doctor_notes = request.POST.get('doctor_notes', '').strip()
        next_visit   = request.POST.get('next_visit_date', '') or None
        diagnosis    = request.POST.get('diagnosis', '').strip()

        if prescription:
            prescription.doctor_notes    = doctor_notes
            prescription.next_visit_date = next_visit
            prescription.diagnosis       = diagnosis
            prescription.save()
            prescription.medicines.all().delete()
        else:
            prescription = Prescription.objects.create(
                appointment=appointment,
                doctor_notes=doctor_notes,
                next_visit_date=next_visit,
                diagnosis=diagnosis,
            )

        med_names     = request.POST.getlist('medicine_name[]')
        med_dosages   = request.POST.getlist('medicine_dosage[]')
        med_durations = request.POST.getlist('medicine_duration[]')
        med_instrs    = request.POST.getlist('medicine_instructions[]')
        print(f"DEBUG med_names: {med_names}")
        print(f"DEBUG POST: {dict(request.POST)}")

        for i, name in enumerate(med_names):
            name = name.strip()
            if not name:
                continue
            Medicine.objects.create(
                prescription=prescription,
                name=name,
                dosage=med_dosages[i].strip()     if i < len(med_dosages)   else '',
                duration=med_durations[i].strip() if i < len(med_durations) else '',
                instructions=med_instrs[i].strip() if i < len(med_instrs)  else '',
            )

        appointment.status = 'completed'
        appointment.save()
        messages.success(request, f'Prescription saved for {appointment.patient.first_name} {appointment.patient.last_name}!')
        return redirect('appointment_list')

    return render(request, 'appointments/add_prescription.html', {
        'appointment':  appointment,
        'prescription': prescription,
        'medicines':    prescription.medicines.all() if prescription else [],
        'today':        timezone.now().date(),
    })


@login_required
def view_prescription(request, appointment_id):
    appointment  = get_object_or_404(Appointment, id=appointment_id)
    prescription = get_object_or_404(Prescription, appointment=appointment)
    return render(request, 'appointments/view_prescription.html', {
        'appointment':  appointment,
        'prescription': prescription,
        'medicines':    prescription.medicines.all(),
    })


@login_required
def prescription_pdf(request, appointment_id):
    appointment  = get_object_or_404(Appointment, id=appointment_id)
    prescription = get_object_or_404(Prescription, appointment=appointment)
    medicines    = list(prescription.medicines.all())

    print(f"DEBUG medicines count: {len(medicines)}")
    for m in medicines:
        print(f"  - {m.name} | {m.dosage} | {m.duration}")

    return render(request, 'appointments/prescription_pdf.html', {
        'appointment':  appointment,
        'prescription': prescription,
        'medicines':    medicines,
        'pdf_mode':     False,
    })