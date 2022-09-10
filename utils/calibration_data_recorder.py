import cv2


print("请在尽可能多的不同角度对标定板进行拍照\n按空格保存当前帧，按Esc退出")

cap = cv2.VideoCapture(0)

i = 1
while True:
    ret, img = cap.read()
    if not ret:
        continue
    key = cv2.waitKey(1) & 0xFF
    cv2.imshow("video", img)
    if key == 27:
        break
    elif key == ord(" "):
        cv2.imshow("save"+str(i), img)
        cv2.waitKey(2000)
        cv2.destroyWindow("save"+str(i))
        cv2.imwrite("data/"+str(i)+".jpg", img)
        i += 1
