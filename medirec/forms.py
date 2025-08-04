from django import forms
from .models import Doctor, User

#Doctor signup Form that creates a User and a Doctor portfolio
class SignUpForm(forms.Form):
    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=64)
    specialization = forms.CharField(max_length=64)

    class mata:
        model = User
        fields = ["name","surname","specialization","username","emailaddress","password1","password2"]
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


