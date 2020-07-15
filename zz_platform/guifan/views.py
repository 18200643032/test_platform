from django.shortcuts import render

from django.http import HttpResponse,StreamingHttpResponse
from guifan.models import GuiFan
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
import json,os
from django.http import FileResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_DIR = os.path.join(BASE_DIR, "download_file")
UPLOAD_DIR = os.path.join(BASE_DIR,"upload_file")

@require_http_methods(["POST"])
def guifan(request):
    response = {}

    images = request.POST.get("images")  #<QueryDict: {'name': ['123']}>
    if len(images.split(' ')) > 1:
        response["msg"] = "镜像名有误"
        return JsonResponse(response)

    # os.system(f"docker pull {images}")


    return  JsonResponse(response)

#下载文件
@require_http_methods(["GET"])
def file_download(request):
    res = {}
    try:
        filename = request.GET.get('file')
        filepath = os.path.join(FILE_DIR, filename)
        fp = open(filepath, 'rb')
        response = StreamingHttpResponse(fp)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename
        res["code"] = 200
        res["msg"] = "下载成功"
        return JsonResponse(res)
    except Exception as e:
        res["code"] = 203
        res["msg"] = str(e)
        return JsonResponse(res)

#上传文件
@require_http_methods(["POST"])
def file_upload(request):
    res = {}
    myfile = request.FILES.get('myfile',None)

    if not myfile:
        res["msg"] = "没有文件上传"
        return JsonResponse(res)
    destination = open(os.path.join(UPLOAD_DIR,myfile.name),"wb+")
    for chunk in myfile.chunks():
        destination.write(chunk)
    destination.close()
    res["code"] = 200
    res["msg"] = "上传成功"
    return JsonResponse(res)

