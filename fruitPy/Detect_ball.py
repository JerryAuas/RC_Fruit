import cv2
import time
from Param import *


def z_score(stats, ref=0.8):  # 数据标准化
    """
    :param stats: 输入数组
    :param ref: 参考值（默认0.8）
    :return: 输入数组满足参考值条件的对应的布尔数组
    """
    mean = np.mean(stats)
    std = np.std(stats)
    if not std:
        return [True for _ in stats]
    stats_z = [(s - mean) / std for s in stats]
    return np.abs(stats_z) < ref


def color_filter(img, color):
    """
    :param img: 图像帧
    :param color: 目标颜色
    :return: 筛选后的二值图像
    """
    if color:  # 黄色为真
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)  # 黄色乒乓球在hls色彩模式下区别度较高
        thresh_lower = yellow_lower
        thresh_upper = yellow_upper
    else:  # 白色乒乓球在bgr色彩模式下区别度较高
        thresh_lower = white_lower
        thresh_upper = white_upper

    img = cv2.inRange(img, thresh_lower, thresh_upper)

    return img


def find_circle(img, color, circle_number):
    """
    :param img: 图像帧
    :param color: 目标颜色
    :param circle_number: 当前树上应有目标颜色的果的数量
    :return: 圆参数
    """
    img = color_filter(img, color)
    cv2.imshow("Filtered", img)
    # 模糊
    img = cv2.GaussianBlur(img, (11, 11), 2, 2)

    # 二值化
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 使区域闭合无空隙
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morphology_kernel_size_ball)  # 卷积核大小
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Closed", img)

    # 腐蚀和膨胀
    element = cv2.getStructuringElement(cv2.MORPH_RECT, erode_dilate_kernel_size_ball)
    img = cv2.erode(img, element, iterations=erode_iterations_ball)
    cv2.imshow("erode", img)
    img = cv2.dilate(img, element, iterations=dilate_iterations_ball)
    cv2.imshow("dilate", img)

    # canny边缘检测
    img = cv2.Canny(img, threshold1=canny_threshold1, threshold2=canny_threshold2)
    cv2.imshow("Canny", img)

    # 自适应霍夫圆检测
    num = 0
    r_min = rmin
    circles = [[[0, 0, 0]]]
    while num != circle_number and r_min < rmin_threshold:
        r_min += 2
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp=1, minDist=100, param1=100,  # 不建议修改
                                   param2=HoughCircles_param2, minRadius=r_min, maxRadius=rmax)  # 可修改的参数
        # param2，越小，检测到越多近似的圆； 越大，检测到的圆越接近完美的圆形
        # minRadius，最小检测圆半径，maxRadius，最大检测圆半径
        if circles is None:
            continue
        num = len(circles[0])
        print("circles detected", circles)
        print("====================\n\n")
    return circles


def detect_circles(cam, color, circle_number, sample_times=9, time_out=5, time_out_en=False):
    """
    :param cam: 摄像头
    :param color: 目标颜色
    :param circle_number: 当前树上应有目标颜色的果的数量
    :param sample_times: 采样次数
    :param time_out: 超时时间（默认5s）
    :param time_out_en: 超时允许（默认不允许超时）
    :return: 第一个圆参数
    """
    print("\n------开始检测圆位置------\n")
    t0 = time.time()
    
    detect_fail = 0
    sample_time = 0
    x_table = []
    y_table = []
    r_table = []
    
    cap = cv2.VideoCapture(cam)
    
    while sample_time < sample_times:
        detect_fail = 0
        # 超时退出
        task_time = time.time() - t0
        if not time_out_en and task_time >= time_out:
            print("\n超时未检测到圆\n")
            detect_fail = 1
            break

        ret, img = cap.read()
        if not ret:
            continue

        if cv2.waitKey(1) & 0xff == 27:
            break

        circles = find_circle(img, color, circle_number)

        if circles is None:
            continue

        if circles[0][0][2] == 0:  # 半径为0
            continue

        num = len(circles[0])
        sample_time += 1

        if num == 2:  # 水平排序
            if circles[0][0][0] > circles[0][1][0]:
                temp = circles[0][0]
                circles[0][0] = circles[0][1]
                circles[0][1] = temp
        # 记录数据
        x_table.append(circles[0][0][0])
        y_table.append(circles[0][0][1])
        r_table.append(circles[0][0][2])

#        # 在原图上画圆
        for i in range(num):
            cv2.circle(img,
                       (int(circles[0][i][0]), int(circles[0][i][1])),
                       int(circles[0][i][2]),
                       (255, 0, 100), 2)
        cv2.imshow("circles", img)
        cv2.waitKey(100)

    cv2.destroyAllWindows()
    
    if detect_fail:
        cap.release()
        return [0, 0, 0], img
    else:
        print("\nx_table", x_table)
        x_select = z_score(x_table, ref=x_select_ref)
        print("\nx_select", x_select)
        if not any(x_select):
            cap.release()
            return [0, 0, 0], img
        x_sum = y_sum = r_sum = real_time = 0
        for i in range(len(x_select)):
            if x_select[i]:
                x_sum += x_table[i]
                y_sum += y_table[i]
                r_sum += r_table[i]
                real_time += 1
        cap.release()
        t3 = time.time()
        print("time: ", t3 - t0)
        return [int(x_sum / real_time), int(y_sum / real_time), int(r_sum / real_time)], img


def detect_type(cam, mode, time_out=8, time_out_en=False):
    """
    :param cam: 摄像头
    :param mode: 检测模式（0 采摘区  1 放置区）
    :param time_out: 超时时间（默认8s）
    :param time_out_en: 超时允许（默认不允许超时）
    :return: 水果种类
    """
    best_match = 0  # 最佳匹配结果
    fruit_type = 0
    left_top = [0, 0]
    right_bottom = [0, 0]

    t0 = time.time()
    # 当在时间范围内，且未检测到水果种类
    while fruit_type == 0:
        task_time = time.time() - t0
        if not time_out_en and task_time >= time_out:
            print("\n超时\n")
            break
        
        circle, img = detect_circles(cam, color=yellow, circle_number=2-mode, time_out=5, time_out_en=False)

        l_t_x = circle[0] - circle[2]
        l_t_y = circle[1] - circle[2]
        r_b_x = circle[0] + circle[2]
        r_b_y = circle[1] + circle[2]
        # 边界处理
        l_t_x = l_t_x if l_t_x >= 0 else 0
        l_t_y = l_t_y if l_t_y >= 0 else 0
        r_b_x = r_b_x if r_b_x <= 639 else 639
        r_b_y = r_b_y if r_b_y <= 479 else 479
        # 截取
        img_roi = img[l_t_y:r_b_y, l_t_x:r_b_x]
        
        # 排除因未检测到圆而未截取到roi
        if not img_roi.shape[0]:
            print("\n检测圆失败，无法检测种类或精度将降低\n")
            img_roi = img

        # 种类检测
        print("\n------开始检测种类------\n")
        for i in range(1, 5):
            pic = 0  # 某一种类的第几张照片最匹配
            for j in range(1, n_pic_per_type + 1):
                name = f"{i}{j}.jpg"  # 读取模板
                template = cv2.imread(f"template_f/{name}")
                temp_h, temp_w = template.shape[:2]
                
                # 判断模板尺寸是否超过输入图像尺寸
                roi_h, roi_w = img_roi.shape[:2]
                if temp_h > roi_h or temp_w > roi_w:
                    print("\nErr! templ oversize\n")
                    return None

                res = cv2.matchTemplate(img_roi, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                if max_val > best_match:  # 最佳匹配更新
                    best_match = max_val
                    fruit_type = i  # 记录当前种类
                    left_top = max_loc
                    right_bottom = (left_top[0] + temp_w, left_top[1] + temp_h)
                    pic = j
## # 结果展示                    
                print(f"type:{i} pic:{j} max_val:{max_val} max pic:{pic} detected type:{fruit_type}")

            print("\n")

        cv2.rectangle(img_roi, left_top, right_bottom, (255, 0, 255), 2)
        cv2.putText(img_roi, f"type{fruit_type}", left_top, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.namedWindow("match")
        cv2.moveWindow("match", 10, 0)
        cv2.imshow("match", img_roi)
        cv2.waitKey(1500)

    cv2.destroyAllWindows()
    print(f"fruit type detected as: {fruit_mapping(fruit_type)}")
    return fruit_type


def check_grab(cam, color):
    """
    :param cam: 摄像头
    :param color: 目标颜色
    :return: 抓取成功标志位
    """
    count = 0
    grab_ok = 0
    time.sleep(1)
    t0 = time.time()
    cap = cv2.VideoCapture(cam)
    
    while not grab_ok:
        count += 1
        ret, img = cap.read()
        # 超时退出
        task_time = time.time() - t0
        if task_time >= 5:
            print("\n超时\n")
            break
        if not ret:
            break
        else:
            img_roi = img[check_grab_roi[0]:check_grab_roi[1],
                          check_grab_roi[2]:check_grab_roi[3]]  # 选取roi(h20*w50，根据自己设备夹取到时球的实际位置自行修改)
            img_roi = color_filter(img_roi, color)
            cv2.rectangle(img,
                          (check_grab_roi[2], check_grab_roi[0]),
                          (check_grab_roi[3], check_grab_roi[1]),
                          (255, 0, 255), 2)
            cv2.imshow("img", img)
            cv2.imshow("img_roi", img_roi)
            cv2.waitKey(1)
            # 找出图像数组内的值num，计算各值出现的次数value
            num, value = np.unique(img_roi, return_counts=True)
            try:  # 防止全黑报错
                print("ratio: ", value[np.where(num == 255)[0][0]] / 1000)
                # roi内有兴趣颜色(此时二值图内的白色区域，值为255)，且对应颜色的像素点个数占比超过ratio
                if 255 in num and value[np.where(num == 255)[0][0]] / 1000 > ratio:
                    print("\n成功抓取到\n")
                    grab_ok = 1
                    cv2.waitKey(1000)
            except:
                print("ratio:  0")            
                print("\n抓取失败\n")
    
    if not grab_ok:
        print("\n抓取失败\n")
    print(count)
    cv2.destroyAllWindows()
    cap.release()
    return grab_ok


if __name__ == '__main__':
    """
    功能测试  每次仅可取注一个功能进行测试
    """
    pass
    """
    颜色筛选检测
    """
#    cap = cv2.VideoCapture(0)
#    while 1:
#        ret, img = cap.read()
#        if not ret:
#            continue
#        else:
#            cv2.imshow("orig", img)
#            img = color_filter(img, yellow)
#            cv2.imshow("filtered", img)

#        if cv2.waitKey(1) & 0xff == 27:
#            break
#    cv2.destroyAllWindows()
#    cap.release()

    """
    圆检测测试
    """
    cam = "samples/detect_ball.mp4"
#    cam = 0
    circle, img = detect_circles(4, color=yellow, circle_number=1, sample_times=20, time_out=10, time_out_en=False)
    print("First circle:", circle)

    """
    种类检测测试
    """
#    cam = "samples/detect_ball.mp4"
##    cam = 0
#    fruit_type = detect_type(cam, mode=0, time_out=15, time_out_en=False)
#    print("fruit_type:", fruit_mapping(fruit_type))

    """
    抓取检测测试
    """
#     cam = "samples/check_grab.mp4"
# #    cam = 0
#     check_grab(4, yellow)
