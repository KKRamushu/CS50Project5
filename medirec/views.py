from django.shortcuts import render
from django.core.cache import cache
from .forms import SignUpForm, UsernameForm, LoginForm
from .models import User, Doctor, Patient, Patient_file
from .utils import create_OTP, verify_OTP
from django.contrib.auth import get_user_model
from django.db.models import Q

def index(request):
    return render(request, "medirec/index.html")

def username_form(request):
    #open login form    
    form = UsernameForm()
    return render(request, "medirec/login.html",{'form':form, 'username':''})

def user_identifyer(identification):
    try:
        user = User.objects.get(Q(username=identification)|
                                Q(email=identification)|
                                Q(id=identification))
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
            user = {'username':user_id, 'user_type':'patient'} #user_identifyer(user_id)
            if user['user_type'] is 'patient':
                otp = create_OTP(user['username'])
                print(f"the login OTP for {user['username']}: {otp}")
            return render(request, "medirec/login.html",{'login_form':login_form, 'user':user, 'username':user['username']})      
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = form.cleaned_data['password']
            if verify_OTP(username, password):
                user = {'username':username, 'password': password}
                cache.delete(username)
                return render(request, "medirec/dashboard.html",{'user':user})
            else:
                cache.delete(username)
                return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})
    
        else:
            return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})
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