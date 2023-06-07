import cv2
import numpy as np

img = cv2.imread("/opt/data/face_landmark/train/side/SZ6420_1685797688_482442_0.jpg")
h,w = img.shape[:2]

points = "0.12466229890789474 0.3646078017475728 0.5100111710526316 0.39162800611650483 0.12375961842105263 0.546100427184466 0.09113311842105262 0.720803932038835 0.42773256578947366 0.7471188349514563".split()
points = [float(x) for x in points]
def letter_bbox(img, target_size=128):
    np_img = np.array(img)
    h,w = np_img.shape[:2]
    im_ratio = h / w
    if im_ratio > 1:
        new_h = target_size
        new_w = int(new_h / im_ratio)

    else:
        new_w = target_size
        new_h = int(new_w * im_ratio)

    np_img = cv2.resize(np_img, (new_w, new_h))
    det_img = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    det_img[:new_h, :new_w, :] = np_img

    return det_img
# 87.54153442382812 129.66238403320312 355.5540771484375 492.317626953125 157.18161010742188 247.5338897705078 286.86907958984375 253.90589904785156 218.35882568359375 337.43963623046875 167.34255981445312 399.81768798828125 267.37640380859375 405.1838684082031
# landmarks =list(map(int, list(map(float,"157.18161010742188 247.5338897705078 286.86907958984375 253.90589904785156 218.35882568359375 337.43963623046875 167.34255981445312 399.81768798828125 267.37640380859375 405.1838684082031".split()))))

# cv2.rectangle(img, (572,248), (598,266), [255,255,0], 2)
img = letter_bbox(img)
for i in range(5):
    cv2.circle(img, (int(points[i*2]*128), int(points[i*2+1]*128)), 1, (255, 0, 0), 2)
    cv2.putText(img, str(i), (int(points[i*2]*128), int(points[i*2+1]*128)), 1, 2, (0, 255, 0), 1)



cv2.imshow("x", img)
cv2.waitKey(0)




# 0 0.8509 0.8972 0.1207 0.1981
# 4 0.2286 0.1282 0.0177 0.0565