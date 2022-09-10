from detect_turn import detect_turn
from Detect_qr import detect_qr
from Go_series import *
from Motion import arm_standby, arm_scout
from Serial_communication import serial_communicate


input("按回车运行\n>>>")
arm_standby(arm_middle)
chassic_reset = serial_communicate("0")

# 调用摄像头
cam = 0

# 前往1号交叉点读转向标识
traffic_position_get = serial_communicate("1")
if traffic_position_get:
    arm_scout(arm_middle)
    turn = detect_turn(cam, sample_time=9, time_out=20, time_out_en=False)
    arm_standby(arm_middle)
    if turn == 1:
        ret = serial_communicate(turn_left)
    elif turn == 3:
        ret = serial_communicate(turn_right)

# 前往2号交叉点读二维码
qr_position_get = serial_communicate("2")
flag_qr = 0
fruit_seq = [0, 0, 0, 0]
if qr_position_get:
    arm_scout(arm_middle)
    flag_qr, fruit_seq = detect_qr(cam, time_out=5, time_out_en=False)
    arm_standby(arm_middle)

fruit_tree_basket = np.zeros((3, 4))  # 3行4列空映射表，第1行树号，第2行采摘区果号，第3行放置区果号
fruit_tree_basket[1] = [1, 2, 3, 4]  # 初始化树号

if flag_qr:  # 解到二维码，抓果，运输，放置区测序，放置
    fruit_tree_basket[0] = list(fruit_seq)

    # 按果号倒序排列映射表
    fruit_tree_basket = fruit_tree_basket.T[np.lexsort(-fruit_tree_basket[::-1, :])].T
    print("\n果号： ", fruit_tree_basket[1])
    print("树号： ", fruit_tree_basket[0], "\n")

    # 前往4号果对应的树（fruit_tree_basket2行1列），抓黄果，返回交叉点待命
    grab_ok = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][0]),
                              color=yellow, circle_number=2, grab_time_out=10)
    if grab_ok:
        fruit_tree_basket[2] = go_detect_seq(cam, mode=1)   # 放置区测序

else:
    fruit_tree_basket[0] = go_detect_seq(cam, mode=0)  # 如无意外，已抓取到4号果

    # 按果号倒序排列映射表
    fruit_tree_basket = fruit_tree_basket.T[np.lexsort(-fruit_tree_basket[::-1, :])].T
    print("\n果号： ", fruit_tree_basket[1])
    print("树号： ", fruit_tree_basket[0], "\n")

    fruit_tree_basket[2] = go_detect_seq(cam, mode=1)  # 放置区测序

# 抓4号果第二颗黄球
grab_ok = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][0]),
                          color=yellow, circle_number=1, grab_time_out=10)
if grab_ok:
    go_put_in_basket(int(np.where(fruit_tree_basket[2] == 4)[0][0]))
# 抓4号果第一颗白球
grab_ok = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][0]),
                          color=white, circle_number=1, grab_time_out=10)
if grab_ok:
    go_put_in_basket(int(np.where(fruit_tree_basket[2] == 4)[0][0]))

# 4号已放置完，取、放3,2,1
for i in range(3):  # 树
    for j in range(2):  # 黄果
        grab_ok = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][i + 1]),
                                  color=yellow, circle_number=2 - i, grab_time_out=10)
        if grab_ok:
            go_put_in_basket(int(np.where(fruit_tree_basket[2] == 3 - i)[0][0]))
    # 白果
    grab_ok = go_grab_retreat(cam, tree=int(fruit_tree_basket[1][i + 1]),
                              color=yellow, circle_number=1, grab_time_out=10)
    if grab_ok:
        go_put_in_basket(int(np.where(fruit_tree_basket[2] == 3 - i)[0][0]))

# 去终点
park = serial_communicate("8")
