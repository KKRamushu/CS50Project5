from django.contrib.auth.models import AbstractUser
from django.db import models

#User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (('doctor','doctor'), ('patient','patient'),)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='doctor')
    #name = models.CharField(max_length=64, blank=True)
    #surname = models.CharField(max_length=64, blank=True)

#Doctor Profile
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name[:1].upper() if self.user.first_name else ""} {self.user.last_name}"

#Patient profile
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    patient_id = models.CharField(max_length=14,unique=True, null=True)
    date_of_birth = models.DateField(null=True)
    contact = models.CharField(max_length=11, null=True)
    address = models.TextField(null=True)
    GENDER_CHOICES = (('male','male'),('female','female'),('other','other'))
    gender = models.CharField(max_length=8,choices=GENDER_CHOICES, null=True)
    BLOOD_TYPE_CHOICES = (('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'))
    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPE_CHOICES, null=True)
    allergies = models.TextField(blank=True, null=True)

#Cosultation Record 
class Patient_Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_visits")
    visit_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

#Patient Vitals for every visit
class Patient_Vitals(models.Model):
    visit = models.OneToOneField(Patient_Visit, on_delete=models.CASCADE, related_name="vitals")
    blood_pressure = models.CharField(max_length=10, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    heart_rate = models.PositiveIntegerField(blank=True, null=True)

#Medical record file
class Patient_file(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
