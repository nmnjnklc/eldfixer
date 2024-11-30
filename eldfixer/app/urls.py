from django.urls import path
from . import views


urlpatterns = [
    path("", views.fixer_redirect, name="fixer_redirect"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path("fixer/", views.fixer, name="fixer"),
    path("malfunctionletters/", views.malfunctionletters, name="malfunctionletters"),
]
