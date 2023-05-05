import os

root = '/opt/data/person_vector_non/labels/videoimg'

txts = os.listdir(root)
for txt in txts:
    if "16-" in txt:
        with open(root + "/" + txt,'r') as f:
            lines = f.readlines()
        tmp_str = []
        flag = 0
        for line in lines:
            data = line.split()
            if data[0] == '4' and float(data[1]) - 0.2286 < 0.01:
                flag = 1
            else:
                tmp_str.append(line)

        if flag == 1:
            with open(txt, 'w') as f:

                for line in tmp_str:
                    f.write(line)



