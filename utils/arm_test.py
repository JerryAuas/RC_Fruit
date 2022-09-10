import time
from Arm_Lib import Arm_Device


# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.01)

left = 180
middle = 90
right = 0

tight = 130  # 夹紧时的6号舵机角度(需比读取到的角度略大3~5°)
loose = 50  # 松开使的6号舵机角度
level_servo_2 = 180  # 待命位调水平时的2号舵机角度
level_servo_3 = 0  # 待命位调水平时的3号舵机角度
level_servo_4 = 0  # 待命位调水平时的4号舵机角度


def read_servo_degree():
    Arm.Arm_serial_set_torque(0)
    print("\n机械臂舵机力矩已关闭，可以掰动\n")
    input("\n当机械臂掰动到位后请输按回车\n")
    Arm.Arm_serial_set_torque(1)
    print("\n机械臂舵机力矩已启动\n")
    time.sleep(.2)
    for i in range(6):
        aa = Arm.Arm_serial_servo_read(i + 1)
        print("第" + str(i + 1) + "号舵机角度为：", aa)
    

def arm_standby(direction):
    Arm.Arm_serial_servo_write6(direction, level_servo_2, level_servo_3, level_servo_4, 90, loose, 800)
    time.sleep(1)


def arm_scout(direction):
    Arm.Arm_serial_servo_write6(direction, 90, 90, 0, 90, loose, 800)
    time.sleep(1)
    
    
def arm_grab(data_ik):
    # 居中待命
    Arm.Arm_serial_servo_write6(90, level_servo_2, level_servo_3, level_servo_4, 90, loose, 800)
    time.sleep(1)
    # 中途防撞
    Arm.Arm_serial_servo_write6(90, 90, 60, 0, 90, loose, 500)
    time.sleep(.5)
    # 张开,前出,预备
    Arm.Arm_serial_servo_write6(data_ik[0], data_ik[1], data_ik[2], data_ik[3]-25, 90, loose, 500)
    time.sleep(1)
    # 张开,前出,到位
    Arm.Arm_serial_servo_write6(data_ik[0], data_ik[1], data_ik[2], data_ik[3], 90, loose, 500)
    time.sleep(1)
    # 抓紧
    Arm.Arm_serial_servo_write6(data_ik[0], data_ik[1], data_ik[2], data_ik[3], 90, tight, 500)
    time.sleep(1)
    # 抓紧，摘下
    Arm.Arm_serial_servo_write6(data_ik[0], data_ik[1], data_ik[2], data_ik[3]-15, 90, tight, 500)
    time.sleep(1)
    # 回中
    Arm.Arm_serial_servo_write6(90, level_servo_2, level_servo_3, level_servo_4, 90, tight, 500)
    time.sleep(1)
    # 回中
    Arm.Arm_serial_servo_write6(90, level_servo_2, level_servo_3, level_servo_4, 90, tight, 500)
    time.sleep(.5)


def put_in_basket(direction):
    # 放球
    Arm.Arm_serial_servo_write6(direction, level_servo_2, level_servo_3, level_servo_4, 90, tight, 500)  # 转向到位
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(direction, 91, 13, 65, 90, tight, 500)  # 伸出
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(direction, 91, 13, 65, 90, loose, 500)  # 松开
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(90, level_servo_2, level_servo_3, level_servo_4, 90, loose, 500)  # 回
    time.sleep(.5)


if __name__ == '__main__':
    while 1:
        print("\n代号      指令")
        print("r         读取角度")
        print("st        设定角度")
        print("wm        居中待命")
        print("wl        左转待命")
        print("wr        右转待命")
        print("sc        瞭望")
        print("g         抓取")
        print("lp        左放置")
        print("rp        右放置")
        print("q         退出")
        command = input("\n请输入指令代码: \n>>>")
        if command == "r":
            print("\n当前指令  读取角度\n")
            read_servo_degree()
        elif command == "st":
            print("\n当前指令  设定角度\n")
            num = input("\n请输入目标角度(六个舵机，以空格隔开): \n>>>")
            degree = [int(n) for n in num.split(" ")]
            Arm.Arm_serial_servo_write6(degree[0], degree[1], degree[2], degree[3], degree[4], degree[5], 800)
        elif command == "wm":
            print("\n当前指令  居中待命\n")
            arm_standby(middle)
        elif command == "wl":
            print("\n当前指令  左转待命\n")
            arm_standby(left)
        elif command == "wr":
            print("\n当前指令  右转待命\n")
            arm_standby(right)
        elif command == "sc":
            print("\n当前指令  瞭望\n")
            arm_scout(middle)
        elif command == "g":
            print("\n当前指令  抓取\n")
            arm_grab([105, 66, 32, 56])
        elif command == "lp":
            print("\n当前指令  左放置\n")
            put_in_basket(left)
        elif command == "rp":
            print("\n当前指令  右放置\n")
            put_in_basket(right)
        elif command == "q":
            print("\n当前指令  退出\n")
            break
        else:
            print("\n未知指令，请重新输入\n")
            
