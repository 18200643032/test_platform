from django.shortcuts import render

from django.http import StreamingHttpResponse  #文件处理
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
import json,os
import shutil


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILE_DIR = os.path.join(BASE_DIR, "download_file")
UPLOAD_DIR = os.path.join(BASE_DIR,"upload_file")
DOCER_DIR = os.path.join(BASE_DIR,"docker")

@require_http_methods(["POST"])
def guifan(request):
    response = {}

    images = request.POST.get("images")  #<QueryDict: {'name': ['123']}>
    if len(images.split(' ')) > 1:
        response["msg"] = "镜像名有误"
        return JsonResponse(response)
    if not os.system(f"docker pull {images}"):
        response["list"] = images
    else:
        response["list"] = "镜像名不存在"
    #生成容器，挂载规范目录
    images_name = images.split(":")[0].split("/")[-1]
    if os.path.exists(os.path.join(DOCER_DIR,images_name)):
        pass
    else:
        os.makedirs(os.path.join(DOCER_DIR,images_name))
    #移动zip包导挂载目录
    shutil.copy(os.path.join(DOCER_DIR,'guifan.zip'),os.path.join(DOCER_DIR,images_name))
    os.system(f"unzip {os.path.join(os.path.join(DOCER_DIR,images_name),'guifan.zip')} -d {os.path.join(DOCER_DIR,images_name)}")
    docker_run_cmd = f"docker run -itd --runtime=nvidia --privileged -v /dockerdata/AppData:/data -v {os.path.join(DOCER_DIR,images_name)}:/zhengzhong  -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=all {images} >>{os.path.join(BASE_DIR,'tmp/docker_id.txt')}"
    os.system(docker_run_cmd)
    #运行容器
    with open(os.path.join(BASE_DIR,"tmp/docker_id.txt"), 'r') as f:
        docker_id = f.readlines()[-1][0:6]
    response["docker_id"] = docker_id
    os.system("docker exec -it %s python3 /zhengzhong/auto_run.py" % (docker_id))
    response["msg"] = "算法规范已完成，请去查看结果"
    response["res_jpg"] = os.path.join(os.path.join(DOCER_DIR,images_name),'res_jpg')
    response["dynamiv_res"] = os.path.join(os.path.join(DOCER_DIR, images_name), 'dynamiv_res')
    response["project_res"] = os.path.join(os.path.join(DOCER_DIR, images_name), 'project_res.txt')
    os.system(f"tar zcvf {os.path.join(BASE_DIR,'res.tar.gz')} {os.path.join(os.path.join(DOCER_DIR,images_name),'res_jpg')} {os.path.join(os.path.join(DOCER_DIR, images_name), 'dynamiv_res')} {os.path.join(os.path.join(DOCER_DIR, images_name), 'project_res.txt')}")
    response["res_path"] = os.path.join(BASE_DIR,'res.tar.gz')
    return  JsonResponse(response)

#下载文件
@require_http_methods(["GET"])
def file_download(request):
    res = {}
    try:
        filename = request.GET.get('file')
        filepath = os.path.join(BASE_DIR, filename)
        fp = open(filepath, 'rb')
        response = StreamingHttpResponse(fp)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename
        res["code"] = 200
        res["msg"] = "下载成功"
        return response
        # return
    except Exception as e:
        res["code"] = 203
        res["msg"] = str(e)
        return JsonResponse(res)
def send_file(fullfilename):
    store_path = fullfilename
    with open(store_path, 'rb') as targetfile:
        while 1:
            data = targetfile.read(20 * 1024 )  # 每次读取20M
            if not data:
                break
            yield data
#复制文件到本地
@require_http_methods(["GET"])
def scp_file(request):
    res = {}
    old_filename = request.GET.get("old_path")
    new_filename = request.GET.get("new_path")




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
