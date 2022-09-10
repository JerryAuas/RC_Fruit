from ctypes import *
from operator import imod

import os

dir_path = os.getcwd()

lib = CDLL(dir_path + f'/Lib/serial.so')

def serial_communicate(data_send):
    lib.try1.argtypes = [c_char_p]
    lib.try1.restype = c_int
    ret = lib.try1(c_char_p(data_send))

    return ret


if __name__ == '__main__':
    print(serial_communicate(1))

