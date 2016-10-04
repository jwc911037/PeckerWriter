#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import sqrt,hypot
from PIL import Image
Slice = 1 #每筆畫精細度設定為10mm
board_len = 1320.
init = np.array([150.,290.])
tmp = (255,255,255)
zero = np.array([0.,0.])
gname = raw_input('File save:')
gcode = open(gname,'wb')
im = Image.open('test1001.jpg')
init_pos = Pecker.PosCaculator(init,zero,board_len)
gcode.write('G1 F800\n')
for x in range(im.size[0]):
    for y in range(im.size[1]):
        pos = np.array([float(x),float(y)])
        rgb = im.getpixel((x,y))
        if tmp == (255,255,255) and rgb == (0,0,0):
            gcode.write('Z1\n')
        elif tmp == (0,0,0) and rgb == (255,255,255):
            gcode.write('Z2\n')
        Pecker.DoRun(pos,init,board_len,init_pos,gcode,True)
        tmp = rgb
gcode.write('Z2\n')
gcode.write('X0 Y0\n')
raw_input('Press <Enter> to terminate the prog..')
gcode.close()