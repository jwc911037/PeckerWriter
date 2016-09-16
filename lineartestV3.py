#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
from math import *

def PosCaculator(pos,init,l):
    mpos = pos+init #原座標須加上一開始筆架所在位置
    roll = np.array([0.,0.])
    roll[0] = hypot(mpos[0], mpos[1]) #sqrt(X**2 + Y**2)
    roll[1] = hypot((l-mpos[0]), mpos[1]) #sqrt((L-X)**2 + Y**2)
    return roll

def DoRun(pos,init,l,init_pos):
    roll = PosCaculator(pos,init,l)
    pos_move = roll - init_pos
    gcode_cmd = 'X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'
    # gcode.write(gcode_cmd)
    print 'Go to: ('+str(pos[0])+', '+str(pos[1])+')'
    print gcode_cmd

Slice = 10. #每筆畫精細度設定為10mm
def SliceMove(a,b,l,init,init_pos,Slice):
    V = b-a #求出a,b兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v #求出slice vector
        while dis_v > Slice:
            a = a + slice_v #移動一單位的slice vector
            DoRun(a,init,l,init_pos)
            dis_v = dis_v - Slice
        if dis_v > 0: #假設Slice無法完整走完剩下的距離就直接走完
            DoRun(b,init,l,init_pos)

if __name__ == '__main__':    
    board_len = float(raw_input('Length of Board: '))
    init = np.array(map(float,raw_input('Input Init Pos: ').split()))

    tmp = np.array([0.,0.])
    init_pos = PosCaculator(init,tmp,board_len)
    # print init_pos
    while True:
        try:
            pos = np.array(map(float,raw_input('Input Position:').split()))
            SliceMove(tmp,pos,board_len,init,init_pos,Slice)    
            tmp = pos
        except Exception:
            print 'Test End!'
            raise