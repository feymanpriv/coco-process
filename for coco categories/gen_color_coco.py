import cv2
import numpy as np
import scipy.io

data = scipy.io.loadmat('color150.mat')
# print data['colors']
colors = data['colors']
# print colors[0]
color_map = {}
index = 0
for i in range(0,81):
    color_map[index] = colors[index]
    index += 1

_label = cv2.imread('mask_back.png', 0)
_color = np.zeros((_label.shape[0], _label.shape[1], 3))
for i in xrange(_label.shape[0]):
        for j in xrange(_label.shape[1]):
            _color[i][j] = color_map[_label[i][j]]

cv2.imwrite('mask_color.png',_color)
# print color_map

