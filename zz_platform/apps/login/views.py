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
@require_http_methods(["GET"])
def register(request):
    response = {}
    # r = User()
    # r.name = "a910386943"
    # r.password = "123456"
    # r.sex = "男"
    # r.email = "910386943@qq.com"
    # r.save()
    # username = request.POST.get("username")
    # password = request.POST.get("password")
    # email = request.POST.get("email")

    return HttpResponse("sourss")


# @require_http_methods(["GET"])
def show(request):
    try:
        users = User.objects.filter(name="a910386943")
        print(users)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"code":405})