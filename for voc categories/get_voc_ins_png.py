#coding:utf-8
import sys
import numpy as np
import cv2
import json
from collections import OrderedDict
from pprint import pprint
import load_coco_label_map as load

dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation/'
#dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation_val/'

coco_label_map = load.get_label_map()
voc_label_map = {1:'aeroplane', 2:'bicycle', 3:'bird', 4:'boat',5: 'bottle',6: 'bus', 7:'car',8: 'cat',
              9:'chair',10: 'cow',11: 'diningtable',12: 'dog',13: 'horse',14: 'motorbike',15: 'person',
              16:'pottedtable',17: 'sheep',18: 'sofa',19: 'train',20: 'tvmonitor',21: 'ignore' }

def isIn(value):
    for v in voc_label_map.itervalues():
        if v == value:
            return True
    return False



def batch_get_mask():
    txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_21_seg/coco_21_train.txt'
    #txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_21_seg/coco_21_val.txt'
    coco_train_list = []

    f = open(txt_path, 'r')
    for i in f:
        coco_train_list.append(i.strip())

    for idx in coco_train_list:
        print idx

        annotation_file = dataDir + idx + '.json'
        annotation_set = json.load(open(annotation_file, 'r'))
        img_annotation = annotation_set['annotation']
        img_info = annotation_set['image']
        img_height = img_info['height']
        img_width = img_info['width']

        points = []
        category_id = []
        list = []

        for ann in img_annotation:
            if 'segmentation' in ann:
                if ann['iscrowd'] == 0:
                    if len(ann['segmentation']) == 1:
                        for seg in ann['segmentation']:
                            points.append(seg)
                            category_id.append(ann['category_id'])
                    else:
                        for seg in ann['segmentation']:
                            list = list + seg
                        points.append(list)
                        category_id.append(ann['category_id'])

        labels = []
        npoints= []
        j = 0
        for id in category_id:
            value = coco_label_map.get(category_id[j])
            if isIn(value):
                for key,value2 in voc_label_map.items():
                    if value2 ==value:
                        labels.append(key)
                        npoints.append(points[j])
            j += 1

        nlabels = []
        i = 1
        for point in npoints:
            nlabels.append(i)
            i += 1

        _mask = get_mask(img_height, img_width, npoints, labels)
        cv2.imwrite('/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_21_ins/train2014/' + idx + '.png',_mask)  #修改文件名

def get_mask(img_height,img_width,npoints, nlabels):
    mask = np.zeros((img_height, img_width, 1), np.uint8)
    index = 0
    for point in npoints:
        color = nlabels[index]
        point = npoints[index]
        point = np.asarray(point, 'int32')
        _shape = np.reshape(point, (len(point) / 2, 2))
        index += 1
        cv2.fillConvexPoly(mask, _shape, color)
    return mask

if __name__ == '__main__':
    batch_get_mask()

