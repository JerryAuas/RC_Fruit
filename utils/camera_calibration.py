import cv2
import numpy as np
import glob

print("请确保当前路径下/data文件夹内有多角度的标定板照片素材，如无请先用calibration_data_recorder.py制作\n")
command = input("按Q退出，按其它任意键进行标定\n>>>")
if command == "Q":
    exit()
    
# 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

# 获取标定板角点的位置
"""
根据自己标定板格子的行列数(注意减去1)
"""
row = 9 - 1  # 行
column = 12 - 1  # 列
objp = np.zeros((row * column, 3), np.float32)
objp[:, :2] = np.mgrid[0:column, 0:row].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

obj_points = []  # 存储3D点
img_points = []  # 存储2D点

images = glob.glob("data/*.jpg")
for fname in images:
    img = cv2.imread(fname)
    cv2.imshow('img', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    size = gray.shape[::-1]
    ret, corners = cv2.findChessboardCorners(gray, (row, column), None)
    print(ret)

    if ret:

        obj_points.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
        # print(corners2)
        if [corners2]:
            img_points.append(corners2)
        else:
            img_points.append(corners)

        cv2.drawChessboardCorners(img, (8, 6), corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(1)

print("lenth:", len(img_points))
cv2.destroyAllWindows()

# 标定
print("计算中......\n")
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

print("内参数矩阵:\n", mtx, "\n")  # 内参数矩阵
print("-----------------------------------------------------")
print("畸变系数:\n", dist, "\n")  # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
print("-----------------------------------------------------")
print("旋转向量:\n", rvecs, "\n")  # 旋转向量  # 外参数
print("-----------------------------------------------------")
print("平移向量:\n", tvecs, "\n")  # 平移向量  # 外参数


