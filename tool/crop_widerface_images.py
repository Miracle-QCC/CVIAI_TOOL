import os
import numpy as np
import cv2
from tqdm import tqdm

with open('/opt/data/retinaface/train/labelv2_base.txt', 'r') as f:
    lines = f.readlines()

one = {}
# zero = {}
neg = {}
for line in lines:
    if  "#" in line:
        img_name = line.split()[1]
        one[img_name] = []
        # zero[img_name] = []
        neg[img_name] = []
    else:
        data = line.split()
        bbox = data[:4]
        bbox = [float(x) for x in bbox]
        bbox = [int(x) for x in bbox]
        if bbox[2] - bbox[0] < 32 or bbox[3] - bbox[1] < 32:
            continue
        landmark = data[4:]
        landmark = [float(x) for x in landmark]
        x = landmark[::3]
        y = landmark[1::3]
        label = landmark[2::3]
        label = [int(x) for x in label]
        ld = []
        for i in range(5):
            ld.append(x[i])
            ld.append(y[i])

        if x[0] == -1:
            neg[img_name].append(bbox + ld)
        # elif 0 in label:
        #     zero[img_name].append(bbox + ld)
        else:
            one[img_name].append(bbox + ld)


def expand_crop_img(bbox, img):
    """

    :param bbox: 左上角和右下角坐标
    :param img: 原始图片
    :return:
    """
    h,w = img.shape[:2]
    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]

    ctx = (bbox[0] + bbox[2]) / 2
    cty = (bbox[1] + bbox[3]) / 2

    expand_scale = 0.6
    ## expand
    x1 = ctx - expand_scale * bbox_w
    y1 = cty - expand_scale * bbox_h

    x2 = ctx + expand_scale * bbox_w
    y2 = cty + expand_scale * bbox_h

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(x2, w - 1)
    y2 = min(y2, h - 1)

    new_box = [x1,y1,x2,y2]
    new_box = [int(x) for x in new_box]
    return new_box

def judge_eye_dis(ld, MI = 0.3, MA = 1):
    x1,y1 = ld[:2]
    x2,y2 = ld[2:4]

    dis = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    if MA > dis > MI:
        return True
    else:
        return False

# def judge_eye_dis(ld, dis_conf = 0.3):
#     x1,y1 = ld[:2]
#     x2,y2 = ld[2:4]
#
#     if abs(x1 - x2) < dis_conf:
#         return False
#     return True

def abdon_30(img_name, non):
    for x in non:
        if x == "40--Gymnastics/40_Gymnastics_Gymnastics_40_5.jpg":
            y = 1
        if x in img_name:
            return True
    return False

def crop_img(mps, img_root, save_path, txt_path):
    f = open(txt_path, 'w')
    for img_name in tqdm(mps):
        img = cv2.imread(img_root + "/" + img_name)
        bboxs = mps[img_name]
        idx = 0
        for bbox in bboxs:
            ld = bbox[4:]
            bbox = bbox[:4]
            new_name = img_name.replace("/","_").replace(".jpg", "")
            new_name = new_name + "_" + str(idx) + ".jpg"
            ld = [float(x) for x in ld]
            ld = np.array(ld)
            # h,w = bbox[3] - bbox[1], bbox[2] - bbox[0]
            # ld[::2] = (ld[::2] - bbox[0]) / w
            # ld[1::2] = (ld[1::2] - bbox[1]) / h

            # expand
            new_box = expand_crop_img(bbox, img)
            new_crop_img = img[new_box[1]:new_box[3], new_box[0]:new_box[2], :]
            new_w = new_box[2] - new_box[0]
            new_h = new_box[3] - new_box[1]

            ld[::2] = (ld[::2] - new_box[0]) / new_w
            ld[1::2] = (ld[1::2] - new_box[1]) / new_h
            # ld[::2] = ld[::2] * w / new_w
            # ld[1::2] = ld[1::2] * h / new_h
            ld = list(ld)

            if not judge_eye_dis(ld, MI=0.2, MA=0.35):
                continue


            ld = [str(x) for x in ld]

            # crop_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2],:]
            # cv2.imshow("x", crop_img)


            gray = cv2.cvtColor(new_crop_img, cv2.COLOR_BGR2GRAY)  # 图片的灰度值
            lp_score = cv2.Laplacian(gray,cv2.CV_64F).var()
            if lp_score < 50:
                continue

            # if idx > 1 and "30--Surgeons" not in img_name:
            #     continue
            # cv2.imshow("new", new_crop_img)
            # cv2.waitKey(0)
            try:
                cv2.imwrite(save_path + new_name, new_crop_img)
                f.write(new_name  + " " + " ".join(ld) + "\n")
                idx += 1
            except:
                pass
    f.close()

def crop_img_neg(mps, img_root, save_path, txt_path):
    f = open(txt_path, 'w')
    for img_name in tqdm(mps):
        img = cv2.imread(img_root + "/" + img_name)
        bboxs = mps[img_name]
        idx = 0
        for bbox in bboxs:
            ld = bbox[4:]
            bbox = bbox[:4]
            new_name = img_name.replace("/", "_").replace(".jpg", "")
            new_name = new_name + "_" + str(idx) + ".jpg"
            ld = [float(x) for x in ld]
            ld = np.array(ld)
            h, w = bbox[3] - bbox[1], bbox[2] - bbox[0]
            ld[::2] = (ld[::2] - bbox[0]) / w
            ld[1::2] = (ld[1::2] - bbox[1]) / h
            ld = list(ld)
            if judge_eye_dis(ld,MI=0.25):
                continue
            ld = [str(x) for x in ld]
            crop_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2], :]

            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)  # 图片的灰度值
            lp_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            if lp_score < 20:
                continue

            # if idx > 3:
            #     continue
            cv2.imshow("x", crop_img)
            cv2.waitKey(0)
            try:
                cv2.imwrite(save_path + new_name, crop_img)
                f.write(new_name  + " " + "-1" + "\n")
                idx += 1
            except:
                pass
    f.close()

if __name__ == '__main__':
    img_root = '/opt/data/retinaface/train/images'
    save_path = '../images/expand_widerface_img/'
    txt_path = "../TXT/expand_widerface_img.txt"
    with open("../TXT/retinaface_imgs.txt", 'r') as f:
        lines = f.readlines()
    crop_img(one, img_root, save_path, txt_path)

    # crop_img_neg(one, img_root, "../images/neg_widerface_crop_6_14/", "../TXT/neg_widerface_crop_6_14.txt")