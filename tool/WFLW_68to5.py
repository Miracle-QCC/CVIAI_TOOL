import os
import cv2
with open("/opt/data/face_landmark/WFLW/test.txt", 'r') as f:
    lines = f.readlines()

f = open("../TXT/WFLW_val_5.txt", 'w')
for line in lines:
    img_name = line.split()[0]
    data = line.split()[1:]
    data = [float(x) for x in data]

    x1 = (data[60*2] + data[64 * 2 + 1]) / 2
    y1 = (data[60 *2 + 1] + data[64*2 + 1]) / 2

    x2 = (data[68 * 2]+ data[72 * 2]) / 2
    y2 = (data[68 * 2 + 1] + data[72 * 2 + 1]) / 2

    x3 = data[54*2]
    y3 = data[54 * 2 + 1]

    x4 = data[88 * 2]
    y4 = data[88 * 2 +1]

    x5 = data[92 * 2 ]
    y5 = data[92 * 2 + 1]


    landmarks = [x1,y1,x2,y2,x3,y3,x4,y4,x5,y5]
    # img = cv2.imread("/opt/data/face_landmark/WFLW/images_test/wflw_test_0001.jpg")
    #
    # # cv2.circle(img, (int(data[60*2] * 256), int(data[60*2+1] * 256)), 1, (255, 0, 0), 2)
    # for i in range(5):
    #     cv2.circle(img, (int(landmarks[i*2] * 256), int(landmarks[i*2+1] * 256)), 1, (255, 0, 0), 2)
    #
    # cv2.imshow("x", img)
    # cv2.waitKey(0)
    landmarks = [str(x) for x in landmarks]
    f.write("WFLW_test/" + img_name + " " + " ".join(landmarks) + "\n")