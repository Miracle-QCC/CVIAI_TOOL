import math

import cv2
import numpy as np

img = cv2.imread("/opt/data/face_landmark/train/side/0_2021991_1685780310_5824685_0.jpg")


def AddHaze1(img):
    img_f = img / 255.0
    (row, col, chs) = img.shape

    A = np.random.uniform(0.2,0.7)  # 亮度
    beta = 0.25 # 雾的浓度
    # math.sqrt()返回数字x的平方根。
    size = math.sqrt(max(row, col))  # 雾化尺寸
    center = (row // 2, col // 2)  # 雾化中心
    for j in range(row):
        for l in range(col):
            d = -0.04 * math.sqrt((j - center[0]) ** 2 + (l - center[1]) ** 2) + size
            td = math.exp(-beta * d)
            img_f[j][l][:] = img_f[j][l][:] * td + A * (1 - td)
    img_f = img_f * 255.0

    return img_f.astype(np.uint8)

img_f = AddHaze1(img )
img_f = img_f.astype(np.uint8)
cv2.imshow("clear", img)
cv2.imshow("fog", img_f)
cv2.waitKey(0)
