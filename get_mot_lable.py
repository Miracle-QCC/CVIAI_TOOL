import os

root = '/opt/data/face_landmark/train/mot_blur'
imgs = os.listdir(root)
with open("TXT/mot_blur_label.txt", 'w') as f:
    for im in imgs:
        f.write("mot_blur/" + im + " 2\n")
