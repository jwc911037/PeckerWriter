#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import sqrt,hypot
Slice = 10. #每筆畫精細度設定為10mm
board_len = 1320.
init = np.array([150.,290.])
# gname = raw_input('File save:')
# gcode = open(gname,'wb')
# gcode.write('G1 F50')\
print 'G1 F50'
a = np.array([0.,0.])
b = np.array([0.,600.])
c = np.array([900.,600.])
d = np.array([900.,0.])

tmp = np.array([0.,0.])
init_pos = Pecker.PosCaculator(init,tmp,board_len)


for i in range(2):
    a += i*np.array([10.,10.])
    b += i*np.array([10.,-10.])
    c += i*np.array([-10.,-10.])
    d += i*np.array([-10.,10.])
    # print a,b,c,d,a
    Pecker.SliceMove(tmp,a,board_len,init,init_pos,None,Slice,False)
    Pecker.SliceMove(a,b,board_len,init,init_pos,None,Slice,False)
    Pecker.SliceMove(b,c,board_len,init,init_pos,None,Slice,False)
    Pecker.SliceMove(c,d,board_len,init,init_pos,None,Slice,False)
    Pecker.SliceMove(d,a,board_len,init,init_pos,None,Slice,False)

raw_input('Finished! Press <Enter> to terminate the program.')
# gcode.close()