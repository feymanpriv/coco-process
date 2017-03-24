import numpy as np

f = open('./coco_label_map.txt', 'r')
sourceInLnes = f.readlines()
f.close()

label_list = []
for line in sourceInLnes:
    temp1 = line.strip('\n')
    temp2 = temp1.split(',')
    label_list.append(temp2)
label_map = {}
label_key= []
label_value = []
for list in label_list:
    label_key.append(int(list[0]))
    label_value.append(list[2])
def get_label_map():
    index = 0
    for each_key in label_key:
        label_map[label_key[index]] = label_value[index]
        index  += 1
    return label_map
# get_label_map()
# print label_map
