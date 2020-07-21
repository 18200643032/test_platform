from django.shortcuts import render
from .models import User
# Create your views here.
from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
from django.http import FileResponse

@require_http_methods(["POST"])
def login():
    response = {}
    username = 1



#注册
@require_http_methods(["POST"])
def register(request):
    response = {}
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    return JsonResponse(response)
