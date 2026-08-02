from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.contrib import messages

def register_doctor(form):
    
    if form.is_valid():
        form.save()
        
        return redirect('username_form')
    else:
        print(form.errors)

def register_patient(request, form):

    if form.is_valid():
        form.save()
        messages.success(request,"Patient registered successfully!!")
        patient = get_object_or_404(Patient,patient_id=form.cleaned_data['patient_id'])
        return render(request, "medirec/dashboard.html",{"patient":patient} )
    else:
        print(form.errors)
        return redirect('add_patient')