
"""
去掉低质量的trunk标签
"""

import os
import tqdm

root = '/opt/data/person_vector_non/labels'

def fun(d):
    if d in ['bdd100k_rider', 'cars_test','cars_train','crowedhumen','train2017','val2017']:
        return
    txts = os.listdir(root + "/" + d)

    for t in tqdm.tqdm(txts):
        tmp_str = []
        with open(root + "/" + d + "/" + t, 'r') as f:
            lines = f.readlines()
        for line in lines:
            data = line.split()
            if '2' == data[0]:
                continue
            else:
                tmp_str.append(line)
        if len(tmp_str) == 0:
            continue
        else:
            if not os.path.exists(d):
                os.makedirs(d)
            with open(d + "/" + t, 'w') as f:
                for x in tmp_str:
                    f.write(x)

if __name__ == '__main__':
    import threading as th

    dirs = os.listdir(root)
    ths = []
    for d in dirs:
        th_ = th.Thread(target=fun, args=(d,))
        ths.append(th_)


    for t in ths:
        t.start()
    for t in ths:
        t.join()















