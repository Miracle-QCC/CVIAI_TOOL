"""
清洗标签，去掉带;和超过 cls x y w h的部分
"""

import os
import tqdm



root = '/opt/data/person_vector_non/labels'
def convert_label(data):  # 11 - > 8
    ## 最原始的数据需要经过下面处理
    if data[0] in ['4','5','6']:
        data[0] = str(int(data[0]) - 1)
    elif data[0] in ['8']:
        data[0] = str(int(data[0]) - 2)
    elif data[0] in ['10']:
        data[0] = str(int(data[0]) - 3)

    ## 在新的标注中去掉head,rider,rider_with_motor标注
    # if data[0] == '8':
    #     data[0] = str(int(data[0]) - 1)

    return " ".join(data) + "\n"

def fun(d):
    # if d in ['bdd100k_rider', 'cars_test', 'cars_train', 'crowedhumen', 'train2017', 'val2017', 'CarsTest', 'CarsTrain', 'Insight-MVT_Annotation_Test', 'Insight-MVT_Annotation_Train']:
    if d in ['Insight-MVT_Annotation_Test', 'Insight-MVT_Annotation_Train']:
        return
    if os.path.isfile(root + "/" + d):
        return
    txts = os.listdir(root + "/" + d)
    # if d not in ['crowedhumen']:
    #     return
    for t in tqdm.tqdm(txts):
        tmp_str = []

        with open(root + "/" + d + "/" + t, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if ";" in line:
                data = line.split(";")
                data = data[0].split()[:5]
            elif "-" in line:
                continue
            else:
                data = line.split()[:5]
            if data[0] not in ['3',"7","9"]:
                data = convert_label(data)
                # tmp_str.append(convert_label(data))
                data = data.split()
                if data[0] not in ['6', "7", "8"]:
                    tmp_str.append(" ".join(data) + "\n")

            # ## 在新的标注中去掉head,rider,rider_with_motor标注
            # if data[0] not in ['6', "7", "8"]:
            #     tmp_str.append(" ".join(data) + "\n")

            # else:
            #     tmp_str.append(" ".join(data) + "\n")
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















