import os
import  xml.dom.minidom
# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET
from tqdm import tqdm
import cv2
cls_dict = {'car':'0','van':'2',"bus":'1'}
def get_id(id):
    id = int (id)
    if id < 10:
        return '0' * 4 + str(id)
    elif id < 100 :
        return '0' * 3 + str(id)
    elif id < 1000:
        return '0' * 2 + str(id)
    elif id < 10000:
        return '0' * 1 + str(id)
def get_img_name(id):
    name = 'img' + get_id(id)
    return name
cls_set = set()
"""

将DETRAC xml转为txt文件，格式为
    cls ctx cty w h ，并且归一化

"""
rootpath = '/opt/data/trunk/DETRAC-Train-Annotations-XML'
train_root = '/opt/data/person_vector_non/Insight-MVT_Annotation_Train/'
xmls = os.listdir(rootpath)
for x in tqdm(xmls):
    # 使用minidom解析器打开XML文档
    DOMTree = xml.dom.minidom.parse(rootpath + "/" + x)
    root = DOMTree.documentElement
    d = x.replace(".xml", "")
    if not os.path.exists(d):
        os.makedirs(d)
    fs = root.getElementsByTagName('frame')
    for f in fs:
        id = f.getAttribute('num')

        boxes = f.getElementsByTagName('box')
        clss = f.getElementsByTagName('attribute')
        imgname = get_img_name(id) + ".jpg"
        img = cv2.imread(train_root + "/" + d + "/" + imgname)
        txt_name = imgname.replace("jpg",'txt')

        H,W = img.shape[:2]

        tmp_str = []
        for box, cls in zip(boxes, clss):
            left = box.getAttribute('left')
            top = box.getAttribute('top')
            width = box.getAttribute('width')
            height = box.getAttribute('height')
            cls = cls.getAttribute('vehicle_type')
            if cls in ['others']:
                continue
            cls_set.add(cls)
            ctx = (float(left) + float(width) / 2) / W
            cty = (float(top) + float(height) / 2) / H
            width = float(width) / W
            height = float(height) / H

            cls_id = cls_dict[cls]
            tmp_str.append(cls_id + " " + " ".join([str(ctx), str(cty), str(width), str(height)]) + "\n")

        if len(tmp_str) == 0:
            continue
        with open('train/' + d +"/"+ txt_name, 'w') as w:
            for x in tmp_str:
                w.write(x)



rootpath = '/opt/data/trunk/DETRAC-Test-Annotations-XML'
test_root = '/opt/data/person_vector_non/Insight-MVT_Annotation_Test/'
xmls = os.listdir(rootpath)
for x in tqdm(xmls):
    # 使用minidom解析器打开XML文档
    DOMTree = xml.dom.minidom.parse(rootpath + "/" + x)
    root = DOMTree.documentElement
    d = x.replace(".xml", "")
    if not os.path.exists(d):
        os.makedirs(d)
    fs = root.getElementsByTagName('frame')
    for f in fs:
        id = f.getAttribute('num')

        boxes = f.getElementsByTagName('box')
        clss = f.getElementsByTagName('attribute')
        imgname = get_img_name(id) + ".jpg"
        img = cv2.imread(test_root + "/" + d + "/" + imgname)
        txt_name = imgname.replace("jpg",'txt')

        H,W = img.shape[:2]

        tmp_str = []
        for box, cls in zip(boxes, clss):
            left = box.getAttribute('left')
            top = box.getAttribute('top')
            width = box.getAttribute('width')
            height = box.getAttribute('height')
            cls = cls.getAttribute('vehicle_type')
            if cls in ['others']:
                continue
            cls_set.add(cls)
            ctx = (float(left) + float(width) / 2) / W
            cty = (float(top) + float(height) / 2) / H
            width = float(width) / W
            height = float(height) / H

            cls_id = cls_dict[cls]
            tmp_str.append(cls_id + " " + " ".join([str(ctx), str(cty), str(width), str(height)]) + "\n")

        if len(tmp_str) == 0:
            continue
        with open('test/' + d + "/" + txt_name, 'w') as w:
            for x in tmp_str:
                w.write(x)


print(cls_set)
