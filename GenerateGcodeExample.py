#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import sqrt,hypot

Slice = 10. #每筆畫精細度設定為10mm

if __name__ == '__main__':    
    board_len = float(raw_input('Length of Board: '))
    init = np.array(map(float,raw_input('Input Init Pos: ').split()))
    gname = raw_input('File save:')
    gcode = open(gname,'wb')
    gcode.write('G1 F50')

    tmp = np.array([0.,0.])
    init_pos = Pecker.PosCaculator(init,tmp,board_len)
    # print init_pos
    while True:
        pos = np.array(map(float,raw_input('Input Position:').split()))
        if len(pos)<1: break #不輸入值直接Enter即可結束程式
        Pecker.SliceMove(tmp,pos,board_len,init,init_pos,gcode,Slice,True)    
        tmp = pos
    raw_input('Finished! Press <Enter> to terminate the program.')
    gcode.close()
