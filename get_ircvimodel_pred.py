import os

root = '/home/qcj/workcode/sdk_package_2x/install/soc_cv1821_wevb_0005b_64mb_spinor/tpu_32/cvitek_ai_sdk/bin/out_txt'
txts = os.listdir(root)
with open("test_list2.txt", 'r') as f:
    lines = f.readlines()
    ls = {}
    for line in lines:
        ls[line.replace("/","_").replace("jpg","txt")[:-1]] = 1

for t in txts:
    if t not in ls:
        continue
    with open(root + "/" + t, 'r') as f:
        lines = f.readlines()
        w = open("cvimodel_pred/" + t, 'w')

        for line in lines:
            data = line.split()[:5]
            data[0],data[1:5] = data[4], data[0:4]
            w.write("face " + " ".join(data) + "\n")
        w.close()


