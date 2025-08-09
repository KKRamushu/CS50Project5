from django.shortcuts import render
from .forms import SignUpForm, UsernameForm, LoginForm



def index(request):
    return render(request, "medirec/index.html")

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
            user_id = form.cleaned_data['user_identification']
            return render(request, "medirec/login.html",{'login_form':login_form, 'username':user_id})      
    else:
        return render(request, "medirec/login.html",{'form':UsernameForm(), 'username':''})

def login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = form.cleaned_data['password']
            user = {'username':username, 'password': password}
            return render(request, "medirec/dashboard.html",{'user':user})
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