from django.shortcuts import render, redirect
from django.core.cache import cache
from .forms import SignUpForm, UsernameForm, LoginForm
from .models import User, Doctor, Patient, Patient_file
from .utils import create_OTP, verify_OTP
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q

def index(request):
    return render(request, "medirec/index.html")

def dashboard(request):
    return render(request, "medirec/dashboard.html")

def sign_out(request):
    logout(request)
    return redirect('index')

def username_form(request):
    #open login form    
    form = UsernameForm()
    return render(request, "medirec/login.html",{'form':form, 'username':''})

def user_identifyer(identification):
    try:
        user = User.objects.get(Q(username=identification)|
                                Q(email=identification))
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
                otp = create_OTP(user['username'])
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
        return redirect("login",{'user':user})
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
        if form.is_valid:
            user = form.save()
        else:
            return redirect('"registration_form')
        
    return redirect('"registration_form')