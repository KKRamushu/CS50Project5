from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, User

#Doctor signup Form that creates a User and a Doctor portfolio
class SignUpForm(UserCreationForm):

    #create custom form fields for doctor sign up
    name = forms.CharField(max_length=64, label="" , widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Name'}))
    surname = forms.CharField(max_length=64, label="" , widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Surname'}))
    specialization = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Specialization e.g.(Ganeral Practitionor)'}))
    password1 = forms.CharField(
    label="",
    widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(
    label="",
    widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm password'}))
    
    #add fielsds to sign up form
    class Meta:
        model = User
        fields = ["name","surname","specialization","username","email","password1","password2"]
        widgets = {
            'username' : forms.TextInput(attrs={'class':'input','placeholder':'Username'}),
            'email' : forms.EmailInput(attrs={'class':'input','placeholder':'Email Address'}),
        }

        #remove labels from form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ""

    #custom save method that creates a User and a portfolio linked to it
    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.user_type = 'doctor'
        if commit:
            user.save()
            Doctor.objects.create(
                user = user,
                specialization = self.cleaned_data['specialization']
            )

        return user

#Username collection form
class UsernameForm(forms.Form):
    user_identification = forms.CharField(max_length=64, label="" , widget=forms.TextInput(attrs={'class':'input', 'placeholder':'username/email/ID number'}))

class LoginForm(forms.Form):
    password = forms.CharField(
    label="",
    widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter password'}))
