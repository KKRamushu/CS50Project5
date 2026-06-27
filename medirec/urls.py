from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login_form", views.username_form, name="username_form"),
    path("sign up", views.registration_form, name="registration_form"),
    path('password request', views.password_form, name='password_form'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('myProfile/', views.my_profile, name='my_profile'),
    path('allPatients/', views.all_patients, name='all_patients'),
    path('myPatients/',views.my_patients, name='my_patients'),
    path('logout', views.sign_out, name='logout'),
    path('patient sign up', views.add_patient, name='add_patient'),
    path('remove_patient/<int:patient_id>', views.remove_patient, name='remove_patient'), 
    path('register patient', views.register_patient, name="register_patient"),
    path('view_patient/<int:patient_id>', views.view_patient_file, name="view_file"),
    path('patient_info/<int:patient_id>',views.patient_info, name="patient_info"),
    path('visits/<int:patient_id>', views.visits, name="visits"),
    path('visit/<int:patient_id>', views.visit, name='visit'),
    path('save visit/<int:patient_id>', views.save_visit, name='save_visit'),
    path('remove_visit/<int:visit_id>', views.remove_visit, name='remove_visit'),
    path('viewVisit/<int:visit_id>', views.view_visit, name="view_visit"),
    ]