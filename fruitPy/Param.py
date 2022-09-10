import numpy as np


# #####################################################################
"""
detect_turn
"""
# 蓝色HSV阈值
blue_lower = np.array([100, 100, 50])  # h:色调 s:饱和度 v:明度
blue_upper = np.array([124, 255, 200])

morphology_kernel_size_turn = (5, 5)  # 形态学闭操作时的卷积核大小
erode_dilate_kernel_size_turn = (3, 3)  # 腐蚀膨胀时的卷积核大小
erode_iterations_turn = 3  # 腐蚀操作迭代次数
dilate_iterations_turn = 5  # 膨胀操作迭代次数

area_threshold = 30000  # 标志面积最小阈值

max_val_threshold = 0.3  # 相似度最低阈值
# #####################################################################


# #####################################################################
"""
detect_ball
"""
# 黄色HLS阈值
yellow_lower = np.array([0, 90, 160])  # h:色相  l:亮度  s:饱和度
yellow_upper = np.array([30, 255, 255])
# 白色BGR阈值
white_lower = np.array([220, 220, 230])  # b g r
white_upper = np.array([255, 255, 255])

morphology_kernel_size_ball = (5, 5)  # 形态学闭操作时的卷积核大小
erode_dilate_kernel_size_ball = (3, 3)  # 腐蚀膨胀时的卷积核大小
erode_iterations_ball = 3  # 腐蚀操作迭代次数
dilate_iterations_ball = 5  # 膨胀操作迭代次数

canny_threshold1 = 10  # canny最小阈值
canny_threshold2 = 100  # canny最大阈值

HoughCircles_param2 = 18  # 霍夫圆参数2
rmin = 30  # 霍夫圆最小半径
rmax = 90  # 霍夫圆最大半径
rmin_threshold = 86  # 最小半径自适应的上限

x_select_ref = 0.8  # 数据标准化参考值

n_pic_per_type = 3  # 模板库中每个种类包含的模板张数
# 可视情况自行添加模板匹配最小阈值和最大阈值（detect_ball.py中也需自行添加条件判断），以减少误判率以及提高速度

# 检查抓取情况时的兴趣域 [top bottom left right]  h20*w50，根据自己设备夹取到球时的实际情况自行修改
check_grab_roi = [459, 479, 254, 304]

ratio = 0.70  # 兴趣域内兴趣颜色像素点占比
# #####################################################################


# #####################################################################
"""
arm_coord_2_claw
"""
pi = 3.1415926
DE2RA = pi / 180.0
RA2DE = 180.0 / pi

# 相机内参矩阵参数
f_x_div_dx = 680.0  # 水平缩放，偏大（即左夹偏左，右夹偏右）调大
f_y_div_dy = 680.0  # 垂直缩放，偏大（即上夹偏上，下夹偏下）调大
u0 = 320.0  # 水平中心位置，偏左（即左夹右夹均偏左）调小
v0 = 240.0  # 垂直中心位置，偏上（即上夹下夹均偏上）调小

# 底座坐标系下相机位置参数 单位cm
y_camera_to_base = 3.7
z_camera_to_base = 24.8

D_object_to_camera_upper = 24.5
D_object_to_camera_lower = 27.5

# 夹爪参数 单位cm
j5_claw_delta_y = 8.5
j5_claw_delta_z = 1.15

#
sight_middle = 175
# #####################################################################


# #####################################################################
"""
basic
"""
yellow = 1
white = 0

arm_left = 180
arm_middle = 90
arm_right = 0

turn_left = "a"
turn_right = "d"
drive_ahead = "w"
drive_back = "s"

tight = 90
loose = 10
# #####################################################################


# 转向标识代号解码字典
def turn_mapping(turn):
    sign_code = {
        1: "left",
        2: "ahead",
        3: "right"
    }
    return sign_code.get(turn, None)


# 水果种类代号解码字典
def fruit_mapping(fruit_type):
    fruit_code = {
        1: "蓝莓",
        2: "红枣",
        3: "草莓",
        4: "无花果"
    }
    return fruit_code.get(fruit_type, None)
