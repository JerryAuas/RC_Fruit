import cv2


name = input("请输入图片名与格式(例xxx.jpg): \n>>>")

arr = input("\n请输入目标尺寸(长宽，以空格隔开): \n>>>")
size = [int(n) for n in arr.split()]

img = cv2.imread(name)
cv2.imshow("original", img)
img = cv2.resize(img, size)
cv2.imshow("resized", img)
cv2.waitKey(0)
cv2.imwrite("reaized_" + name, img)
