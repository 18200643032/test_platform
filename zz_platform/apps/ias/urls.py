from django.urls import re_path
from ias import views

urlpatterns = [
    re_path("ias", views.ias),
    re_path("get_files_result",views.get_files_result)
]