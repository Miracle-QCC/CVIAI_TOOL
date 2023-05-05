"""
清洗标签，去掉带;和超过 cls x y w h的部分,
去掉
    #  3: carplate
    #  7: tricycle
"""

import os
import tqdm


def judge(data):
    for x in data:
        if x > 1.0:
            return True
    return False
root = '/opt/data/person_vector_non/labels'


dirs = os.listdir(root)
for d in dirs:
    if os.path.isfile(root + "/" + d):
        continue
    txts = os.listdir(root + "/" + d)
    if d not in ['crowedhumen']:
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
                else:
                    tmp_str.append(" ".join(data) + "\n")
        if len(tmp_str) == 0:
            continue
        else:
            if not os.path.exists(d):
                os.makedirs(d)
            with open(d + "/" + t, 'w') as f:
                for x in tmp_str:
                    f.write(x)














