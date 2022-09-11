from Motion import *
from Detect_ball import detect_circles, detect_type, check_grab
from Arm_coord_2_claw import arm_coord_2_claw
from Serial_communication import serial_communicate
from Socket_communication import socket_communicate


def go_put_in_basket(basket):
    """
    :param basket: 目标放置篮  0 1 2 3
    """
    # 0 1 --> 6    2 3 --> 7
    ret = serial_communicate("6" if basket < 2 else "7")

    put_in_basket(arm_right if basket & 1 else arm_left)


def go_grab_retreat(cam, tree, color, circle_number, grab_time_out=10, go=True, retreat=True):
    """
    :param cam: 摄像头
    :param tree: 目标树  1 2 3 4
    :param color: 目标颜色
    :param circle_number: 当前树上应有目标颜色的果的数量
    :param grab_time_out: 抓取超时时间
    :param go: 是否需要前往目标树（默认需要）
    :param retreat: 是否需要退回交叉点（默认需要）
    :return: 抓取成功标志位
    """
    if go:
        ret = serial_communicate("4" if tree <= 2 else "5")  # 1 2 --> 4    3 4 --> 5
        if tree & 1:  # 奇数树号左转
            ret = serial_communicate(turn_left)
        else:
            ret = serial_communicate(turn_right)
        ret = serial_communicate(drive_ahead)

    grab_ok = 0
    trial_time = 0  # 最大尝试抓取次数
    t0 = time.time()
    grad_sum = 2    # 一个果树总计抓取的果子总数
    while not grab_ok and trial_time < 5 and (time.time() - t0) < grab_time_out and grad_sum:

        # 两次居中？

        arm_standby(arm_middle)  # 居中待命，稳定镜头
        arm_standby(arm_middle)  # 居中待命，稳定镜头
        circle, _ = detect_circles(cam, color=color, circle_number=circle_number, time_out=10, time_out_en=False)
        if not circle[2]:
            print(f"\n未检测到圆\n")
            continue
        print(f"\n当前圆位置参数： {circle}\n\n------开始抓取------\n")
        trial_time += 1

        # 解算第一个圆
        coord = arm_coord_2_claw([circle[0], circle[1]])
        data_ik = socket_communicate(coord)

        # 第一次抓取，共抓取两次
        arm_grab_put_side(data_ik)

        # 抓取检查
        grab_ok = check_grab(cam, color)

        # 如果抓取成功状态位减1
        if grab_ok:
            if grad_sum == 2:
                grab_ok -= 1
            grad_sum -= 1
            # 进行第二次抓取
        

    # 退回
    if retreat:
        ret = serial_communicate(drive_back)
        if tree & 1:  # 奇数树号右转
            ret = serial_communicate(turn_right)
        else:
            ret = serial_communicate(turn_left)

    return grab_ok


def go_detect_seq(cam, mode):
    """
    :param cam: 摄像头
    :param mode: 模式  1 放置区   0 采摘区
    :return: 果序
    """
    # 初始化检测区序列
    seq = [0, 0, 0, 0]

    # 前往检测起始点，开始循环检测
    last_fruit = 0  # 记录上一次的果号，简易防重
    pos = 6 if mode else 4  # 根据模式确定检测起始点位  
    for i in range(4):  # 检测4棵树
        print(f"\n第 {i + 1} 棵树")
        # 0 1 在第一个节点   2 3 在下一个节点
        if i == 0:
            ret = serial_communicate(str(pos))
        elif i == 2:
            pos = pos + 1
            ret = serial_communicate(str(pos))

        # 摄像头接近
        if mode:  # 放置区
            if i & 1:  # 1, 3   2， 4号树
                direction = arm_right
                arm_standby(direction, claw=tight)
            else:  # 0, 2   1， 3号树
                direction = arm_left
                arm_standby(direction, claw=tight)
        else:  # 采摘区
            if i & 1:  # 0, 2   1， 3号树
                ret = serial_communicate(turn_right)
                direction = turn_left  # 后续回退时的转向方向
            else:  # 1, 3   2， 4号树
                ret = serial_communicate(turn_left)
                direction = turn_right  # 后续回退时的转向方向
            ret = serial_communicate(drive_ahead)
            arm_standby(arm_middle)
        
        # 种类检测
        fruit_type = 0
        while not fruit_type or fruit_type is None or fruit_type in seq:  # 防重
            fruit_type = detect_type(cam, mode=mode, time_out=8, time_out_en=False)

        last_fruit = fruit_type
        seq[i] = last_fruit
        print(f"seq: {seq}")

        if seq[i] == 4:  # 最高权重果
            if mode:
                print("\n将4号放入框\n")
                put_in_basket(direction)
                pass
            else:
                print("\n将4号摘下\n")
                go_grab_retreat(cam, tree=i + 1, color=yellow, circle_number=2, go=False)  # 已到位，go=False
                pass
        
        if not mode:
            # 退回
            ret = serial_communicate(drive_back)
            ret = serial_communicate(direction)

    print(f"\nDetected Sequence: {seq}\n")
    return seq


if __name__ == '__main__':
    """
    功能测试  每次仅可取注一个测试命令
    """
    cam = 0

    """
    在位抓取测试
    """
#    go_grab_retreat(cam, tree=1, color=yellow, circle_number=1, grab_time_out=50, go=False, retreat=False)

    """
    前往抓取退回测试
    """
#    go_grab_retreat(cam, tree=1, color=yellow, circle_number=2, grab_time_out=20)

    """
    前往放置测试
    """
#    go_put_in_basket(basket=1)

    """
    前往测序测试
    """
#    go_detect_seq(cam, mode=0)
