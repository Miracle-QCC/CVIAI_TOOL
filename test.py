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

s = set()
cls_dict = {"bus":'1', 'bicycle':'4','motorbike':'5','person':'3'}

# 使用minidom解析器打开XML文档
tree = ET.ElementTree(file = '/home/qcj/workcode/tool/2007_001284.xml')
# DOMTree = xml.dom.minidom.parse(rootpath + "/" + x)
# root = DOMTree.documentElement
root = tree.getroot()
W = root.find('size').find('width').text
H = root.find('size').find('height').text

box = root.findall('object').find('bndbox')
x1 = box.find('xmin').text
x2 = box.find('xmax').text

y1 = box.find('ymin').text
y2 = box.find('ymax').text

ctx = str(((float(x1) + float(x2)) / 2 ) / float(W))
cty = str(((float(y1) + float(y2)) / 2) / float(H))
width = str((float(x2) - float(x1)) / float(W))
height = str((float(y2) - float(y1)) / float(H))
cls = cls_dict[root.find('object').find('name').text]



print(s)
