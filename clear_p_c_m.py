import os

import tqdm

root = '/opt/data/coco/coco'


train_root = root + "/labels/" + "val2017"
new_train_root = root + "/labels/" + "new_val2017"
files = os.listdir(train_root)
total = 0
p = 0
n_v = 0
v = 0
w = open(os.path.join(root, 'val2017.txt'), 'w')
for fl in tqdm.tqdm(files):
    with open(os.path.join(train_root, fl), 'r') as f:
        lines = f.readlines()
        tmp_str = []
        for line in lines:
            label = line.split()[0]
            if int(label) == 0:
                tmp_str.append(line)
                p += 1
            elif int(label) == 1:
                tmp_str.append(line)
                n_v += 1

            elif int(label) in [2,3,5]:
                data = line.split()
                data[0] = "2"
                tmp_str.append(" ".join(data) + "\n")
                v += 1
    if len(tmp_str) > 0:
        with open(os.path.join(new_train_root,fl), 'w') as f:
            for x in tmp_str:
                f.write(x)
                total += 1
        w.write("./images/val2017/" + fl.replace('txt','jpg') + "\n")
w.close()
print(total)
# print("人：", p)
# print("非", n_v)
# print("机动车", v)
#

