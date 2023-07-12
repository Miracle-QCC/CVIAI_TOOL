import os

import cv2

img_root = '/opt/data/face_landmark/face_keypoint_5/face_roi'

with open("/opt/data/face_landmark/face_keypoint_5/landmark/landmark_20230612.txt", 'r') as f:
    lines = f.readlines()
mp = {}
for line in lines:
    # print(line)
    img_name = line.split()[0]
    data = line.split()[1:]
    data = [float(x) for x in data]
    mp[img_name] = data
f = open("../TXT/norm_benchmark_label.txt", 'w')
for key in mp:
    new_name = key.replace("/", "_")
    if not os.path.exists(img_root + "/" + key):
        continue
    img = cv2.imread(img_root + "/" + key)
    h,w = img.shape[:2]
    points = mp[key]
    data = []
    for i in range(5):
        data.append(points[i*2] / w)
        data.append(points[i*2+1] / h)

    data = [str(x) for x in data]
    f.write(key + " " + " ".join(data) + "\n")

        # cv2.circle(img, (int(points[i * 2] * w), int(points[i * 2 + 1] * h)), 1, (255, 0, 0), 2)
        # cv2.putText(img, str(i), (int(points[i * 2] * w), int(points[i * 2 + 1] * h)), 1, 1, (0, 255, 0), 1)
    # cv2.imwrite("../images/face_benchmark/" + new_name, img)