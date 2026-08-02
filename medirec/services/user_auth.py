from django.shortcuts import render, redirect, get_object_or_404
from ..forms import SignUpForm, UsernameForm, LoginForm, PatientForm, VisitForm, VitalsForm
from ..models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from ..utils import create_OTP, verify_OTP
from django.http import JsonResponse, HttpResponse, Http404
from django.core.cache import cache

#Identify user type and provide the appropriate login method
def user_identifyer(form):

    identification = form.cleaned_data['user_identification']
    identification = identification.upper()
    
    try:
        user = User.objects.get(Q(username__iexact=identification)|Q(email__iexact=identification))
    except User.DoesNotExist:
        raise Http404("User not found")
    
    if user.user_type == 'patient':

        otp = create_OTP(user.username)
        print(f"the login OTP for {user.username}: {otp}")

    return user

def authenticate_user(request):

    if request.method == 'POST':
        #Get credentials, choose method to authenticate user and redirect to dashboard
        form = LoginForm(request.POST)
        if form.is_valid():

            username = request.POST['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(username=username)
            except:
                return redirect('username_form')
            
            if user.user_type != 'doctor':
                return otp_login(request, user, password)
            else:
                return password_login(request, username, password)
            
        else:
            return redirect('username_form')
        
    else:
        return redirect('username_form')
        
#OTP login

def otp_login(request, user, password):

    if verify_OTP(user.username, password):
        login(request, user)
        cache.delete(user.username)
        return redirect("index")
    else:
        cache.delete(user.username)
        return redirect('username_form')    

#Password_login

def password_login(request, username, password):

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("index")
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})
