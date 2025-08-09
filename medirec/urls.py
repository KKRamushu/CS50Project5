from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_form", views.username_form, name="username_form"),
    path("sign up", views.registration_form, name="registration_form"),
    path('Login', views.password_form, name='password_form'),
    path('dashboard', views.login, name='login'),
    ]