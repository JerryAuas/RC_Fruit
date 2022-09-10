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
    print("get data to send", data_send)
    ret = 0
    ser = serial.Serial(port=portx, baudrate=bps, timeout=timeout)  # 打开串口
    # 判断是否打开成功
    if ser.is_open:
        ser.write(data_send.encode("utf-8"))
        print(f"sended position code：{data_send}")
    while True:
        if ser.in_waiting:
            get_data = ser.read(ser.in_waiting)
            if get_data == b'\x01':  # 退出标志
                ret = 1
                break
    print("Chassic on position")
    ser.close()  # 关闭串口
    time.sleep(0.1)

    return ret
    