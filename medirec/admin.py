from django.contrib import admin
from .models import User, Doctor, Patient, Patient_file, Patient_Visit, Patient_Vitals

# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Patient_file)
admin.site.register(Patient_Visit)
admin.site.register(Patient_Vitals)