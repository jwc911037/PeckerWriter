#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import numpy as np
from math import *
import serial.tools.list_ports
import serial
import time

step = serial.Serial()

Pecker.ListPort()
step_port = raw_input('step_port: ')

Pecker.OpenPort(step,step_port,115200)

step.write("\r\n\r\n")
time.sleep(2)
step.flushInput()

# board_len = float(raw_input('Length of Board: '))
# init = np.array(map(float,raw_input('Input Init Pos: ').split()))
board_len = 975.
init = np.array([75.,440.])
Slice = 1.
tmp = np.array([0.,0.])
init_pos = Pecker.PosCaculator(init,tmp,board_len)

step.write('G1 F500\n')
while True:
    pos = np.array(map(float,raw_input('Input Position:').split()))
    if len(pos)<1: break #不輸入值直接Enter即可結束程式
    Pecker.SliceMove(tmp,pos,board_len,init,init_pos,step,Slice,True,True)    
    tmp = pos   
step.close()  