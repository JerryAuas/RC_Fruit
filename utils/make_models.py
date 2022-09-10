import cv2
                

def model_mapping(model_type):
    model_code = {
        1: "蓝莓",
        2: "红枣",
        3: "草莓",
        4: "无花果",
        5: "left",
        6: "ahead",
        7: "right"
    }
    return model_code.get(model_type, None)
    
            
def get_model(i, pic_name, img):
    roi = cv2.selectROI("Video", img)
    model = img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
    if len(model):
        if not pic_name[0].isdigit():
            model = cv2.resize(model, [30, 30])
            print("\n交通标识牌模板尺寸已转换至[30, 30]")
        cv2.imwrite(pic_name, model)
        print(f"\n已保存{pic_name}\n")
        i = i + 1
    return i


i = 1
j = 1
print("\n按n切换种类，按m截取模板，按空格或回车保存，按c取消当前操作，按esc退出")
print(f"\n当前种类为: {model_mapping(i)}\n")

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if ret:
#        img = cv2.flip(img, 1)
        cv2.imshow("Video", img)
        if i < 5:
            model_name = f"{i}{j}.jpg"
        else:
            model_name = f"{model_mapping(i)}.jpg"
        key = cv2.waitKey(25) & 0xFF
        if key == ord('n'):
            i += 1
            if i > 7:
                i = 1
            print(f"\n当前种类为: {model_mapping(i)}\n")
            j = 1
        if key == ord('m'):
            j = get_model(j, model_name, img)
        elif key == 27:
            break

cap.release()
cv2.destroyAllWindows()
