with open("../TXT/norm_label.txt", 'r') as f:
    lines = f.readlines()

f = open("../TXT/norm_label_v2.txt", 'w')

for line in lines:
    if "side" in line:
        continue
    f.write(line)

