import cv2
with open("../TXT/new_side_6_18.txt", 'r') as f:
    lines = f.readlines()

root = '/opt/data/face_landmark/train'
f = open('../TXT/new_side_6_18.txt', 'w')
for line in lines:
    img_name = line.split()[0]
    ld = line.split()[1:]
    ld = [float(x) for x in ld]
    img = cv2.imread(root + "/" + img_name)
    h,w = img.shape[:2]
    for i in range(5):
        ld[i*2] = ld[i*2] / w
        ld[i*2+1] = ld[i*2+1] / h

    ld = [str(x) for x in ld]
    f.write(img_name + " " + " ".join(ld) + "\n")