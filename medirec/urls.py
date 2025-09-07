from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login_form", views.username_form, name="username_form"),
    path("sign up", views.registration_form, name="registration_form"),
    path('password request', views.password_form, name='password_form'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('Dashboard', views.dashboard, name='dashboard'),
    path('logout', views.sign_out, name='logout'),
    path('patient sign up', views.add_patient, name='add_patient')
    ]