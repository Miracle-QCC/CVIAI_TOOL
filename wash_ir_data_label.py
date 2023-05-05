import os
import cv2

root = '/opt/data/ir_data_new/canteen_real'
dirs_lst = ["cluster0207","cluster0208","cluster0209","cluster0210"]
def get_retina_kps(kps):
    tmp_list = []
    i = 0
    for kp in kps:
        i += 1
        tmp_list.append(kp)

        if i % 2 == 0:
            tmp_list.append("0")
    return " ".join(tmp_list)
tmp_dict = {}
files = os.listdir(os.path.join(root,dirs_lst[0]))
gt_txt = 'ir_gt.txt'
for i in range(len(dirs_lst)):
    gt_path = os.path.join(os.path.join(root,dirs_lst[i]), gt_txt)
    with open(gt_path, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        i = 0
        while i < n:
            line = lines[i]
            if line.split(":")[-1][:-1] == "1":
                tmp_dict[line] = {}
                tmp_dict[line]["bbox"] = lines[i+1]
                tmp_dict[line]["kps"] = lines[i+2]
                i += 2
            i += 1
f = open("train_label.txt", 'w')
for key in tmp_dict.keys():
    img_path = key.replace('/home/linaro/eval_datasets/RGB_IR_dataset/', "/opt/data/ir_data_new/")[:-3]
    img = cv2.imread(img_path)
    h,w,c = img.shape
    bbox = tmp_dict[key]["bbox"][:-1]
    kps = tmp_dict[key]['kps'][:-1]
    x = kps.split()[:5]
    y = kps.split()[5:]
    tmp_kps = ""
    for i in range(5):
        tmp_kps += x[i] + " " + y[i] + " "
    tmp_str = key.replace('/home/linaro/eval_datasets/RGB_IR_dataset/', "# ")[:-3]
    tmp_str = tmp_str + " " + str(w) + " " + str(h) +  "\n" +  bbox + " " +  get_retina_kps(tmp_kps.split())
    f.write(tmp_str + "\n")

f.close()


