import cv2


name = input("请输入保存名称(例xxx): \n>>>")
print(f"本次录像将保存为{name}.mp4\n")
cap = cv2.VideoCapture(0)
    
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频格式
fps = cap.get(cv2.CAP_PROP_FPS)  # 视频帧率
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 视频宽高
out = cv2.VideoWriter(f"{name}.mp4", fourcc, fps, size)   

while cap.isOpened():
    ret, img = cap.read()
    out.write(img)
    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
            
cap.release()
cv2.destroyAllWindows()

