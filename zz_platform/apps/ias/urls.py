from django.urls import re_path
from ias import views

urlpatterns = [
    re_path("ias", views.ias),
]