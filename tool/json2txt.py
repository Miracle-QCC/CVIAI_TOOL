import json
import os

from tqdm import tqdm

root = '/opt/data/head_track/xq/bmalgo_eval/chefhat'
drs = os.listdir(root)
tracks = {}
for dr in tqdm(drs):
    jsons = os.listdir(root + "/" + dr)
    jsons.sort()
    if not os.path.exists("../head_track/" + dr + "/gt"):
        os.makedirs("../head_track/" + dr + "/gt")

    for js in jsons:
        js_p = root + "/" + dr + "/" + js
        new_txt = js.replace("json", "txt")
        frame = js.replace(".json", '')
        frame_id = int(frame)
        with open(js_p,'r') as f:
            data = json.load(f)
            for p in data['shapes']:
                if p['label'] != 'head':
                    continue
                w,h = p['points'][1][0] - p['points'][0][0],p['points'][1][1] - p['points'][0][1]
                if "../head_track/" + dr + "/gt/gt.txt" not in tracks:
                    tracks["../head_track/" + dr + "/gt/gt.txt"] = []
                tracks["../head_track/" + dr + "/gt/gt.txt"].append([frame_id,p['group_id']] + p['points'][0] + [w,h] + [1,-1,-1,-1])

for key in tqdm(tracks):
    with open(key, 'w') as f:
        datas = tracks[key]
        for data in datas:
            data = [str(x) for x in data]
            f.write(",".join(data) + "\n")