import cv2
import numpy as np
from PIL import Image

def letterbox(img, new_shape=(128, 128), color=(0, 0, 0), auto=True, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 128), np.mod(dh, 128)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)

if __name__ == '__main__':
    img_path = '/opt/data/face_landmark/train/pos/90_5b274c5a5e028a0ffb33121f_1685697208_1271062_0.jpg'
    target = "0.30828366136363633 0.3987091409039548 0.7468555912878788 0.44558077881355934 0.5090721212121212 0.6315631073446327 0.29687356060606057 0.7583568926553673 0.6520285606060606 0.7979001129943503".split()
    target = [float(x) for x in target]
    target = np.array(target)
    img = cv2.imread(img_path)
    img, ratio, (dw,dh) = letterbox(img, new_shape=(128,128),color=(0,0,0))
    if dw:
        x = target[::2]
        x = x * ratio[0] + dw / 128
        y = target[1::2]
    else:
        y = target[1::2]
        y = y * ratio[0] + dh / 128
        x = target[::2]
    h,w = (128,128)
    for i in range(5):
        cv2.circle(img, (int(x[i] * w), int(y[i] * h)), 1, (255, 0, 0), 2)
        cv2.putText(img, str(i), (int(x[i] * w), int(y[i] * h)), 1, 1, (0, 255, 0), 1)

    cv2.imshow("x", img)
    cv2.waitKey(0)
