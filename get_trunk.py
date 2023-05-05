import os
import glob

import cv2
import tqdm

root = '/opt/data/person_vector_non/labels'
img_root = '/opt/data/person_vector_non/'
dirs = os.listdir(root)
imgs = 0
labels = 0
for d in tqdm.tqdm(dirs):
    txts = os.listdir(root + "/" + d)
    if d == "crowedhumen":
        continue
    if not os.path.exists(d):
        os.makedirs(d)

    for t in txts:
        img_path = "images/" + d + "/" + t.replace("txt", 'jpg')
        txt_path = "/" + d + "/" + t
        with open(root + txt_path, 'r') as f:
            lines = f.readlines()
        tmp_str = []
        for line in lines:
            data = line.split()
            if data[0] == "2":
                tmp_str.append(line)
                labels += 1
        if len(tmp_str) == 0:
            continue
        else:
            img = cv2.imread(img_root + img_path)
            imgs += 1
            for x in tmp_str:
                _,ctx,cty,w,h = map(float,x.split())
                H,W = img.shape[:2]
                w = W * w
                h = H * h

                x1 = int(ctx * W - 0.5 * w)
                y1 = int(cty * H - 0.5 * h)

                x2 = int(x1 + w)
                y2 = int(y1 + h)
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), [0,255,0], 2)

            cv2.imwrite(d + "/" + t.replace("txt", 'jpg'), img)



print("labels:",labels)
print("imgs:",imgs)