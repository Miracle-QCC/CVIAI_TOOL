import csv
tmp_str = []
with open('/opt/data/face_landmark/new_face_data_clean_all/landmark_new.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f, skipinitialspace=True):
        tmp = ['new_side_6_18/' + row['name']]
        # print(row
        #       )
        for i in range(1,11):
            tmp.append(row[str(i)])
        tmp_str.append(tmp)

f = open("../TXT/new_side_6_18.txt", 'w')
for x in tmp_str:
    f.write(" ".join(x) + "\n")
