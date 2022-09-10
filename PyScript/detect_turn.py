from ctypes import *
import os

dir_path = os.getcwd()

lib = CDLL(dir_path + f'/Lib/detect_turn.so')


def detect_turn(cam):
    cam = c_int(cam)
    majorityElement = lib.detect_turn(cam)

    print(majorityElement)

    return majorityElement


# 转向标识代号解码字典
def turn_mapping(turn):
    sign_code = {
        1: "left",
        2: "ahead",
        3: "right"
    }
    return sign_code.get(turn, None)



if __name__ == '__main__':

    a = detect_turn(0)

    print("\n转向标识: ", turn_mapping(a))