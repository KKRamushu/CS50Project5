from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, User, Patient_file, Patient

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
    
#Patient and File creation form
class PatientForm(UserCreationForm):
    patient_id = forms.CharField(max_length=13, label="", widget=forms.TextInput(attrs={"class": "input", "placeholder": "Patient ID"}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "input"}))
    contact = forms.CharField(max_length=10, label="", widget=forms.TextInput(attrs={"class": "input", "placeholder": "Contact number"}))
    address = forms.CharField(label="", widget= forms.Textarea(attrs={"class": "input", "placeholder": "Address", "rows": 3}))
    gender = forms.ChoiceField(label="", choices=[('male','male'),('female','female'),('other','other')], widget=forms.Select(attrs={"class": "input"}))
    bloode_type = forms.ChoiceField(label="", choices=[('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','0-')], 
                                            widget=forms.Select(attrs={"class": "input"}))
    allergies = forms.CharField(required=False, label="", widget=forms.Textarea(attrs={"class": "input", "placeholder": "Allergies (optional)", "rows": 3}))
    
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]
        widgets = {
            'last_name' : forms.TextInput(attrs={'class':'input','placeholder':'Last Name'}),
            'first_name' : forms.TextInput(attrs={'class':'input','placeholder':'First Name'}),
            'email' : forms.EmailInput(attrs={'class':'input','placeholder':'Email Address'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password1", None)
        self.fields.pop("password2", None)
        for field_name in self.fields:
            self.fields[field_name].label = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = 'patient'

        if commit:
            user.save()
            patient = Patient.objects.create(
                user = user,
                patient_id = self.cleaned_data['patient_id'],
                date_of_birth = self.cleaned_data['date_of_birth'],
                contact = self.cleaned_data['contact'],
                address = self.cleaned_data['address'],
                gender = self.cleaned_data['gender'],
                blood_type = self.cleaned_data['blood_type'],
                allergies = self.cleaned_data['allergies']
            )

            Patient_file.objects.create(
                patient = patient
            )
            return user

#Username collection form
class UsernameForm(forms.Form):
    user_identification = forms.CharField(max_length=64, label="" , widget=forms.TextInput(attrs={'class':'input', 'placeholder':'username/email/ID number'}))

class LoginForm(forms.Form):
    password = forms.CharField(
    label="",
    widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter password'}))
