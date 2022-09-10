import serial
import time


portx = "/dev/CH340"  # 所提供的环境中已为所需用到的串口设置了别名
bps = 115200
timeout = None


def serial_communicate(data_send):
    """
    :param data_send: 待发送的数据
    :return: 底盘完成指令标志位
    """
    print("geted data to send", data_send)
    ret = 0
    ser = serial.Serial(port=portx, baudrate=bps, timeout=timeout)  # 打开串口
    # 判断是否打开成功
    if ser.is_open:
        ser.write(data_send.encode("utf-8"))
        print("sended position code：", data_send)
    while True:
        if ser.in_waiting:
            get_data = ser.read(ser.in_waiting)
            if get_data == b'\x01':  # 退出标志
                ret = 1
                break
    print("on position: ", get_data)
    ser.close()  # 关闭串口
    time.sleep(0.1)

    return ret
    
    
# # 底盘单步运行测试 
while True: 
    print("0：底盘重置") 
    print("1-7：交叉点 8：泊车区") 
    print("a：左转") 
    print("d：右转") 
    print("w：前进到下一交叉点") 
    print("s：后退到上一交叉点")
    print("q：退出调试") 
    data_send = input("输入指令:") 
    if data_send == "q": 
        break 
    data_get = serial_communicate(data_send) 
    if data_get == b'\x01': 
        print("Command Completed", data_get, "\n")

