from django.contrib.auth.models import AbstractUser
from django.db import models

#User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (('doctor','doctor'), ('patient','patient'),)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=64, blank=True)
    surname = models.CharField(max_length=64, blank=True)

#Doctor Profile
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=64, blank=True)

#Patient profile
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")

#Medical record file
class Patient_file(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
