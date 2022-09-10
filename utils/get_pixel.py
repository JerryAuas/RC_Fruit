import cv2


def get_bgr(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("pixel x y: ", x, y)
        print("[B G R]: ", bgr[y, x], "\n")
#        print(bgr[y, x])


def get_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("pixel x y: ", x, y)
        print("[h s v]: ", hsv[y, x], "\n")
#        print(hsv[y, x])
        
        
def get_hls(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("pixel x y: ", x, y)
        print("[h l s]: ", hls[y, x], "\n")
#        print(hls[y, x])


print("点击对应色彩模式的界面，即可得点击位置的像素点在该色彩模式下的值")
cap = cv2.VideoCapture(0)
cv2.namedWindow("BGR")
cv2.moveWindow("BGR", 10, 0)
cv2.namedWindow("HSV")
cv2.moveWindow("HSV", 640, 0)
cv2.namedWindow("HLS")
cv2.moveWindow("HLS", 310, 330)

while True:
    ret, bgr = cap.read()
    if ret:
        bgr = cv2.resize(bgr, (320, 240))
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)
        cv2.imshow("BGR", bgr)
        cv2.imshow("HSV", hsv)
        cv2.imshow("HLS", hls)
        cv2.setMouseCallback("BGR", get_bgr)
        cv2.setMouseCallback("HSV", get_hsv)
        cv2.setMouseCallback("HLS", get_hls)
        
        key = cv2.waitKey(100) & 0xFF
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
