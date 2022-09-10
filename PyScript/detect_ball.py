from ctypes  import *
import cv2
import numpy as np
from typing import List

import os

dir_path = os.getcwd()

so = cdll.LoadLibrary   
lib = so(dir_path+f'/Lib/detect_ball.so')   # absolute path


class detect_circless_(Structure):
    
    rows:int
    cols:int
    channels:int
    x:float
    y:float
    r:float
    data:(List[c_ubyte])
    _fields_ = [("rows",c_int32),("cols",c_int32),("channels",c_int32),("data",POINTER(c_ubyte)), ("x",c_float), ("y",c_float),("r",c_float)]
    def __str__(self):
        return "detect_circless(rows={},cols={},channels={},data:{}, x:{}, y:{}, r:{})".format(self.rows,self.cols,self.channels,List[c_ubyte], self.x, self.y, self.r)


def detect_circles(cam, color, number):
    lib.detect_circles.argtypes = [c_int, c_int, c_int]
    lib.detect_circles.restype = detect_circless_

    resultCI = lib.detect_circles(c_int(cam), c_int(color), c_int(number))

    circle = [resultCI.x, resultCI.y, resultCI.r]

    cols = resultCI.cols
    rows = resultCI.rows
    channels = resultCI.channels
    data = resultCI.data

    imgArr = string_at(data, cols*rows*channels)
    npArr = np.frombuffer(imgArr, np.uint8)
    imgDecode = cv2.imdecode(npArr, cv2.IMREAD_COLOR)

    return circle, imgDecode


def detect_type(cam, mode):
    lib.detect_type_.argtypes = [c_int, c_int]
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


def check_grab(cam, color):
    lib.check_grab_.argtypes = [c_int, c_int]
    lib.check_grab_.restype = c_int

    grab = lib.check_grab_(c_int(cam), c_int(color))

    return grab

if __name__ == '__main__':

    """
    circle
    """
    circle1, img = detect_circles(4, 1, 1)

    print()
    print("circle:",circle1)

    """
    type
    """
    # fruit_type = detect_type(4, 1)

    # print("fruit_type:", fruit_mapping(fruit_type))

    """
    check
    """
    # grab = check_grab(4, 1)
