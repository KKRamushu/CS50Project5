from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, UsernameForm, LoginForm, VisitForm, VitalsForm
from .models import Doctor, Patient, Patient_file, Patient_Visit
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import doctor_required
from django.db.models import Q
import json
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .services import user_auth, user_management, visit_management, patient_management


def index(request):

    if request.user.is_authenticated and request.user.user_type == "doctor":

        all_patients = patient_management.get_all_patients()
        return render(request, "medirec/dashboard.html", {'patients':all_patients})
    
    return render(request, "medirec/index.html")

#View current user's profile
@login_required
@doctor_required

def my_profile(request):

    profile = user_management.get_user_profile(request)
    return JsonResponse([profile.serialize()], safe=False)

#view all patients
@login_required
@doctor_required

def all_patients(request):

    all_patients = patient_management.get_all_patients()
    return JsonResponse([patient.serialize() for patient in all_patients], safe=False)

#view current doctor's patients
@login_required
@doctor_required

def my_patients(request):

    myPatients = patient_management.get_my_patients(request)
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

    return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def login_view(request):

    return user_auth.authenticate_user(request)

#call up registration form for doctor

def registration_form(request):

    #open registration form
    form = SignUpForm()
    return render(request,"medirec/register.html", {'form':form})

#create doctor

def register(request):
    #get data from form and save it to database
    if request.method == 'POST':

        form = SignUpForm(request.POST)
        return user_management.register_patient(form)
        
    return redirect('registration_form')

#present form to register a patient
@login_required
@doctor_required

def add_patient(request):

    form = user_management.patient_form(request)
    return render(request, "medirec/dashboard.html",{'form':form})

#Register patient
@login_required
@doctor_required

def register_patient(request):
    #get patient details from form and create a user, patient, and patient file
    if request.method == 'POST':

        return user_management.register_patient(request)
    
    return redirect('add_patient')

#View patient information
@login_required

def view_patient_file(request, patient_id):
    
    patient = patient_management.get_patient(patient_id)
    return render(request, "medirec/dashboard.html",{"patient":patient, 'vitals_form':VitalsForm, 'visit_form': VisitForm })

#Remove Patient from system
@login_required
@doctor_required

def remove_patient(request, patient_id):

   return user_management.delete_patient(request,patient_id) 

#view patient information through API
@login_required

def patient_info(request, patient_id):

    patient = patient_management.get_patient_info(patient_id)
    return JsonResponse(patient.serialize())

# open Patient Visit List
@login_required

def visits(request, patient_id):

    visits = visit_management.get_patient_visits(patient_id)
    return JsonResponse({'visits':[visit.serialize() for visit in visits], 'currentUser': request.user.serialize()}, safe=False)

# Open visit form
@login_required

def visit(request, patient_id):

    patient = patient_management.get_patient_info(patient_id)   
    return render(request, "medirec/dashboard.html",{'patient':patient,'new_visit':True, 'vitals_form':VitalsForm(), 'visit_form': VisitForm() })

# Save patient visit
@login_required

def save_visit(request, patient_id):
    
    return visit_management.create_visit(request,patient_id)

#remove visit from list
@login_required
@doctor_required

def remove_visit(request, visit_id):

    return visit_management.delete_visit(request, visit_id)

#Open and view visit details
@login_required

def view_visit(request, visit_id):

    vitals = visit_management.visit_details(visit_id)
    user_is_visit_doctor = (request.user == vitals.visit.doctor.user)
    return JsonResponse({"vitals":vitals.serialize(),"user_is_visit_doctor": user_is_visit_doctor})

#change value of a specific visit detail and return new value
@csrf_exempt
@login_required

def edit_visit_detail(request, visitId):

    return visit_management.edit_visit(request,visitId)

#make changes to patient personal infomation details
@csrf_exempt
@login_required

def edit_patient_info(request,patientId):

    return  user_management.edit_patient_details(request, patientId)