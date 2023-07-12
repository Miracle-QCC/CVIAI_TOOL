import os
import glob
import json

# 从json中获得五个关键点的坐标
# 标注json时，需要按照左眼、右眼、鼻子、左嘴和右嘴的顺序
# 每个文件表示一张人脸
from tqdm import tqdm


def get_5_points_json(json_path):
    js_ls = glob.glob(json_path + "/*json")
    landmarks = {}
    for js_p in js_ls:
        with open(js_p,'r') as f:
            data = json.load(f)
            # img_name = js_p.split("/")[-2] + "/" +  js_p.split("/")[-1].replace("json",'jpg')
            img_name = data['imagePath']

            landmarks[img_name] = []
            for p in data['shapes']:
                points = p['points'][0]
                landmarks[img_name] += points
    return landmarks




if __name__ == '__main__':
    root = "/opt/data/face_landmark/train/add_pos"
    pre_dir = root.split("/")[-1]
    landmarks = get_5_points_json(root)
    f = open("../TXT/add_pos.txt", 'w')
    for key in tqdm(landmarks):
        ld_str = [str(x) for x in landmarks[key]]
        f.write(pre_dir + "/" + key + " " + " ".join(ld_str) + "\n")

    f.close()