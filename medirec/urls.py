from django.urls import path

from . import views

urlpatterns = [
    path("Home", views.index, name="index"),
    path("login_form", views.username_form, name="username_form"),
    path("sign up", views.registration_form, name="registration_form"),
    path('', views.password_form, name='password_form'),
    path('login', views.login_view, name='login'),
    path('Dashboard', views.dashboard, name='dashboard'),
    path('logout', views.sign_out, name='logout'),
    ]