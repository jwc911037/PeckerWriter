#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
from math import *
import serial.tools.list_ports
import serial
import time

def ListPort():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        for port in port_list:
            available_port = port[0]
            print '>>> '+available_port

def OpenPort(port_name, port, baudrate):
    try:
        port_name.port = port
        port_name.baudrate = baudrate
        port_name.timeout = 0.5
        port_name.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+port_name.port

def DoPen(serv,gcode):
    pen = gcode[-1] #抓取Gcode指令內自定義的提放筆的值(Z值)
    serv.write(pen+'\n')
    time.sleep(1)

def DoMove(step,gcode):

    gcode = line.strip() # Strip all EOL characters for consistency
    step.write(gcode+ '\n') # Send g-code block to grbl   
    grbl_out = step.readline() # Wait for grbl response with carriage return
    print 'Sending: '+gcode+' : ' + grbl_out.strip()
        
def PosCaculator(pos,init,l):
    pos[1] = -pos[1] #由下往上畫的座標調整
    #----------計算座標轉換----------#
    actual_pos = pos+init #原座標須加上一開始筆架所在位置
    modified_pos = np.array([0.,0.])
    modified_pos[0] = hypot(actual_pos[0], actual_pos[1]) #sqrt(X**2 + Y**2)
    modified_pos[1] = hypot((l-actual_pos[0]), actual_pos[1]) #sqrt((L-X)**2 + Y**2)
    #----------計算座標轉換----------#
    pos[1] = -pos[1] #計算完畢後恢復原值
    return modified_pos

Slice = 100. #每筆畫精細度設定為10mm
def SliceMove(last,now,Slice):
    V = now-last #求出now,last兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v
        while dis_v > Slice:
            last += slice_v #移動一單位的Slice
            last_move = PosCaculator(last,init,board_len)
            last_move -= init_pos

            dis_v = dis_v - Slice

            step.write('G0 X'+str(last_move[0])+' Y'+str(last_move[1])+'\n')
            # grbl_out = step.readline() # Wait for grbl response with carriage return
            # print 'Go to: ('+str(last[0])+', '+str(last[1])+') : ' + grbl_out.strip()
            # print 'Go to: ('+str(last[0])+', '+str(last[1])+')'
            # print 'G0 X'+str(last_move[0])+' Y'+str(last_move[1])+'\n'
   
if __name__ == '__main__':
    step = serial.Serial()
    serv = serial.Serial()
    ListPort()
    step_port = raw_input('step_port: ')
    # serv_port = raw_input('serv_port: ')

    OpenPort(step,step_port,115200)
    # OpenPort(serv,serv_port,9600)

    step.write("\r\n\r\n")
    #暫停兩秒等待grbl初始化(Grbl 0.9g ['$' for help])
    time.sleep(2)
    #清掉grbl初始化指令
    step.flushInput()

    # board_len = float(raw_input('Length of Board: '))
    # init = np.array(map(float,raw_input('Input Init Pos: ').split()))
    board_len = 1420.
    init = [192.,670.]

    tmp = np.array([0.,0.])
    init_pos = PosCaculator(init,tmp,board_len)
       
    while True:
        try:
            pos = np.array(map(float,raw_input('Input Position:').split()))

            SliceMove(tmp,pos,Slice)    
            pos_move = PosCaculator(pos,init,board_len)
            pos_move -=init_pos

            tmp = pos

            step.write('G0 X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n')
            grbl_out = step.readline() # Wait for grbl response with carriage return
            print 'Go to: ('+str(pos[0])+', '+str(pos[1])+') : ' + grbl_out.strip()
            # print 'G0 X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'
        except Exception:
            step.close()
            break 

        