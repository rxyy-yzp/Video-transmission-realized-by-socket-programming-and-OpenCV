import socket
import struct
import cv2
import pickle
import time


print("服务器\n")

IP = input("请输入要设置的服务器IP地址:")
port = int(input("请输入要设置的服务器端口号:"))
print("服务器正在等待连接...")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建套接字
server_socket.bind((IP, port)) # 设置要连接的服务器IP地址和端口
server_socket.listen(5) # 监听
client_socket, addr = server_socket.accept() # 接受连接请求

print("连接成功!  客户端IP地址:" + str(addr[0]) + "  端口号:" + str(addr[1]))


data = b''# 用于不断接受客户端传输的数据

length = struct.calcsize('L')# 数据长度编码后的长度，比如说用于存放的数据占用几个字节
sumt = 0
i = 0
avv = 0
s = ""

while True:

    t1 = time.time()
    if len(data) < length: # 先接受传输图片的长度
        data += client_socket.recv(4096)
    size = data[:length] # 获取图片的长度字节 
    data = data[length:] # 图片字节数据   
    data_len = struct.unpack('L', size)[0] # 获取图片的长度    
    while len(data) < data_len: # 如果接受的字节长度小于图片长度,进行不断的接受
        data += client_socket.recv(4096)    
    frame = data[:data_len] # 拿出该图片长度的字节数据    
    data = data[data_len:] # 将剩下的数据保存到下一次接受
    frame = pickle.loads(frame, fix_imports=True, encoding='bytes') # 将图片解码为array
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR) # 将图片解压缩

    t2 = time.time()
    t = t2 - t1

    if(i < 10):
        sumt += t
        i += 1
    if(i == 10):
        avv = sumt / 10.0
        i = 0
        sumt = 0
        vtime  ='%.3f' % (t)
        avvtime = '%.3f' % (avv*4)    
        s="Average-Delay:" + str(avvtime) + "s"
        print(s)
    
    
    cv2.putText(frame, s, (0,25), cv2.LINE_AA , 0.8, (205, 0, 0), 2)

    cv2.imshow('IMAGES FROM THE CLIENT', frame) #显示图像
    cv2.waitKey(1)



    
    

