import socket
import struct
import cv2
import pickle
import time
from time import ctime


print("客户端\n")

IP = input("请输入服务器IP地址:")
port = int(input("请输入服务器端口号:"))
print("连接中...")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建TCP套接字
client_socket.connect((IP, port)) # 设置要连接的服务器IP地址和端口

print("连接成功!")

cap = cv2.VideoCapture(0)

sumv = 0
i = 0
avv = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]# 图片进行压缩的参数
while cap.isOpened():
    t1 = time.time()
    ret, frame = cap.read()
    if not ret:
        continue
    result,frame_encode = cv2.imencode('.jpg', frame, encode_param) # 将图片进行压缩
    frame_bytes = pickle.dumps(frame_encode, 0) # 将图片转化成bytes字节对象
    size1 = len(frame_bytes) # 获取图片字节的长度
    size = struct.pack('L', size1) # 将长度进行编码
    client_socket.sendall(size + frame_bytes) # 将图片长度和图片发送给服务器
    t2 = time.time()

    t = t2 - t1
    if(t!=0):
        v = size1 / t
        v = v / 1000000

        if(i < 2):
            sumv += v
            i += 1
        if(i == 2):
            avv = sumv / 2.0
            i = 0
            sumv = 0
            av  ='%.2f' % (avv)
            s = "V-Rate:" + str(av) + "MB/s"
            print(s)

        
        
                

                
