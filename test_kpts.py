import os
import numpy as np

keys = os.listdir("0.5_out_txt")
# label_lst = os.listdir("label")

def bbox_overlaps(boxes, query_boxes):
    n_ = boxes.shape[0]
    k_ = query_boxes.shape[0]
    overlaps = np.zeros((n_, k_), dtype=np.float)
    for k in range(k_):
        query_box_area = (query_boxes[k, 2] - query_boxes[k, 0] +
                          1) * (query_boxes[k, 3] - query_boxes[k, 1] + 1)
        for n in range(n_):
            iw = min(boxes[n, 2], query_boxes[k, 2]) - max(
                boxes[n, 0], query_boxes[k, 0]) + 1
            if iw > 0:
                ih = min(boxes[n, 3], query_boxes[k, 3]) - max(
                    boxes[n, 1], query_boxes[k, 1]) + 1
                if ih > 0:
                    box_area = (boxes[n, 2] - boxes[n, 0] +
                                1) * (boxes[n, 3] - boxes[n, 1] + 1)
                    all_area = float(box_area + query_box_area - iw * ih)
                    overlaps[n, k] = iw * ih / all_area
    return overlaps

def bbox_overlap(a, b):
    x1 = np.maximum(a[:,0], b[0])
    y1 = np.maximum(a[:,1], b[1])
    x2 = np.minimum(a[:,2], b[2])
    y2 = np.minimum(a[:,3], b[3])
    w = x2-x1+1
    h = y2-y1+1
    inter = w*h
    aarea = (a[:,2]-a[:,0]+1) * (a[:,3]-a[:,1]+1)
    barea = (b[2]-b[0]+1) * (b[3]-b[1]+1)
    o = inter / (aarea+barea-inter + 1e-2)
    o[w<=0] = 0
    o[h<=0] = 0
    return o

def com_loss(kps1, kps2, w, h):
    kps1 = np.array(kps1)
    kps2 = np.array(kps2)
    w_ = (kps1[::2] - kps2[::2]) / w
    h_ = (kps1[1::2] - kps2[1::2]) / h
    loss = np.sqrt(w_ ** 2 + h_ ** 2)
    loss = sum(loss) / 5.0
    return loss

def com_kps_loss(bbox1, bbox2):
    ious = bbox_overlaps(bbox1,bbox2)
    loss = 0.0
    count = 0.0
    for i in range(bbox1.shape[0]):
        idx = np.argmax(ious[i],0)
        if ious[i][idx] < 0.5:
            continue
        w = bbox2[idx][2] - bbox2[idx][0]
        h = bbox2[idx][3] - bbox2[idx][1]
        loss += com_loss(bbox1[i][4:], bbox2[idx][5:], w, h)
        count += 1

    loss /= count
    return loss


def string2np(bboxs):
    tmp_np = []
    for bbox in bboxs:
        tmp_np.append(list(map(float, bbox.split())))
    return np.array(tmp_np)

count = 0
loss = 0.0
for key in keys:
    try:
        with open("0.5_out_txt/" + key, 'r') as f1:
            with open("label/" + key, 'r') as f2:
                preds = f1.readlines()
                labels = f2.readlines()
                if len(preds) == 0 or len(labels) == 0:
                    continue
                preds_np = string2np(preds)
                labels_np = string2np(labels)
                loss += com_kps_loss(preds_np, labels_np)
                count += 1
    except:
        pass
print(count)
print(loss)
print(loss / count)
