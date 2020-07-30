import os

a1 = os.popen("ldd /usr/local/ev_sdk/lib/libji.so |grep so.4.1").read()
if a1:
    with open("/zhengzhong/res.txt","w") as f:
        f.write("4.1")
else:
    with open("/zhengzhong/res.txt","w") as f:
        f.write("3.4")
