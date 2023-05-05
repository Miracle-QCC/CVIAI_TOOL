import os
import glob

import tqdm

root = '/opt/data/person_vector_non/labels'
dirs = os.listdir(root)
f = open("val_list.txt", 'w')
for d in tqdm.tqdm(dirs):
    if os.path.isfile(root + "/" + d):
        continue
    if "val" not in d and 'Test' not in d and "VOC" not in d:
        continue
    #     c_dirs = os.listdir(root + "/" + d)
    #     for c_d in c_dirs:
    #         txts = os.listdir(root + "/" + d + "/" + c_d)
    #         for t in txts:
    #             txt_path = "./images/" + d + "/" + c_d + "/" + t.replace("txt", 'jpg')
    #             f.write(txt_path + "\n")

    txts = os.listdir(root + "/" + d)
    # if not os.path.exists(d):
    #     os.makedirs(d)
    for t in txts:
        if d == "crowedhumen":
            d = d + "/images/val"
        txt_path = "./images/" + d + "/" + t.replace("txt", 'jpg')
        f.write(txt_path + "\n")

f.close()

f = open("train_list.txt", 'w')
for d in tqdm.tqdm(dirs):
    if "val" in d or "Test" in d :
        continue
    if os.path.isfile(root + "/" + d):
        continue
    # if d == 'Insight-MVT_Annotation_Train':
    #     c_dirs = os.listdir(root + "/" + d)
    #     for c_d in c_dirs:
    #         txts = os.listdir(root + "/" + d + "/" + c_d)
    #         for t in txts:
    #             txt_path = "./images/" + d + "/" + c_d + "/" + t.replace("txt", 'jpg')
    #             f.write(txt_path + "\n")

    txts = os.listdir(root + "/" + d)
    # if not os.path.exists(d):
    #     os.makedirs(d)
    for t in txts:
        # if d == "crowedhumen":
        #     d = d + "/images/train"
        txt_path = "./images/" + d + "/" + t.replace("txt", 'jpg')
        f.write(txt_path + "\n")














