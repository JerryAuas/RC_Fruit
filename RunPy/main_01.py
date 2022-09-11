import re
import sys
from tkinter.tix import Tree
sys.path.append('PyScript/')
from detect_turn import detect_turn
from detect_qr import detect_qr
from go_series import *
from detect_ball import *
from motion import arm_standby, arm_scout
from serial import serial_communicate



input("按回车运行\n>>>")
arm_standby(arm_middle)
chassic_reset = serial_communicate("0")

# 调用摄像头
cam = 0  # 调用摄像头

while True:
    cap = cv2.VideoCapture(cam)
    ret, _ = cap.read()
    if not ret:
        cam += 1
    else:
        cap.release()
        cv2.destroyAllWindows()
        break

traffic_position_get = serial_communicate("1")  # 前往1号交叉点
if traffic_position_get:
    arm_scout(arm_middle)  # 机械臂抬起
    turn = detect_turn(cam, sample_time=9, time_out=20, time_out_en=False)  # 读转向标识
    arm_standby(arm_middle)  # 机械臂待命位
    if turn == 1:  # 识别结果左转
        ret = serial_communicate(turn_left)
    elif turn == 3:  # 识别结果右转
        ret = serial_communicate(turn_right)

qr_position_get = serial_communicate("2")  # 前往2号交叉点
flag_qr = 0  # 初始化解码成功标志位为失败
fruit_seq = [0, 0, 0, 0]  # 初始化解码结果
if qr_position_get:
    arm_scout(arm_middle)  # 机械臂抬起
    flag_qr, fruit_seq = detect_qr(cam, time_out=5, time_out_en=False)  # 读二维码
    arm_standby(arm_middle)  # 机械臂待命位

fruit_tree_basket = np.zeros((3, 4))  # 创建3行4列空表，第1行存采摘区果号，第2行存树号，第3行存放置区果号
fruit_tree_basket[1] = [1, 2, 3, 4]  # 初始化树号

if flag_qr:  # 解到二维码
    fruit_tree_basket[0] = list(fruit_seq)  # 解码结果记录到第1行
    fruit_tree_basket = fruit_tree_basket.T[np.lexsort(-fruit_tree_basket[::-1, :])].T  # 按果号(第1行)倒序排列整张映射表
    print("\n树号： ", fruit_tree_basket[1])
    print("果号： ", fruit_tree_basket[0], "\n")

    # 前往4号果对应的树（fruit_tree_basket2行1列），此时树上应有2个黄果，20s内抓1个，退回交叉点待命
    # 第一次抓取果子时候只需进行一次抓取加放置操作，不需退回节点

    grab_ok_1, grab_sum_1 = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][0]),
                              color=yellow, circle_number=2, grab_time_out=20) # retreat= False 代表不需要返回

    num_4 = np.zeros((2, 1)) # 创建一行一列的空表，用以记录已抓取的果子数量
    num_4[0] = grab_sum_1  # 更新无花果黄球计数
    
    # 此时树上已经采摘完无花果，下面采摘草莓
    grab_ok_2, grab_sum_2 = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][1]),
                                  color=yellow, circle_number=2, grab_time_out=10)

    num_4[1] = grab_sum_2 # 更新草莓数量

    if grab_ok_1 or grab_ok_2:
        if grab_ok_1:
            fruit_tree_basket[2], _ = go_detect_seq(cam, mode=1, sum=num_4[0])   # 放置区测序，记录到第3行(测序时会将抓到的4号果对应放置)，此时无花果已经放置
        else: 
            fruit_tree_basket[2], _ = go_detect_seq(cam, mode=1, sum=num_4[1])
    # 接下来放置草莓
    if grab_ok_2:
        go_put_in_basket(int(np.where(fruit_tree_basket[2] == 3)[0][0]), sum=num_4[1])

else:  # 未解到二维码
    fruit_tree_basket[0], grab_ok = go_detect_seq(cam, mode=0)  # 前往采摘区测序
    num_4 = 1 if grab_ok else 2  # 更新黄球计数

    fruit_tree_basket = fruit_tree_basket.T[np.lexsort(-fruit_tree_basket[::-1, :])].T  # 按果号(第1行)倒序排列整张映射表
    print("\n果号： ", fruit_tree_basket[1])
    print("树号： ", fruit_tree_basket[0], "\n")

    fruit_tree_basket[2], _ = go_detect_seq(cam, mode=1)  # 放置区测序



# 去终点
park = serial_communicate("8")
