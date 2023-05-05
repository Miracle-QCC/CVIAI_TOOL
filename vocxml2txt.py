import os
# import  xml.dom.minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from tqdm import tqdm
"""

将voc xml转为txt文件，格式为
    cls ctx cty w h ，并且归一化

"""
rootpath = '/opt/data/person_vector_non/VOCdevkit/VOC2012/Annotations'
import cv2
train_root = '/opt/data/person_vector_non/VOCdevkit/VOC2012/JPEGImages'

cls_set = set()
xmls = os.listdir(rootpath)
s = set()
cls_dict = {"bus":'1', 'bicycle':'4','motorbike':'5','person':'3'}
for x in tqdm(xmls):
    # 使用minidom解析器打开XML文档
    tree = ET.ElementTree(file = rootpath + "/" + x)
    # DOMTree = xml.dom.minidom.parse(rootpath + "/" + x)
    # root = DOMTree.documentElement
    root = tree.getroot()
    W = root.find('size').find('width').text
    H = root.find('size').find('height').text
    objs = root.findall('object')
    tmp_lst = []
    for obj in objs:
        if obj.find('name').text not in ['motorbike','person','bus','bicycle']:
            continue
        box = obj.find('bndbox')
        x1 = box.find('xmin').text
        x2 = box.find('xmax').text

        y1 = box.find('ymin').text
        y2 = box.find('ymax').text

        ctx = str(((float(x1) + float(x2)) / 2 ) / float(W))
        cty = str(((float(y1) + float(y2)) / 2) / float(H))
        width = str((float(x2) - float(x1)) / float(W))
        height = str((float(y2) - float(y1)) / float(H))
        cls = cls_dict[obj.find('name').text]
        tmp_lst.append(cls + " " + " ".join([ctx,cty,width,height]) + "\n")
    if len(tmp_lst) == 0:
        continue
    else:
        with open('VOC2012/' + x.replace('xml', 'txt'), 'w') as w:
            for x in tmp_lst:
                w.write(x)
    #     for c_tag in tag:
    #         x = 1
    # size = root.getElementsByTagName('size')[0]
    # boxs = root.getElementsByTagName('object')[0].getElementsByTagName('part')
    # W = size.getAttribute('width')
    # H = size.getAttribute('height')
    # for f in fs:
    #     boxes = f.getElementsByTagName('box')
    #     clss = f.getElementsByTagName('attribute')
    #     imgname = x.replace(".xml", 'jpg')
    #     txt_name = imgname.replace("jpg",'txt')
    #
    #     with open("VOC2012" +"/"+ txt_name, 'w') as w:
    #         for box,cls in zip(boxes,clss):
    #             left = box.getAttribute('left')
    #             top = box.getAttribute('top')
    #             width = box.getAttribute('width')
    #             height = box.getAttribute('height')rootpath + "/" + x
    #             cls = cls.getAttribute('vehicle_type')
    #             cls_set.add(cls)
    #             ctx = (float(left) + float(width) / 2) / W
    #             cty = (float(top) + float(height) / 2) / H
    #             width = float(width) / W
    #             height = float(height) / H
    #
    #             w.write(cls + " " + " ".join([str(ctx), str(cty), str(width),str(height)]) + "\n")


print(s)
