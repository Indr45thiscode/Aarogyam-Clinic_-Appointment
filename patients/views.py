from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/list.html', {'patients': patients})

@login_required
def patient_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        medical_history = request.POST.get('medical_history')

        if Patient.objects.filter(email=email).exists():
            messages.error(request, 'Ya email ne patient already exist ahe!')
            return render(request, 'patients/add.html', {'form_data': request.POST})

        Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            medical_history=medical_history
        )
        messages.success(request, f'{first_name} {last_name} added successfully!')
        return redirect('patient_list')

    return render(request, 'patients/add.html')

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email')
        patient.address = request.POST.get('address')
        patient.medical_history = request.POST.get('medical_history')
        patient.save()
        messages.success(request, f'{patient.first_name} {patient.last_name} updated!')
        return redirect('patient_list')
    return render(request, 'patients/edit.html', {'patient': patient})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = str(patient)
        patient.delete()
        messages.success(request, f'{name} deleted!')
        return redirect('patient_list')
    return render(request, 'patients/delete_confirm.html', {'patient': patient})