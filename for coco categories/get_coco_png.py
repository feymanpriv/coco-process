#coding:utf-8
import sys
import numpy as np
import cv2
import json
from collections import OrderedDict
from pprint import pprint

dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation/'
#dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation_val/'
def batch_get_mask():
    txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/coco_train2014.txt'
    #txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/coco_val2014.txt'
    coco_train_list = []

    f = open(txt_path, 'r')
    for i in f:
        coco_train_list.append(i.strip())

    coco_81_list = []
    for idx in coco_train_list:
        print idx

        annotation_file = dataDir + idx + '.json'
        annotation_set = json.load(open(annotation_file, 'r'))
        img_annotation = annotation_set['annotation']
        img_info = annotation_set['image']
        img_height = img_info['height']
        img_width = img_info['width']
        points = []
        labels = []
        list = []

        for ann in img_annotation:
            if 'segmentation' in ann:
                if ann['iscrowd'] == 0:
                    if len(ann['segmentation']) == 1:
                        for seg in ann['segmentation']:
                            points.append(seg)
                            labels.append(ann['category_id'])
                    else:
                        for seg in ann['segmentation']:
                            list = list + seg
                        points.append(list)
                        labels.append(ann['category_id'])

        _mask = get_mask(img_height,img_width,points,labels)
        cv2.imwrite('/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_81_seg/train2014/' + idx +'.png',_mask) #修改文件夹名称
        coco_81_list.append(idx)
    # print len(coco_81_list)
    f2 = open('./coco_81_seg/coco_81_train.txt', 'w')  #修改文件名
    f2.write("\n".join(coco_81_list))

def get_mask(img_height,img_width,points,labels):
    mask = np.zeros((img_height, img_width, 1), np.uint8)
    if labels:
        index = 0
        for label in labels:
            color = labels[index]
            point = points[index]
            point = np.asarray(point, 'int32')
            _shape = np.reshape(point, (len(point) / 2, 2))
            index += 1
            cv2.fillConvexPoly(mask, _shape, color)
    return mask

if __name__ == '__main__':
    batch_get_mask()



