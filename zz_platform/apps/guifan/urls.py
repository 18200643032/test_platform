from django.urls import re_path
from guifan import views

urlpatterns = [
    re_path("guifan", views.guifan),
    re_path("download", views.file_download),
    re_path("upload", views.file_upload),
    re_path("opencv",views.opencv),
    re_path("test_image",views.img_test)

]