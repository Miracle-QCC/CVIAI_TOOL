import os


with open("val_list.txt", 'r') as f:
    lines = f.readlines()
prefix = '/mnt/data/test_data/person_vector_non'

with open("test_yolo.sh", 'w') as f:
    for line in lines:
        print(line)
        f.write(prefix + line[1:])


