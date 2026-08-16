from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from ..forms import SignUpForm, UsernameForm, LoginForm, PatientForm, VisitForm, VitalsForm
import json

def register_doctor(form):
    
    if form.is_valid():
        form.save()
        
        return redirect('username_form')
    else:
        print(form.errors)

def patient_form(request):

    current_doctor = request.user.doctor_profile
    return PatientForm(doctor=current_doctor)

def register_patient(request):

    current_doctor = request.user.doctor_profile
    form = PatientForm(request.POST, doctor=current_doctor)
    if form.is_valid():
        form.save()
        messages.success(request,"Patient registered successfully!!")
        patient = get_object_or_404(Patient,patient_id=form.cleaned_data['patient_id'])
        return render(request, "medirec/dashboard.html",{"patient":patient} )
    else:
        print(form.errors)
        return redirect('add_patient')

#get current user's profile
def get_user_profile(request):

    current_user = request.user

    if current_user.user_type == "doctor":
        return get_object_or_404(Doctor,user=current_user)
    return get_object_or_404(Patient,user=current_user)    

def edit_patient_details(request, patientId):

    data = json.loads(request.body)
    patient = get_object_or_404(Patient,patient_id=patientId)
    user = patient.user

    user_fields = {'first_name','last_name','email'}
    patient_fields = {'patient_id','date_of_birth','contact','address','gender','blood_type','allergies'}

    for field in user_fields:
        setattr(user,field,data[field])

    for field in patient_fields:
        setattr(patient,field,data[field])

    user.save()
    patient.save()

    return JsonResponse({'message': 'Patient ifno updated successfully!'})

def delete_patient(request,patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id)
    if request.user.doctor_profile == patient.file.doctor:
        patient.user.delete()
    return redirect('index')