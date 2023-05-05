"""
清洗标签，去掉带;和超过 cls x y w h的部分,
去掉
    #  3: carplate
    #  7: tricycle
"""

import os
import tqdm



root = '/opt/data/person_vector_non/labels'
def convert_label(data):  # 11 - > 9
    if data[0] in ['4','5','6']:
        data[0] = str(int(data[0]) - 1)
    elif data[0] in ['8','9','10']:
        data[0] = str(int(data[0]) - 2)
    return " ".join(data) + "\n"
def judge(data):
    for x in data:
        if x > 1.0:
            return True
    return False
dirs = os.listdir(root)
for d in dirs:
    if os.path.isfile(root + "/" + d):
        continue
    txts = os.listdir(root + "/" + d)
    if d not in ['videoimg']:
        continue
    for t in tqdm.tqdm(txts):
        tmp_str = []
        with open(root + "/" + d + "/" + t, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = None

            if ";" in line:
                data = line.split(";")
                data = data[0].split()[:5]
            elif "-" in line:
                continue
            else:
                data = line.split()[:5]
                x = list(map(float, data[1:]))
                if judge(x):
                    tmp_str = []
                    break
            if data[0] not in ["3", "7"]:
                tmp_str.append(convert_label(data))

        if len(tmp_str) == 0:
            continue
        else:
            if not os.path.exists(d):
                os.makedirs(d)
            with open(d + "/" + t, 'w') as f:
                for x in tmp_str:
                    f.write(x)














