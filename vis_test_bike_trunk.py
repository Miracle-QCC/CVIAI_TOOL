import os

import tqdm

with open("/opt/data/person_vector_non/train_list.txt", 'r') as f:
    lines = f.readlines()


root = '/opt/data/person_vector_non'
cls_dict = {
    0: 'car',
    1: 'bus',
    2: 'truck',
    3: 'pedestrian',
    4: 'bike',
    5: 'motor',
    6: 'rider',
    7: 'head',
    8: 'rider_with_motor',
}
color_dist = {
    0: (0,127,0),
    1: (0,255,0),
    2: (127,0,0),
    3: (255,0,0),
    4: (0,0,127),
    5: (0,0,255),
    6: (127,127,0),
    7: (0,127,127),
    8: (127,127,127),
}
bikes = 0
trunks = 0
for line in tqdm.tqdm(lines):
    path = root + line[1:].replace("images", "labels").replace(".jpg",'.txt')[:-1]
    with open(path, 'r') as f:
        datas = f.readlines()
        tmp_str = []
        for data in datas:
            tmp = data.split()
            label = tmp[0]
            if label in ['2', '4']:
                tmp_str.append(data)
        if len(tmp_str) == 0:
            continue
        else:
            import cv2
            img = cv2.imread(root + line[1:][:-1])
            H,W = img.shape[:2]
            for x in tmp_str:
                label, ctx,cty,w,h = map(float, x.split())

                w = w * W
                h = h * H
                x1 = ctx * W - 0.5 * w
                y1 = cty * H - 0.5 * h

                x2 = ctx * W + 0.5 * w
                y2 = cty * H + 0.5 * h
                color = color_dist[int(label)]
                cls = cls_dict[int(label)]
                if cls == "bike":
                    bikes += 1
                else:
                    trunks += 1
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(img, cls, (int(x1), int(y1)), 1, 2, color, 3)

            cv2.imwrite("train_out/" + line.split("/")[-1][:-1],img)
print("bikes :", bikes)
print("trunks:", trunks)
