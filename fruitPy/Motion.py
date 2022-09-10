import time
from Param import *
from Arm_Lib import Arm_Device


# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.01)


def arm_standby(direction, claw=loose):
    Arm.Arm_serial_servo_write6(direction, 180, 0, 0, 90, claw, 800)
    time.sleep(1)
    
    
def arm_scout(direction):
    Arm.Arm_serial_servo_write6(direction, 90, 90, 0, 90, loose, 800)
    time.sleep(1)  
    
    
def arm_midway():
    # 中途防碰撞位
    Arm.Arm_serial_servo_write6(90, 90, 30, 30, 90, loose, 800)
    time.sleep(1)


def arm_grab(data_ik):
    # 居中待命
    arm_standby(90)
    # 中途防撞
    arm_midway()
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
    Arm.Arm_serial_servo_write6(90, 180, 0, 0, 90, tight, 500)
    time.sleep(1)
    # 回中
    Arm.Arm_serial_servo_write6(90, 180, 0, 0, 90, tight, 500)
    time.sleep(.5)
    
    
def put_side():
    # 抓紧，左转
    Arm.Arm_serial_servo_write6(162, 180, 0, 0, 90, tight, 500)
    time.sleep(1)
    # 松开
    Arm.Arm_serial_servo_write6(162, 180, 0, 0, 90, loose, 500)
    time.sleep(.4)
    # 回中
    Arm.Arm_serial_servo_write6(90, 180, 0, 0, 90, loose, 500)
    time.sleep(.5)


def put_in_basket(direction):
    # 放球
    Arm.Arm_serial_servo_write6(direction, 180, 0, 0, 90, tight, 500)  # 转向到位
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(direction, 91, 13, 65, 90, tight, 500)  # 伸出
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(direction, 91, 13, 65, 90, loose, 500)  # 松开
    time.sleep(.5)
    Arm.Arm_serial_servo_write6(90, 180, 0, 0, 90, loose, 500)  # 回
    time.sleep(.5)
