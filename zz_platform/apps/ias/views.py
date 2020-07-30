from django.shortcuts import render

# Create your views here.

from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
import subprocess,requests,os
from config.response_codes import RET

from sdk_precision.run import iter_files, clear_dirs
path= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #zz_platform目录
UPLOAD_DIR = os.path.join(path,"tmp")      #临时存放图片目录
@require_http_methods(["POST"])
def ias(request):
    res = {}
    """
    # 封装ias
    :param algo_image:  接收传入的镜像名称:image_name,
    :return:
    """
    res_datas = request.POST
    port = res_datas.get('port')
    image_name = res_datas.get('image_name')

    # 获取到容器id
    cmd_run_sdk = f"docker run -itd  --runtime=nvidia --privileged -v /home/zheng:/home  -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm  -p {port}:80 {image_name}"
    res_p = subprocess.Popen(cmd_run_sdk, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_p.stderr.readline().decode('utf-8') is not '' or res_p.poll() != 0:
        res["errmsg"] = "端口已使用"
        res["error"] =  RET.DATAERR
        return JsonResponse(res)
    else:
        contain_id = res_p.stdout.readline().decode('utf-8')[:8] #容器ID

    data = {
        "images":image_name
    }
    ias_ver = requests.post("http://192.168.1.147:8888/api/opencv/",data=data).json().get("opencv版本")
    if ias_ver == "4.1":
        cmd = f"cp {path}/sdk_package/ias/ias_4.1.tar.gz /home/zheng;tar -xvf /home/zheng/ias_4.1.tar.gz -C /home/zheng"
        res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(res_p.stderr.readline().decode('utf-8'))
        if res_p.stderr.readline().decode('utf-8') is not '' or res_p.poll() != 0:
            res["errno"] = RET.SERVERERR
            res["errmsg"] = "移动文件到挂载目录失败"
            return JsonResponse(res)
    else:
        cmd = f"cp {path}/sdk_package/ias/ias_3.4.tar.gz /home/zheng;tar -xvf /home/zheng/ias_3.4.tar.gz -C /home/zheng"
        res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(res_p.stderr.readline().decode('utf-8'))
        if res_p.stderr.readline().decode('utf-8') is not '' or res_p.poll() != 0:
            res["errno"] = RET.SERVERERR
            res["errmsg"] = "移动文件到挂载目录失败"
            return JsonResponse(res)
    ias_install = f"docker exec  {contain_id} bash /home/give_license.sh &"
    res_p = subprocess.Popen(ias_install, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res["errno"] = RET.OK
    res["errmsg"] = "封装ias成功"
    res["ias的版本是"] = ias_ver

    return JsonResponse(res)




@require_http_methods(["POST"])
def get_files_result(request):
    res = {}
    file = request.FILE.get("file")
    tag_names = request.POST.get('tag_name')
    alert_info = request.POST.get('alert_info')
    port = request.POST.get('port')
    tag_names = tag_names.split(",")
    if not all([tag_names, port]):
        res["error"] = RET.DATAERR
        res["errmsg"] = "传入数据不完整"
        return JsonResponse(res)
    filename = file.name
    if not filename.lower().endswith('zip'):
        res["error"] = RET.DATAERR
        res["errmsg"] = "上传的图片和xml文件请打包zip格式上传"
        return JsonResponse(res)
    ZZ_PLATFORM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    files_dir = os.path.join(ZZ_PLATFORM_DIR, "sdk_precision/input/files").replace("\\", "/")
    file_name = os.path.join(files_dir, filename).replace("\\", "/")
    destination = open(file_name, "wb+")
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    if alert_info is None:
        iter_files(files_dir, port, tag_names)
    else:
        iter_files(files_dir, port, tag_names, alert_info)
    files_dir = os.path.join(ZZ_PLATFORM_DIR, "sdk_precision/main.py")
    cmd = f"python3 {files_dir}"
    res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_p.stderr.readline().decode('utf-8') is not '' or res_p.poll() != 0:
        res["error"] = RET.DATAERR
        res["errmsg"] = "运行脚本失败"
        return JsonResponse(res)
    os.system(cmd)
    clear_dirs()
    file_res = os.path.join(ZZ_PLATFORM_DIR, "sdk_precision/output/output.txt")

    with open(file_res, 'r') as f:
        r = f.read().splitlines()
    res["errno"] = RET.OK
    res["errmsg"] = r

    return JsonResponse(res)

