#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import sqrt,hypot
Slice = 1 #每筆畫精細度設定為10mm
board_len = 1320.
init = np.array([150.,290.])
gname = raw_input('File save:')
gcode = open(gname,'wb')
gcode.write('G1 F50\n')
# print 'G1 F50'
a = np.array([0.,0.])
b = np.array([0.,400.])
c = np.array([400.,400.])
d = np.array([400.,0.])

tmp = np.array([0.,0.])
init_pos = Pecker.PosCaculator(init,tmp,board_len)


for i in range(15):
    a += np.array([10.,10.])
    b += np.array([10.,-10.])
    c += np.array([-10.,-10.])
    d += np.array([-10.,10.])
    # print a,b,c,d,a
    # print 'Z2'
    gcode.write('Z2\n')
    Pecker.SliceMove(tmp,a,board_len,init,init_pos,gcode,Slice,True)
    # print 'Z1'
    gcode.write('Z1\n')
    Pecker.SliceMove(a,b,board_len,init,init_pos,gcode,Slice,True)
    Pecker.SliceMove(b,c,board_len,init,init_pos,gcode,Slice,True)
    Pecker.SliceMove(c,d,board_len,init,init_pos,gcode,Slice,True)
    Pecker.SliceMove(d,a,board_len,init,init_pos,gcode,Slice,True)
gcode.write('Z2\n')
gcode.write('X0 Y0\n')
raw_input('Finished! Press <Enter> to terminate the program.')
gcode.close()