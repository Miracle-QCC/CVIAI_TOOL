import os
import cv2


def draw_all_images(img_root, img_list, save_txt, save_img_path):
    """

    :param img_root: 图片的目录
    :param img_list: 存有图片名称的txt文件
    :param save_txt: 保存标注的文件
    :param save_img_path: 保存可视化标注的图片地址   // "../images/6_14_31_crop/"
    :return:
    """

    with open(img_list, 'r') as f:
        lines = f.readlines()
    mp = {}
    f = open(save_txt, 'w')
    for line in lines:
        # print(line)
        img_name = line.split()[0]
        data = line.split()[1:]
        data = [float(x) for x in data]
        mp[img_name] = data
    for key in mp:
        new_name = key.split("/")[-1]
        if not os.path.exists(img_root + "/" + new_name):
            continue
        tmp_data = [str(x) for x in data]
        f.write(save_txt.replace("/")[-1] + "/" + new_name + " " + " ".join(tmp_data) + "\n")

        img = cv2.imread(img_root + "/" + new_name)
        h, w = img.shape[:2]
        points = mp[key]
        for i in range(5):
            cv2.circle(img, (int(points[i * 2] * w), int(points[i * 2 + 1] * h)), 1, (255, 0, 0), 2)
            cv2.putText(img, str(i), (int(points[i * 2] * w), int(points[i * 2 + 1] * h)), 1, 1, (0, 255, 0), 1)
        cv2.imwrite(save_img_path + new_name, img)


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
    return new_box

""" 
指定failcase文件夹，获取failcase标注
xx/yyy.jpg -1
"""
def get_failcase_label(path, save_txt):
    """

    :param path: 图片路径
    :param save_txt: 保存标注的文件夹
    :return:
    """
    imgs = os.listdir(path)
    root = path.replace("/")[-1]
    f = open(save_txt, 'w')
    for img in imgs:
        f.write(root + "/" + img + "\n")

def get_imgs_list_txt(root, save_txt):
    """
    将一个文件夹下所有图片的绝对路径保存到save_txt
    :param root:图片路径
    :param save_txt: 保存位置
    :return:
    """
    imgs = os.listdir(root)
    with open(save_txt, 'w') as f:
        for im in imgs:
            f.write(root + "/" + im + "\n")


if __name__ == '__main__':
    pass