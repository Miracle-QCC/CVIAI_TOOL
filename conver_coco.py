import os

import tqdm

root = '/opt/data/person_vector_non/labels'
dirs = os.listdir(root)
tmp_str = []
for d in tqdm.tqdm(dirs):
    if not os.path.exists(d):
        os.makedirs(d)
    txts = os.listdir(root + "/" + d)
    for t in txts:
        if ".git" in d:
            continue
        with open(root + "/" + d + "/" + t, 'r') as f:
            lines = f.readlines()
        with open(d + "/" + t, 'w') as f:
            for line in lines:
                data = line.split()
                if len(data) > 5:
                    tmp_str.append(t)
                    continue
                ctx,cty,w,h = map(float, data[1:])
                x1 = ctx + 0.5 * w
                y1 = cty + 0.5 * h
                data[1] = str(x1)
                data[2] = str(y1)
                data[3] = str(w)
                data[4] = str(h)
                f.write(" ".join(data) + "\n")

x = 1
print(tmp_str)
