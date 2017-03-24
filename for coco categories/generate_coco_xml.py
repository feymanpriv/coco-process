#coding:utf-8
import sys
import numpy as np
import cv2
import json
from xml.dom import minidom, Node
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from lxml import etree
import load_coco_label_map as load

coco_label_map = load.get_label_map()

#dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation/'
dataDir = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/annotation_val/'

def batch_generate_xml():
    #txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_81_seg/coco_81_train.txt'
    txt_path = '/home/yanglu/Database/MSCOCO/MSCOCO_API/ym/coco/PythonAPI/scripts/code/coco_81_seg/coco_81_val.txt'
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

        labels = []
        points = []
        category_id = []
        list = []
        bbox = []
        boxlist = []
        for ann in img_annotation:
            if 'segmentation' in ann:
                if ann['iscrowd'] == 0:
                    if len(ann['segmentation']) == 1:
                        for seg in ann['segmentation']:
                            points.append(seg)
                            category_id.append(ann['category_id'])
                            bbox.append(ann['bbox'])
                    else:
                        for seg in ann['segmentation']:
                            list = list + seg
                        points.append(list)
                        category_id.append(ann['category_id'])
                        bbox.append(ann['bbox'])

        top = Element('annotation')
        folder = SubElement(top, 'folder')
        folder.text = 'COCO2014'
        filename = SubElement(top, 'filename')
        filename.text = idx+'.jpg'
        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = 'COCO_VAL2014' #修改
        anntation = SubElement(source, 'annotation')
        anntation.text = 'MSCOCO'
        image = SubElement(source, 'image')
        image.text = 'flickr'
        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(img_width)
        height.text = str(img_height)
        depth.text = '3'
        segmented = SubElement(top, 'segmented')
        segmented.text = '0'

        i = 0
        for point in points:
            label = coco_label_map[(category_id[i])]
            x1 = bbox[i][0]
            y1 = bbox[i][1]
            x2 = bbox[i][0] + bbox[i][2]
            y2 = bbox[i][1] + bbox[i][3]
            bndbox = {'xmin': int(x1), 'ymin': int(y1), 'xmax': int(x2), 'ymax': int(y2)}
            bndbox['name'] = label
            boxlist.append(bndbox)
            i += 1

        for each_object in boxlist:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = str(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

        save_file = open('./coco_81_det/val2014/'+idx+'.xml', 'w')
        rough_string = ElementTree.tostring(top, 'utf8')
        reparsed = minidom.parseString(rough_string)
        save_file.write(reparsed.toprettyxml(indent="\t"))

if __name__ == '__main__':
    batch_generate_xml()