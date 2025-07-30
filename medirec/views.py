from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "medirec/index.html")

def loginForm(request):
    #open login form    
    return render(request, "medirec/login.html")
    