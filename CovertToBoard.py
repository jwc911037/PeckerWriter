#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
from math import sqrt,hypot,sin,cos,pi
import numpy as np
import re
# =====初始設定=====
Slice = 1 #每筆畫精細度設定為10mm
board_len = 1284.
init = np.array([100.,590.])
tmp = np.array([0.,0.])
init_pos = Pecker.PosCaculator(init,tmp,board_len)
# =================
# =====位移以及大小設定=====
m = np.array([50.,50.])
scale = 1.
# =========================
fname = raw_input('Enter:')
fhand = open('gcode/Unajusted/'+fname)
oname = raw_input('Output:')
gcode = open('gcode/'+oname, 'wb')
for line in fhand:
    l = line.strip()
    pos = re.findall('X(\S+).Y(\S+)', l)
    if l.startswith('G1'):
        # print 'G1 F500'
        gcode.write('G1 F1000\n')
    elif l.startswith('Z'):
        # print l
        if l == 'Z up':
            gcode.write('Z2\n')
            # print 'Z2'
        elif l == 'Z down':
            gcode.write('Z1\n')
            # print 'Z1'
    elif len(pos) > 0:
        x = float(pos[0][0])
        y = float(pos[0][1])
        axis = np.array([x,y])
        axis = scale*axis + m
        Pecker.SliceMove(tmp,axis,board_len,init,init_pos,gcode,Slice,True,False)
        tmp = axis
        # print axis
    elif l.startswith(';'): continue
# gcode.write('Z2\n')
# gcode.write('X0 Y0\n')
Pecker.SliceMove(tmp,np.array([0.,0.]),board_len,init,init_pos,gcode,Slice,True,False)
raw_input('Press <Enter> to terminate the prog..')
fhand.close()
gcode.close()