#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
from math import *
import serial.tools.list_ports
import serial

def ListPort():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        for port in port_list:
            available_port = port[0]
            print available_port
        
def PosCaculator(pos,init,l):
    pos[1] = -pos[1] #從底下畫圖的座標調整
    #----------計算座標轉換----------#
    actual_pos = pos+init #原座標須加上一開始筆架所在位置
    modified_pos = np.array([0.,0.])
    modified_pos[0] = hypot(actual_pos[0], actual_pos[1]) #sqrt(X**2 + Y**2)
    modified_pos[1] = hypot((l-actual_pos[0]), actual_pos[1]) #sqrt((L-X)**2 + Y**2)
    #----------計算座標轉換----------#
    pos[1] = -pos[1] #計算完畢後恢復原值
    return modified_pos

def SliceMove(last,now,Slice):
    V = now-last #求出now,last兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v
        while dis_v > Slice:
            last = last + slice_v #移動一單位的Slice
            last_move = PosCaculator(last,init,board_len)
            last_move -= init_pos
            dis_v = dis_v - Slice

            print 'Go to: ('+str(last[0])+', '+str(last[1])+')'
            print 'G0 X'+str(last_move[0])+' Y'+str(last_move[1])+'\n'
    
Slice = 10. #每筆畫精細度設定為10mm

board_len = float(raw_input('Length of Board: '))
init = np.array(map(float,raw_input('Input Init Pos: ').split()))

tmp = np.array([0.,0.])
init_pos = PosCaculator(init,tmp,board_len)
# print init_pos
while True:
    pos = np.array(map(float,raw_input('Input Position:').split()))

    SliceMove(tmp,pos,Slice)    
    pos_move = PosCaculator(pos,init,board_len)
    pos_move -=init_pos
    tmp = pos

    print 'Go to: ('+str(pos[0])+', '+str(pos[1])+')'
    print 'G0 X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'

    
