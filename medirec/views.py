from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from .forms import SignUpForm, UsernameForm, LoginForm, PatientForm, VisitForm, VitalsForm
from .models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.contrib import messages
from .utils import create_OTP, verify_OTP
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .services import user_auth, user_reg

def index(request):
    allPatients = User.objects.all()
    if request.user.is_authenticated:
        return render(request, "medirec/dashboard.html", {'patients':allPatients})
    return render(request, "medirec/index.html")

#View current user's profile
@login_required

def my_profile(request):

    doctor_profile = get_object_or_404(Doctor,user=request.user)
    return JsonResponse([doctor_profile.serialize()], safe=False)

#view all patients
@login_required

def all_patients(request):

    allPatients = Patient.objects.all()
    return JsonResponse([patient.serialize() for patient in allPatients], safe=False)

#view current doctor's patients
def my_patients(request):

    doctor = get_object_or_404(Doctor,user=request.user)
    myPatients = Patient.objects.filter(visits__doctor=doctor).distinct()
    return JsonResponse([patient.serialize() for patient in myPatients], safe=False)

@login_required

def sign_out(request):
    logout(request)
    return redirect('index')

def username_form(request):
    #open login form    
    form = UsernameForm()
    return render(request, "medirec/login.html",{'form':form, 'username':''})

def password_form(request):
    #check username existance and request password for user
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        login_form = LoginForm()
        if form.is_valid():
            user = user_auth.user_identifyer(form)
        return render(request, "medirec/login.html",{'login_form':login_form, 'user':user, 'username':user.username})      

    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def login_view(request):

    return user_auth.authenticate_user(request)
   
def registration_form(request):
    #open registration form
    form = SignUpForm()
    return render(request,"medirec/register.html", {'form':form})

def register(request):
    #get data from form and save it to database
    if request.method == 'POST':

        form = SignUpForm(request.POST)
        return user_reg.register_patient(form)
        
    return redirect('registration_form')

#present form to register a patient
@login_required

def add_patient(request):
    
    form = PatientForm()
    return render(request, "medirec/dashboard.html",{'form':form})

#Register patient
@login_required

def register_patient(request):
    #get patient details from form and create a user, patient, and patient file
    if request.method == 'POST':

        form = PatientForm(request.POST)
        return user_reg.register_patient(request, form)
    
    return redirect('add_patient')
#View patient information
@login_required

def view_patient_file(request, patient_id):

    patient_file = get_object_or_404(Patient_file,patient__user__id = patient_id)
    patient = get_object_or_404(Patient,user__id=patient_id)
    return render(request, "medirec/dashboard.html",{"patient":patient, "patient_file":patient_file, 'vitals_form':VitalsForm, 'visit_form': VisitForm })

#Remove Patient from system
@login_required

def remove_patient(request, patient_id):
    patient = get_object_or_404(Patient,patient_id=patient_id)
    patient.user.delete()
    return redirect('index')

#view patient information
@login_required

def patient_info(request, patient_id):
    patient = get_object_or_404(Patient,patient_id=patient_id)
    return JsonResponse(patient.serialize())

# open Patient Visit List
@login_required

def visits(request, patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id)
    visits = patient.visits.all()
    return JsonResponse({'visits':[visit.serialize() for visit in visits], 'currentUser': request.user.serialize()}, safe=False)

# Open visit form
@login_required

def visit(request, patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id)   
    return render(request, "medirec/dashboard.html",{'patient':patient,'new_visit':True, 'vitals_form':VitalsForm(), 'visit_form': VisitForm() })

# Save patient visit
@login_required

def save_visit(request, patient_id):

    patient = get_object_or_404(Patient,patient_id=patient_id) 

    #get data from forms and create visit and vitals models
    if request.method == "POST":
        visit_form = VisitForm(request.POST)
        vitals_form = VitalsForm(request.POST)

        if visit_form.is_valid() and vitals_form.is_valid():
            print("forms valid", request.user)
            visit = visit_form.save(commit=False)
            visit.patient = patient
            visit.doctor = get_object_or_404(Doctor,user=request.user)
            visit.save()

            vitals = vitals_form.save(commit=False)
            vitals.visit = visit
            vitals.save()
            print("visit saved")
            messages.success(request,"Patient visit recorded successfully!!")
            return redirect("view_file", patient.user.id)
        else:
            return render(request, "medirec/dashboard.html",{'patient':patient,'visit':True, 'vitals_form':VitalsForm(), 'visit_form': VisitForm() })
    else:
        return render(request, "medirec/dashboard.html",{'patient':patient,'visit':True, 'vitals_form':VitalsForm(), 'visit_form': VisitForm() })

#remove visit from list
@login_required

def remove_visit(request, visit_id):

    visit = get_object_or_404(Patient_Visit,id=visit_id)
    visit.delete()
    return HttpResponse(status=204)

#Open and view visit details
@login_required

def view_visit(request, visit_id):

    visit = get_object_or_404(Patient_Visit,id=visit_id)
    vitals = visit.vitals
    user_is_visit_doctor = (request.user == visit.doctor.user)
    print(vitals.serialize())
    return JsonResponse({"vitals":vitals.serialize(),"user_is_visit_doctor": user_is_visit_doctor})

#change value of a specific visit detail and return new value
@csrf_exempt
@login_required

def edit_visit_detail(request, visitId):

    visit = Patient_Visit.objects.get(id=visitId)
    data = json.loads(request.body)
    field = data['field']
    value = data['value']

    vitals_fields = {'bp','pulse','temp','height','weight'}
    if field in vitals_fields:
        setattr(visit.vitals,field,value)
        visit.vitals.save()
        new_value = getattr(visit.vitals, field)
        return JsonResponse(new_value, safe=False)
    else:
        setattr(visit,field,value)
        visit.save()
        new_value = getattr(visit, field)
        return JsonResponse(new_value, safe=False)

#make changes to patient personal infomation details
@csrf_exempt
@login_required

def edit_patient_info(request,patientId):

    data = json.loads(request.body)
    patient = get_object_or_404(Patient,user__id=patientId)
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