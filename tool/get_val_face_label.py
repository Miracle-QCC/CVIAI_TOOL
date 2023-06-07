import os



drs = os.listdir("/opt/data/face_landmark/val")
f = open("../TXT/face_val_label.txt", 'w')
for dr in drs:
    if os.path.isfile("/opt/data/face_landmark/val/" + dr):
        continue
    imgs = os.listdir("/opt/data/face_landmark/val/" + dr)
    for im in imgs:

        if dr == "pos":

            f.write(dr + "/" + im + " 1\n")
        else:
            f.write(dr + "/" + im + " 0\n")