import math
from param import *


def arm_coord_2_claw(pixel):
    """
    :param pixel: 像素平面上点的坐标
    :return: 夹爪中心应在底座坐标系下的位置
    """
    # 相平面坐标系
    x_image = pixel[0] - u0
    y_image = pixel[1] - v0
    if pixel[1] < sight_middle:  # 根据高度进行物体距离判断（或可自行获取底盘超声波测距结果进行处理）  //175
        D_object_to_camera = D_object_to_camera_upper
    else:
        D_object_to_camera = D_object_to_camera_lower
#    print(f"\n物体到相机CCD距离: {D_object_to_camera}")

    # 相机坐标系
    x_camera = x_image * D_object_to_camera / f_x_div_dx
    y_camera = y_image * D_object_to_camera / f_y_div_dy

    # 底座坐标系     车头超前，x正方向指向车身右侧，y正方向指向车头，z正方向竖直向上
    coord = []  # z y z Roll Pitch Yaw
    coord.append(x_camera)  # x
    coord.append(D_object_to_camera - y_camera_to_base)  # y
    coord.append(z_camera_to_base - y_camera)  # z
#    print(f"原始底座坐标系坐标: {['%.2f' %coord[i] for i in range(2)]}")

    theta = math.atan2(coord[1], coord[0])
#    print(f"偏移角度: {theta * RA2DE :.2f}")  # 底座坐标系下球心与原点的夹角

    # ROLL值选取，仰夹为(0, -90)，水平夹为-90，俯夹为(-90, -180)
    if coord[2] >= 25:  # 根据物体高度进行俯仰角判断（或可自定义一映射关系）
        coord.append(-80.0)  # 10度仰角夹取
    else:
        coord.append(-100.0)  # 10度俯角夹取
#    print(f"俯仰角度: {coord[3]:.2f}")
    coord.append(0.0)  # PITCH
    coord.append(0.0)

    # 引入夹爪长度，根据俯仰角，目标点与原点的夹角更新xyz
    l_j5_claw = math.sqrt(j5_claw_delta_y**2 + j5_claw_delta_z**2)
    pitch_claw = (coord[3] + 180) * DE2RA - math.atan2(j5_claw_delta_z, j5_claw_delta_y)  # 夹爪基线不通过j5，需偏移
    coord[0] = coord[0] - l_j5_claw * math.sin(pitch_claw) * math.cos(theta)
    coord[1] = coord[1] - l_j5_claw * math.sin(pitch_claw) * math.sin(theta)
    coord[2] = coord[2] + l_j5_claw * math.cos(pitch_claw)

#    print(f"\n更新数据结果:\n{['%.2f' %i for i in coord]}\n")
    return coord


if __name__ == '__main__':
    circle = [100, 200, 30]  # 测试样本
    coord = arm_coord_2_claw([int(circle[0]), int(circle[1])])
    print("coord", coord)
    