from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_form", views.loginForm, name="login_form"),
    path("register", views.register, name="register"),
    ]