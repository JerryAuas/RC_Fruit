from ctypes import *

import os

dir_path = os.getcwd()

coord = []

class Rect(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('Roll', c_float),
        ('Pitch', c_float),
        ('Yaw', c_float)
    ]

lib = CDLL(dir_path + f'/Lib/arm_coord_2_claw.so')

float_arg_x = c_float(100)
float_arg_y = c_float(200)

# arr = lib.arm_coord_2_claw(int_arg_x, int_arg_y)

def c_obtain_rect_array_and_free(x, y):
    """
    parm@ x:  像素点坐标
    parm@ y: 
    return@ coord: list[]
    
    """
    lib.arm_coord_2_claw.argtypes = [POINTER(c_float), POINTER(c_float)]
    lib.arm_coord_2_claw.restype = POINTER(Rect)

    rect_pt = lib.arm_coord_2_claw(byref(float_arg_x), byref(float_arg_y))

    # 结构体数组初始化
    # rect_pt.contents只能输出首元素的内容，rect_pt.contents.index
    # rect_array = [rect_pt[i] for i in range(6)]

    # for item in rect_array:
    # print("x:", rect_pt[0].x, "yaw:", rect_pt[0 ].Yaw)

    coord.append(rect_pt[0].x)
    coord.append(rect_pt[0].y)
    coord.append(rect_pt[0].z)
    coord.append(rect_pt[0].Roll)
    coord.append(rect_pt[0].Pitch)
    coord.append(rect_pt[0].Yaw)

    return coord



if __name__ == '__main__':

    c = c_obtain_rect_array_and_free(x=float_arg_x, y=float_arg_y)

    print(c)