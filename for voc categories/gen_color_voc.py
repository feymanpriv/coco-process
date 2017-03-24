mport cv2
import numpy as np

color_map = {0: [0, 0, 0], 1: [0, 0, 128], 2: [0, 128, 0], 3: [0, 128, 128], 4: [128, 0, 0], 5: [128, 0, 128],
             6: [128, 128, 0], 7: [128, 128, 128], 8: [0, 0, 64], 9: [0, 0, 192], 10: [0, 128, 64],
             11: [0, 128, 192], 12: [128, 0, 64], 13: [128, 0, 192], 14: [128, 128, 64], 15: [128, 128, 192],
             16: [0, 64, 0], 17: [0, 64, 128], 18: [0, 192, 0], 19: [0, 192, 128], 20: [128, 64, 0],
             255: [255, 255, 255]}

sds = []

_label = cv2.imread('voc_mask.png', 0)

_color = np.zeros((_label.shape[0], _label.shape[1], 3))
for i in xrange(_label.shape[0]):
    for j in xrange(_label.shape[1]):
        _color[i][j] = color_map[_label[i][j]]

cv2.imwrite('./voc_mask_color.png', _color)

