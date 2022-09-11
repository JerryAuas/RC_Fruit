import cv2


cam = 1  # 调用摄像头

while True:
    print(f"cam___{cam}")
    cap = cv2.VideoCapture(cam)
    ret, _ = cap.read()
    if not ret:
        cam += 1
    else:
        cap.release()
        cv2.destroyAllWindows()
        break

print(f"cam: {cam}")