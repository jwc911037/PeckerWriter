#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import sqrt,hypot
Slice = 1 #每筆畫精細度設定為10mm
board_len = 1380.
init = np.array([150.,130.])
gname = raw_input('File save:')
gcode = open(gname,'wb')
gcode.write('G1 F500\n')
# print 'G1 F50'
m = np.array([500.,500.])

aa = np.array([0.,0.])
bb = np.array([0.,60.])
cc = np.array([180.,60.])
dd = np.array([180.,0.])
tmp = np.array([0.,0.])


init_pos = Pecker.PosCaculator(init,tmp,board_len)

gcode.write('Z2\n')
Pecker.SliceMove(tmp,m,board_len,init,init_pos,gcode,Slice,True,False)
# Pecker.DoRun(tmp,m,board_len,init_pos,gcode,True,False)
# gcode.write('Z1\n')
aa += m
bb += m
cc += m
dd += m
tmp += m

for i in range(3):
    a = aa + i*np.array([-50.,-50.])
    b = bb + i*np.array([-50.,50.])
    c = cc + i*np.array([50.,50.])
    d = dd + i*np.array([50.,-50.])
    tmp = a
    # print a,b,c,d,a
    # print 'Z2'
    gcode.write('Z2\n')
    # Pecker.SliceMove(tmp,a,board_len,init,init_pos,gcode,Slice,True,False)
    Pecker.DoRun(a,init,board_len,init_pos,gcode,True,False)
    # print 'Z1'
    gcode.write('Z1\n')
    Pecker.SliceMove(a,b,board_len,init,init_pos,gcode,Slice,True,False)
    gcode.write('G4 P0.5\n')
    Pecker.SliceMove(b,c,board_len,init,init_pos,gcode,Slice,True,False)
    gcode.write('G4 P0.5\n')
    Pecker.SliceMove(c,d,board_len,init,init_pos,gcode,Slice,True,False)
    gcode.write('G4 P0.5\n')
    Pecker.SliceMove(d,a,board_len,init,init_pos,gcode,Slice,True,False)
    gcode.write('G4 P0.5\n')
gcode.write('Z2\n')
# gcode.write('X0 Y0\n')
Pecker.SliceMove(a,np.array([0.,0.]),board_len,init,init_pos,gcode,Slice,True,False)
raw_input('Press <Enter> to terminate the prog..')
gcode.close()