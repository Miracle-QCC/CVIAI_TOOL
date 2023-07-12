import random
import cv2
import numpy as np

def random_crop(img, target,):
    """

    :param img: np格式的图片
    :param target: 归一化的坐标
    :param ratio: 随机crop的比例
    :return:
    """
    ratio = random.uniform(0.7, 0.9)
    rescale_ratio = ratio / 2
    number = random.uniform(0,1)
    target = np.array(target)
    if number < 0.5:
        return img,target

    h, w = img.shape[:2]

    ctx = (0 + w) / 2
    cty = (0 + h) / 2


    # center point move
    new_ctx = ctx * random.uniform(0.90, 1.10)
    new_cty = cty * random.uniform(0.90, 1.10)

    ## random crop
    x1 = new_ctx - rescale_ratio * w
    y1 = new_cty - rescale_ratio * h

    x2 = new_ctx + rescale_ratio * w
    y2 = new_cty + rescale_ratio * h

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(x2, w - 1)
    y2 = min(y2, h - 1)

    new_w = x2 - x1
    new_h = y2 - y1

    x1 = int(x1)
    y1 = int(y1)

    x2 = int(x2)
    y2 = int(y2)
    # return to the original val
    target[::2] = target[::2] * w
    target[1::2] = target[1::2] * h
    print(new_h, new_w)
    new_traget = target.copy()
    new_traget[::2] = (target[::2] - x1) / new_w
    new_traget[1::2] = (target[1::2] - y1) / new_h

    crop_img = img[y1:y2, x1:x2,:]


    # for i in range(5):
    #     cv2.circle(crop_img, (int(new_traget[i * 2] * new_w), int(new_traget[i * 2 + 1] * new_h)), 1, (255, 0, 0), 2)
    #     cv2.putText(crop_img, str(i), (int(new_traget[i * 2] * new_w), int(new_traget[i * 2 + 1] * new_h)), 1, 1, (0, 255, 0), 1)
    #
    # cv2.imshow("x", crop_img)
    # cv2.waitKey(0)
    return crop_img,new_traget

if __name__ == '__main__':


    img = cv2.imread("../images/expand_widerface_img/59--people--driving--car_59_peopledrivingcar_peopledrivingcar_59_567_0.jpg")

    points = "0.43616389548693585 0.3341340879120879 0.46778619952494066 0.5486945274725274 0.15157247030878856 0.4950549450549451 0.14630401425178138 0.8851648351648351 0.19900477434679345 0.9631868131868132".split()
    points = [float(x) for x in points]
    crop_img,new_traget = random_crop(img, points)
    h, w = crop_img.shape[:2]
    for i in range(5):
        cv2.circle(crop_img, (int(new_traget[i * 2] * w), int(new_traget[i * 2 + 1] * h)), 1, (255, 0, 0), 2)
        cv2.putText(crop_img, str(i), (int(new_traget[i * 2] * w), int(new_traget[i * 2 + 1] * h)), 1, 1, (0, 255, 0), 1)

    cv2.imshow("x", crop_img)
    cv2.waitKey(0)
