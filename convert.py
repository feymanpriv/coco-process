# -*- coding: utf-8 -*-
'''

Author: Yangmin
Description: To convert the Logo label file to standard VOC format for detection
'''

import json
import cv2
import numpy as np 
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import time

logo_label_map = {"0001": "BAW", "0002": "Ford", "0003": "SKODA", "0004": "Venucia",
				  "0005": "HONDA", "0006": "NISSAN", "0007": "Cadillac", "0008": "SUZUKI",
				  "0009": "GEELY", "0010": "Porsche", "0011": "jeep", "0012": "PAOJUN",
				  "0013": "ROEWE", "0014": "LINCOLN", "0015": "TOYOTA", "0016": "Buick",
				  "0017": "Chery", "0018": "KIA", "0019": "haval", "0020": "Audi",
				  "0021": "Landrover", "0022": "Volkswagen", "0023": "Trumpchi", "0024": "CHANGAN",
				  "0025": "MorrisGarages", "0026": "Renault SA", "0027": "Lexus", "0028": "BMW",
				  "0029": "MAZDA", "0030": "MercedesBenz"}

def indent(elem, level=0):
	i = "\n" + level * "    "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "    "
		for e in elem:
			# print e
			indent(e, level + 1)
		if not e.tail or not e.tail.strip():
			e.tail = i
	if level and (not elem.tail or not elem.tail.strip()):
		elem.tail = i
	return elem

def get_imInfo(_path):
	img = cv2.imread(_path)
	h, w = img.shape[:2]
	return h, w

def create_xml_head(_info, _folder, _annotation):
	root = ElementTree()
	anno = Element("annotation")
	root._setroot(anno)

	folder = Element("folder", {})
	folder.text = _folder
	anno.append(folder)

	filename = Element("filename", {})
	filename.text = _info['file_name']
	anno.append(filename)

	source = Element("source", {})
	anno.append(source)
	SubElement(source, "database").text = " The BDCI2017-gsum Database"
	SubElement(source, "annotation").text = _annotation
	SubElement(source, "image").text = "flickr"
	SubElement(source, "date_updated").text = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

	size = Element("size", {})
	anno.append(size)
	SubElement(size, "width").text = str(_info['width'])
	SubElement(size, "height").text = str(_info['height'])
	SubElement(size, "depth").text = '3'

	segmented = Element("segmented", {})
	segmented.text = '0'
	anno.append(segmented)

	# indent(anno)
	return anno, root

if __name__ == '__main__':
	data_root = '/Users/yangmin/Database/LOGO/image/'      # path where put the image
	save_root = '/Users/yangmin/Database/LOGO/annotation/' # path to save the generated xml

	with open('/Users/yangmin/Database/train.json', 'r') as f:
		data = json.load(f)
		# print type(data[0]['items'])

	image_info = dict()

	for i in data:
		h, w = get_imInfo(data_root + i['image_id'])
		image_info[i['image_id']] = dict(file_name = i['image_id'],
										 height = h,
										 width = w,
										 instance = []
										)
	for i in data:
		image_id = i['image_id']
		for j in i['items']:
			image_info[image_id]['instance'].append(dict(bbox = j['bbox'],
														 logo_id = j['label_id']
														))

	for i in image_info.keys():
		print i

		logo_xml, logo_root = create_xml_head(image_info[i], 'logo_30_det', 'BDCI2017-gsum')

		for j in image_info[i]['instance']:
			obj = Element("object", {})
			logo_xml.append(obj)
			SubElement(obj, "name").text = logo_label_map[j['logo_id']]
			SubElement(obj, "pose").text = 'Unspecified'
			SubElement(obj, "truncated").text = '0'
			SubElement(obj, "difficult").text = '0'
			bndbox = SubElement(obj, 'bndbox')
			xmin = SubElement(bndbox, 'xmin')
			xmin.text = str(int(j['bbox'][0]))
			ymin = SubElement(bndbox, 'ymin')
			ymin.text = str(int(j['bbox'][1]))
			xmax = SubElement(bndbox, 'xmax')
			xmax.text = str(int(j['bbox'][2]))
			ymax = SubElement(bndbox, 'ymax')
			ymax.text = str(int(j['bbox'][3]))

		indent(logo_xml)
		logo_root.write(save_root + image_info[i]['file_name'].replace('jpg', 'xml'), "utf-8")

