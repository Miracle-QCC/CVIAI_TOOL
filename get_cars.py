import os

import cv2
import scipy.io as scio
import tqdm

root = '/opt/data/cars/devkit'
Data1 = scio.loadmat(root + "/" + 'cars_test_annos.mat')
Data2 = scio.loadmat(root + "/" + 'cars_train_annos.mat')

img_root = '/opt/data/cars/'
ann_test = Data1['annotations']
ann_train = Data2['annotations']

for i in tqdm.tqdm(range(2000)):
    data = ann_test[0][i]
    img_path = img_root + "cars_test/" +  data[4][0]
    img = cv2.imread(img_path)
    H,W = img.shape[:2]
    x1 = data[0][0][0]
    y1 = data[1][0][0]
    x2 = data[2][0][0]
    y2 = data[3][0][0]
    ctx = (float(x1) + float(x2)) / 2
    cty = (float(y1) + float(y2)) / 2
    w = x2 - x1
    h = y2 - y1

    ## 归一化
    ctx = ctx / W
    cty = cty / H

    w = w / W
    h = h / H

    with open('cars_test/' + data[4][0].replace(".jpg", ".txt"), 'w') as f:
        tmp_str = " ".join(list(map(str, [ctx,cty,w,h])))
        f.write("0 " + tmp_str + "\n")

for i in tqdm.tqdm(range(2000)):
    data = ann_train[0][i]
    img_path = img_root + "cars_train/" + data[5][0]
    img = cv2.imread(img_path)
    H, W = img.shape[:2]
    x1 = data[0][0][0]
    y1 = data[1][0][0]
    x2 = data[2][0][0]
    y2 = data[3][0][0]
    ctx = (float(x1) + float(x2)) / 2
    cty = (float(y1) + float(y2)) / 2
    w = x2 - x1
    h = y2 - y1

    ## 归一化
    ctx = float(ctx / W)
    cty = float(cty / H)

    w = float(w / W)
    h = float(h / H)

    with open('cars_train/' + data[5][0].replace(".jpg", ".txt"), 'w') as f:
        tmp_str = " ".join(list(map(str, [ctx, cty, w, h])))
        f.write("0 " + tmp_str + "\n")