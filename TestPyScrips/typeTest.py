from ctypes  import *
import cv2
import os

dir_path = os.getcwd()

so = cdll.LoadLibrary   
lib = so(dir_path+f'/Lib/detect_circles.so')

def detect_type(cam, mode):
    lib.detect_type_.argtypes = [c_int]
    lib.detect_type_.restype = c_int

    resultType = lib.detect_type_(c_int(cam), c_int(mode))

    return resultType
    
def fruit_mapping(fruit_type):
    fruit_code = {
        1: "蓝莓",
        2: "红枣",
        3: "草莓",
        4: "无花果"
    }
    return fruit_code.get(fruit_type, None)


if __name__ == '__main__':
    fruit_type = detect_type(0, 0)

    print("fruit_type:", fruit_mapping(fruit_type))
