import cv2
import time
from Param import *


def find_sign(img):
    """
    :param img: 图像帧
    :return: flag 截取成功标志位   img 帧内截取的标识图片
    """
    flag = 0  # 识别到标识标志位

    img_src = img.copy()
    cv2.imshow("img", img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", img)

    # 提取蓝色区域
    img = cv2.inRange(img, blue_lower, blue_upper)
    cv2.imshow("inRange", img)
    
    # 模糊
    img = cv2.GaussianBlur(img, (11, 11), 2, 2)

    # 二值化
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # 形态学闭操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morphology_kernel_size_turn)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("closed", img)

    # 腐蚀和膨胀
    element = cv2.getStructuringElement(cv2.MORPH_RECT, erode_dilate_kernel_size_turn)
    img = cv2.erode(img, element, iterations=erode_iterations_turn)
    cv2.imshow("erode", img)
    img = cv2.dilate(img, element, iterations=dilate_iterations_turn)
    cv2.imshow("dilate", img)

    # 找轮廓
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    print("轮廓个数：", len(contours))

    for con in contours:
        # 遍历计算轮廓面积
        area = cv2.contourArea(con)
        print("轮廓面积", area)
        # 面积过滤，滤除环境噪点
        if area < area_threshold:  # 判断条件可自行优化
            continue
        # 轮廓转换为矩形
        rect = cv2.minAreaRect(con)
        # 矩形转换为box
        box = np.int0(cv2.boxPoints(rect))
        # 在原图画出目标区域
        cv2.drawContours(img_src, [box], -1, (0, 0, 255), 2)
        cv2.imshow("img_src_sign", img_src)

        # 计算轮廓的正矩形包围框左上(t_l)与右下(r_b)角点
        l_t_x = min([box][0][0][0], [box][0][1][0], [box][0][2][0], [box][0][3][0])
        l_t_y = min([box][0][0][1], [box][0][1][1], [box][0][2][1], [box][0][3][1])
        r_b_x = max([box][0][0][0], [box][0][1][0], [box][0][2][0], [box][0][3][0])
        r_b_y = max([box][0][0][1], [box][0][1][1], [box][0][2][1], [box][0][3][1])
        # 防错，确保裁剪区域无异常
        if l_t_x > 0 and l_t_y > 0 and r_b_x > 0 and r_b_y > 0 and r_b_y - l_t_y > 0 and r_b_x - l_t_x > 0:
            # 裁剪矩形区域
            img = img_src[l_t_y:r_b_y, l_t_x:r_b_x]
            cv2.imshow("sign", img)
            # 缩放至模板尺寸
            img = cv2.resize(img, (30, 30))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.waitKey(1)
            flag = 1

    return flag, img


# 模板匹配分类标识
def match_template(img):
    """
    :param img: 标识图像
    :return: 标识解码
    """
    # 读取模板
    template_left = cv2.imread("template_t/left.jpg")
    template_left = cv2.cvtColor(template_left, cv2.COLOR_BGR2GRAY)
    template_right = cv2.imread("template_t/right.jpg")
    template_right = cv2.cvtColor(template_right, cv2.COLOR_BGR2GRAY)
    template_ahead = cv2.imread("template_t/ahead.jpg")
    template_ahead = cv2.cvtColor(template_ahead, cv2.COLOR_BGR2GRAY)

    # 计算与左转的相似度
    res_left = cv2.matchTemplate(img, template_left, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res_left)

    # 计算与直行的相似度
    res_ahead = cv2.matchTemplate(img, template_ahead, cv2.TM_CCOEFF_NORMED)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res_ahead)

    # 计算与右转的相似度
    res_right = cv2.matchTemplate(img, template_right, cv2.TM_CCOEFF_NORMED)
    min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res_right)

    print(f"left: {max_val1:.5f}\tahead: {max_val2:.5f}\tright: {max_val3:.5f}")
    max_val = max(max_val1, max_val2, max_val3)  # 求最大的相似度，认为是该标识
    
    # 相似度过小
    if max_val < max_val_threshold:
        return 0

    if max_val == max_val1:
        print("left")
        return 1
    elif max_val == max_val2:
        print("ahead")
        return 2
    elif max_val == max_val3:
        print("right")
        return 3


def detect_turn(cam, sample_time, time_out=8, time_out_en=False):
    """
    :param cam: 摄像头
    :param sample_time: 采样次数
    :param time_out: 超时时间（默认8s）
    :param time_out_en: 超时允许（默认不允许超时）
    :return: 采样众数
    """
    cap = cv2.VideoCapture(cam)
    print("\n开始识别转向标识\n")
    t0 = time.time()
    datalist = []
    num = 0
    majorityElement = 2  # 默认为直行，若未识别到，则直行

    while 1:
        task_time = time.time() - t0
        if not time_out_en and task_time >= time_out:
            print("\n超时，未识别到转向标识\n")
            break

        ret, img = cap.read()
        if not ret:
            continue
        cv2.imshow("video", img)

        key = cv2.waitKey(1) & 0xFF
        
        # 寻找标志区域图片
        flag, sign = find_sign(img)
        if flag:
            # 分类标识
            turn_current = match_template(sign)
        else:
            continue
        # 当前采样到的标志
        if turn_current:
#            print("turn_current", turn_current)
            datalist.append(turn_current)
            num += 1
            if num == sample_time:  # 达到设置的采样次数
                majorityElement = np.argmax(np.bincount(datalist))  # 求众数
                print(f"\n转向标识识别结束，识别为: {turn_mapping(majorityElement)}\n")
                break

        print("====================\n\n")
        if key == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    return majorityElement


if __name__ == '__main__':
    """
    功能测试  每次仅可取注一个功能进行测试
    """
    pass
    """
    image test
    """
    # img = cv2.imread("samples/testr.jpg")
    # ret, roi = find_sign(img)
    # turn = match_template(roi)
    # print("\n转向标识: ", turn_mapping(turn))

    """
    video test
    """
#     cam = "samples/detect_turn.mp4"
# #    cam = 0
#     turn = detect_turn(cam, sample_time=100, time_out=20, time_out_en=True)
#     print("\n转向标识: ", turn_mapping(turn))
