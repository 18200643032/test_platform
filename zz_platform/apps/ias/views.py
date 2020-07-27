from django.shortcuts import render

# Create your views here.

from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON


@require_http_methods(["POST"])
def ias(request):
    images = request.POST.get("images")
    port = request.POST.get("port")
