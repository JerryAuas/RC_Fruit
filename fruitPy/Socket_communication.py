import time
from socket import *


def socket_communicate(data):
    """
    :param data: 客户端发送给反解服务器的数据
    :return: 服务器发回的反解数据
    """
    # address为发送端创建的同一个文件
    ADDR = '/home/jetson/dofbot_ws/src/dofbot_moveit/src/server.sock'
    clientfd = socket(AF_UNIX, SOCK_STREAM)
    # 连接到该套接字
    clientfd.connect(ADDR)
    time.sleep(.5)

    # 发送预处理，浮点数转字符串，空格隔开
    msg_send = " ".join(list(map(str, data)))
    msg_send = msg_send + " "
    print(f"\nsending object pos data : {msg_send}\n")
    if not msg_send:
        return 0
    clientfd.send(msg_send.encode())

    # 接收
    msg_recv = clientfd.recv(1024)
    print(f"\nservo data received: {msg_recv.decode()}\n")
    ch = msg_recv.decode()

    # 接收后处理
    data_ik = []
    num_temp = ""
    for c in ch:
        if c == " ":            # 空格时，将b中存储的数字附到浮点数组a的末尾，并将b清空
            data_ik.append(float(num_temp))
            num_temp = ""
        else:                   # 非空格时，b按位累计接收到的字符
            num_temp += c

    clientfd.close()
    return data_ik


if __name__ == '__main__':
    input("确认打开服务器后按回车运行\n>>>")
    num = [-4.5, 14.7, 27.1, -90.0, 0.0, 0.0]
    socket_communicate(num)
