from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, User

#Doctor signup Form that creates a User and a Doctor portfolio
class SignUpForm(UserCreationForm):

    specialization = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Specialization e.g.(Ganeral Practitionor)'}))

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]
        widgets = {
            'last_name' : forms.TextInput(attrs={'class':'input','placeholder':'Last Name'}),
            'first_name' : forms.TextInput(attrs={'class':'input','placeholder':'First Name'}),
            'username' : forms.TextInput(attrs={'class':'input','placeholder':'Username'}),
            'email' : forms.EmailInput(attrs={'class':'input','placeholder':'Email Address'}),
        }

    #remove labels from form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class':'input','placeholder':'Enter a password'})
        self.fields['password2'].widget.attrs.update({'class':'input','placeholder':'Repeat password'})
        self.fields['password1'].help_text=''
        self.fields['password2'].help_text=''
        self.fields['username'].help_text=''
        for field_name in self.fields:
            self.fields[field_name].label = ""

    #custom save method that creates a User and a portfolio linked to it
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
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
