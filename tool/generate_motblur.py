import os
import random
from glob import glob

import cv2
from letter_box import letterbox
from tqdm import tqdm
import numpy as np
import albumentations as A
def motion_blur(image, degree=12, angle=45):
  image = np.array(image)
  # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
  M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
  motion_blur_kernel = np.diag(np.ones(degree))
  motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
  motion_blur_kernel = motion_blur_kernel / degree
  blurred = cv2.filter2D(image, -1, motion_blur_kernel)
  # convert to uint8
  cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
  blurred = np.array(blurred, dtype=np.uint8)
  return blurred


# 添加椒盐噪声
def add_salt_pepper_noise(image, prob):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

root = '/opt/data/face_landmark/train/WFLW'
imgs = glob(root + "/*jpg")
imgs += glob('/opt/data/face_landmark/train/neg_others/*jpg')
imgs += glob("/opt/data/face_landmark/train/expand_widerface_img/*jpg")
imgs += glob("/opt/data/face_landmark/train/neg_side_back/*jpg")


resize_size = 72
for im in tqdm(imgs):
    img = cv2.imread(im)
    resize_img = cv2.resize(img, (32,32))
    resize_img = cv2.resize(resize_img, (64,64))
    T = A.Compose([
    A.GaussianBlur(p=1.0,blur_limit=(3,5)),
    A.MultiplicativeNoise(p=1.0),
    A.RandomBrightnessContrast(p=1.0),
    A.ISONoise(p=1.0),
    # A.HueSaturationValue(val_shift_limit=20,p=1.0),
    A.GaussNoise(p=1.0,var_limit=(30.0, 50.0)),
    A.MotionBlur(p=1.0, blur_limit=(9, 15))]
    )
    # base,_,_ = letterbox(img,new_shape=(resize_size, resize_size), color=(114,114,114))
    # base = cv2.GaussianBlur(base, (3, 3),3)
    # mean = np.mean(resize_img)
    # x = random.randint(2,8)
    # blur1 = base[x:x+64,x:x+64,:]
    # y =  random.randint(2,8)
    # blur2 = base[8-y:resize_size-y,8-y:resize_size-y,:]
    #
    # if abs(np.mean(blur1) - mean) > 50 or abs(np.mean(blur2) - mean) > 50:
    #     continue
    #
    # res_img = resize_img * 0.4 + blur1 * 0.3 + blur2 * 0.3
    # degree = random.randint(1,5)
    # res_img = motion_blur(resize_img, degree=10)
    # res_img = add_salt_pepper_noise(res_img, prob=0.002)

    res_img = T(image = resize_img)['image']
    # cv2.waitKey(0)
    cv2.imwrite('../mot_blur/' + im.split("/")[-1], res_img)

