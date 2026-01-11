from django.shortcuts import render, redirect
from django.core.cache import cache
from .forms import SignUpForm, UsernameForm, LoginForm, PatientForm, VisitForm, VitalsForm
from .models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.contrib import messages
from .utils import create_OTP, verify_OTP
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q

def index(request):
    if request.user.is_authenticated:
        return(dashboard(request))
    return render(request, "medirec/index.html")

def dashboard(request):
    patients = User.objects.all()
    return render(request, "medirec/dashboard.html", {'patients':patients})

def sign_out(request):
    logout(request)
    return redirect('index')

def username_form(request):
    #open login form    
    form = UsernameForm()
    return render(request, "medirec/login.html",{'form':form, 'username':''})

def user_identifyer(identification):
    identification = identification.upper()
    try:
        user = User.objects.get(Q(username__iexact=identification)|
                                Q(email__iexact=identification))
        return user
    except User.DoesNotExist:
        return None

def password_form(request):
    #check username existance and request password for user
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        login_form = LoginForm()
        if form.is_valid():
            user_id = form.cleaned_data['user_identification']
            user = user_identifyer(user_id)
            if user.user_type == 'patient':
                otp = create_OTP(user.username)
                print(f"the login OTP for {user.username}: {otp}")
            return render(request, "medirec/login.html",{'login_form':login_form, 'user':user, 'username':user.username})      
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def login_view(request):
    if request.method == 'POST':
        #Get credentials, choose method to authenticate user and redirect to dashboard
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.user_type != 'doctor':
                return otp_login(request, user, password)
            else:
                return password_login(request, username, password)
        else:
            return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})
    
#OTP login
def otp_login(request, user, password):
    if verify_OTP(user.username, password):
        login(request, user)
        cache.delete(user.username)
        return redirect("dashboard")
    else:
        return render("medirec/login.html",{'form':password_form(), 'username':user.username, 'error':
                                                     'incorrect OTP entered'})
    
#Password_login
def password_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def registration_form(request):
    #open registration form
    form = SignUpForm()
    return render(request,"medirec/register.html", {'form':form})

def register(request):
    #get data from form and save it to database
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            redirect('username_form')
        else:
            print(form.errors)
        
    return redirect('registration_form')

def add_patient(request):
    form = PatientForm()
    return render(request, "medirec/dashboard.html",{'form':form})

def register_patient(request):
    #get patient details from form and create a user, patient, and patient file
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Patient registered successfully!!")
            return redirect("dashboard")
        else:
            print(form.errors)
        return render(request, "medirec/dashboard.html",{"form":PatientForm()})
    
def view_patient_file(request, patient_id):
    patient_file = Patient_file.objects.get(patient__user__id = patient_id)
    patient = Patient.objects.get(user__id=patient_id)
    return render(request, "medirec/dashboard.html",{"patient":patient, "patient_file":patient_file, 'vitals_form':VitalsForm, 'visit_form': VisitForm })

# open Patient Visit List
def visits(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    visits = patient.visits.all()
    return render(request, "medirec/dashboard.html",{"visits": visits, "patient":patient,'vitals_form':VitalsForm, 'visit_form': VisitForm })

# Open visit form
def visit(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)   
    return render(request, "medirec/dashboard.html",{'patient':patient,'new_visit':True, 'vitals_form':VitalsForm(), 'visit_form': VisitForm() })

# Save patient visit
def save_visit(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id) 

    #get data from forms and create visit and vitals models
    if request.method == "POST":
        visit_form = VisitForm(request.POST)
        vitals_form = VitalsForm(request.POST)

        if visit_form.is_valid() and vitals_form.is_valid():
            print("forms valid", request.user)
            visit = visit_form.save(commit=False)
            visit.patient = patient
            visit.doctor = Doctor.objects.get(user=request.user)
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

def view_visit(request, visit_id):
    visit = Patient_Visit.objects.get(id=visit_id)
    vitals = Patient_Vitals.objects.get(visit=visit)
    patient = visit.patient
    return render(request,  "medirec/dashboard.html",{"visit":visit, "vitals":vitals, "patient":patient})