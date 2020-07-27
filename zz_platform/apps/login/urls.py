from django.urls import re_path
from login import views

urlpatterns = [
    re_path("login", views.login),
    re_path("register", views.register),
    re_path("show", views.show)

]