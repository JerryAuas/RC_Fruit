import cv2


def is_number(s):
    try:
        n = int(s)
        return True
    except :
        return False


print("经本程序设定后，除非重新设定，相机将一直按设定值工作\n")
brightness = input("请输入亮度(初始值为0，参考范围 -64~64)\n>>>")
contrast = input("请输入对比度(初始值为16，参考范围 0~64)\n>>>")

cap = cv2.VideoCapture(0)

if is_number(brightness) and is_number(contrast):
    ##cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 设置帧宽 640
    ##cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 设置帧高 480
    cap.set(cv2.CAP_PROP_BRIGHTNESS, int(brightness))  # 设置亮度 0 （参考范围 -64~64）
    cap.set(cv2.CAP_PROP_CONTRAST, int(contrast))  # 设置对比度 16（参考范围 0~64）
    ##cap.set(cv2.CAP_PROP_EXPOSURE, -1)  # 设置曝光值 -1.0 （本套装原装相机无法调节）

print("\n帧宽:   ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("帧高:   ", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("亮度:   ", cap.get(cv2.CAP_PROP_BRIGHTNESS))
print("对比度: ", cap.get(cv2.CAP_PROP_CONTRAST))
print("曝光值: ", cap.get(cv2.CAP_PROP_EXPOSURE))

while True:
    ret, img = cap.read()
    if ret:
        cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

