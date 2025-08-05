from django.shortcuts import render
from .forms import SignUpForm


# Create your views here.
def index(request):
    return render(request, "medirec/index.html")

def loginForm(request):
    #open login form    
    return render(request, "medirec/login.html")
    
def register(request):
    #open registration form
    form = SignUpForm()
    return render(request,"medirec/register.html", {'form':form})