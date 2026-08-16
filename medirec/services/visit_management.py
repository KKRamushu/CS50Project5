from django.shortcuts import redirect, get_object_or_404
from ..models import Doctor, Patient_Visit
from django.contrib import messages
from ..forms import VisitForm, VitalsForm
from ..models import Doctor, Patient
import json
from django.http import JsonResponse, HttpResponse, Http404


#
#create visit object
def create_visit(request,patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id) 
    #get data from forms and create visit and vitals models
    if request.method == "POST":
        
        visit_form = VisitForm(request.POST)
        vitals_form = VitalsForm(request.POST)

        if visit_form.is_valid() and vitals_form.is_valid():

            doctor = get_object_or_404(Doctor,user=request.user)
            visit = visit_form.save(commit=False)
            visit.patient = patient
            visit.doctor = doctor
            visit.save()

            vitals = vitals_form.save(commit=False)
            vitals.visit = visit
            vitals.save()

            messages.success(request,"Patient visit recorded successfully!!")
            return redirect("view_file", patient.user.id)
        return redirect('visit',patient_id=patient.patient_id)
    
    return redirect('visit',patient_id=patient.patient_id)

#get patient visits

def get_patient_visits(patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id)
    return patient.visits.all()

#Get new visit detail value, save it and return the saved value to display on field

def edit_visit(request,visitId):

    visit = get_object_or_404(Patient_Visit,id=visitId)
    data = json.loads(request.body)

    field = data['field']
    value = data['value']

    vitals_fields = {'bp','pulse','temp','height','weight'}
    if field in vitals_fields:
        setattr(visit.vitals,field,value)
        visit.vitals.save()
        new_value = getattr(visit.vitals, field)
        return JsonResponse(new_value, safe=False)
    
    setattr(visit,field,value)
    visit.save()
    new_value = getattr(visit, field)
    return JsonResponse(new_value, safe=False)

def visit_details(visit_id):
    
    visit = get_object_or_404(Patient_Visit,id=visit_id)
    return  visit.vitals

#Delete visit
def delete_visit(request, visit_id):

    visit = get_object_or_404(Patient_Visit,id=visit_id)
    doctor = request.user.doctor_profile
    
    if visit.doctor == doctor:
        visit.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=404)
