import json
import os

from tqdm import tqdm

root = '/opt/data/freqs/consumer_counting_anno'
drs = os.listdir(root)
num_mp = {}
for dr in tqdm(drs):
    jsons = os.listdir(root + "/" + dr)
    jsons.sort()
    f1 = open("../TXT/" + dr + ".txt", "w")
    for js in jsons:
        js_p = root + "/" + dr + "/" + js
        new_txt = js.replace("json", "txt")
        frame = js.replace(".json", '')
        frame_id = int(frame)
        num = 0
        with open(js_p, 'r') as f:
            data = json.load(f)
            for p in data['shapes']:
                if p['label'] != 'person':
                    continue
                num += 1
        f1.write(frame + " " + str(num) + "\n")

    f.close()

