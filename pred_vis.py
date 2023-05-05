import os
import cv2
from tqdm import tqdm

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
root = '/opt/data/person_vector_non'
with open(root + "/" + "yolov8n_nosigmoid_1120.txt", 'r') as f:
    pred_list = f.readlines()
if not os.path.exists("1120"):
    os.makedirs("1120")
def fun(pred_list):
    img = None
    for line in tqdm(pred_list):

        if "#" in line:
            img_name = line.split()[1].split("/")[-1]
            img_path = line.split()[1]
            try:
                if not img:
                    pass
            except:
                cv2.imwrite("1120" + "/" + img_name, img)


            img = cv2.imread(root + "/" + img_path)
        else:
            data = list(map(float,line.split()))
            label = data[0]
            cls = cls_dict[int(label)]
            conf = data[-1]
            if conf < 0.5:
                continue
            x1,y1,x2,y2 = data[1:5]
            color = color_dist[int(label)]
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img, cls, (int(x1), int(y1)), 1, 2, color, 3)
        # d(root + im[1:-1])
        # tmp = im[1:-1].replace("jpg","txt").replace("images","labels")
        # H,W = img.shape[:2]
        # d = im[1:-1].split("/")[-2]
        #
        # if not os.path.exists(d):
        #     os.makedirs(d)
        #     print(d)
        # image_name = im[1:-1].split("/")[-1]
        # if not os.path.exists(root + tmp):
        #     continue
        # with open(root + tmp, 'r') as f:
        #     labels = f.readlines()
        # for label in labels:
        #     label = label.split()
        #     cls = cls_dict[int(label[0])]
        #     ctx,cty,w,h = map(float,label[1:5])
        #     w_ = w * W
        #     h_ = h * H
        #     x1 = ctx * W - 0.5 * w_
        #     y1 = cty * H - 0.5 * h_
        #     x2 = ctx * W + 0.5 * w_
        #     y2 = cty * H + 0.5 * h_
        #     color = color_dist[int(label[0])]
        #     cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        #     cv2.putText(img, cls , (int(x1), int(y1)), 1, 2, color,  3)


if __name__ == '__main__':
    # import threading as th
    # ths = []
    # every_len = len(imgs_lst) // 20
    # # tmp_lst = []
    # # for x in imgs_lst:
    # #     if "bdd" not in x:
    # #         pass
    # #     else:
    # #         # print(x)
    # #         tmp_lst.append(x)
    # # every_len = len(tmp_lst) // 20
    # for i in range(21):
    #     t = th.Thread(target=fun, args=(imgs_lst[i*every_len:(i+1)*every_len], ))
    #     ths.append(t)
    # for t in ths:
    #     t.start()
    # for t in ths:
    #     t.join()

    fun(pred_list)
