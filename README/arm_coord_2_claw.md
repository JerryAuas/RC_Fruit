# 作出任何更改均需要对连接库作出更改

# arm_coord_2_claw..py

    # 默认参数
    pi = 3.1415926
    DE2RA = pi / 180.0
    RA2DE = 180.0 / pi


    # 根据高度进行物体距离判断（或可自行获取底盘超声波测距结果进行处理
    sight_middle:    //默认 ：175



    # 已知停止线到交叉点的距离为 190mm,果树底座到交叉点的最短距离为 500mm,在此基础上测量当小车停止到停止线上时水果在相机坐标系中的 D_object_to_camera_upper 与D_object_to_camera_lower 值(即距离

    # 底座坐标系下相机位置参数 单位cm
    y_camera_to_base = 3.7
    z_camera_to_base = 24.8
    D_object_to_camera_upper = 24.5
    D_object_to_camera_lower = 27.5




    # 相机内参矩阵参数
    f_x_div_dx = 680.0  # 水平缩放，偏大（即左夹偏左，右夹偏右）调大
    f_y_div_dy = 680.0  # 垂直缩放，偏大（即上夹偏上，下夹偏下）调大
    u0 = 320.0  # 水平中心位置，偏左（即左夹右夹均偏左）调小
    v0 = 240.0  # 垂直中心位置，偏上（即上夹下夹均偏上）调小

    # print(f"偏移角度: {theta * RA2DE :.2f}")  # 底座坐标系下球心与原点的夹角    (atan2(y, x) 反正切)
    float theta   


    # 引入夹爪长度，根据俯仰角，目标点与原点的夹角更新xyz
        l_j5_claw = math.sqrt(j5_claw_delta_y**2 + j5_claw_delta_z**2)



    # 夹爪参数 单位cm
    j5_claw_delta_y = 8.5
    j5_claw_delta_z = 1.15


    # 返回值
    coord[5]

    x    y      z      Roll    Pitch     Yaw