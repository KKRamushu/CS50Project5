from ..models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

#get all patients 

def get_all_patients():

    return Patient.objects.all()

#get a patient with user PK

def get_patient(patient_id):

    return get_object_or_404(Patient,user__id=patient_id)

#get all patient of with a common doctor

def get_my_patients(request):

    doctor = get_object_or_404(Doctor,user=request.user)
    return Patient.objects.filter(Q(visits__doctor=doctor)|Q(file__doctor=doctor)).distinct()

#get patient through with patient ID number

def get_patient_info(patient_id):

    return get_object_or_404(Patient,patient_id=patient_id)
