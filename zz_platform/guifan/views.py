from django.shortcuts import render

from guifan.models import GuiFan
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
import json


@require_http_methods(["POST"])
def guifan(request):
    response = {}
    print(request.POST)  #<QueryDict: {'name': ['123']}>
    return  JsonResponse(response)