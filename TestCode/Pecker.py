#!/user/bin env python 
#-*- coding:utf8 -*-
# CHANGE LOG:
# 2016.09.21-更改35,36行，將轉換後的數值四捨五入至小數點第二位(e.g. round(num,2))
# 2016.09.22-新增DoRun、SliceMove一個Input參數write，如果是False就只印出結果
# 2016.10.04-新增DoRun、SliceMove一個Input參數read，因此可用在SendGcode(read = True)
# 及寫入檔案中(read = False)
import numpy as np
from math import sqrt,hypot
import serial.tools.list_ports
import serial
import time

def ListPort():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        for port in port_list:
            available_port = port[0]
            print '>>> '+available_port
    else: print 'No available port.'

def OpenPort(port_name,port,baudrate):
    try:
        port_name.port = port
        port_name.baudrate = baudrate
        port_name.timeout = None
        port_name.write_timeout = None
        port_name.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+port_name.port

# def WriteMessages(msg,port_name):
#     port_name.write(msg)

def PosCaculator(pos,init,l):
    mpos = pos + init #原座標須加上一開始筆架所在位置
    roll = np.array([0.,0.])
    roll[0] = round(hypot(mpos[0], mpos[1]),2) #sqrt(X**2 + Y**2)
    roll[1] = round(hypot((l-mpos[0]), mpos[1]),2) #sqrt((L-X)**2 + Y**2)
    return roll

def DoRun(pos,init,l,init_pos,step,write,read):
    roll = PosCaculator(pos,init,l)
    pos_move = roll - init_pos
    gcode_cmd = 'X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'
    if write is True:
        step.write(gcode_cmd)
        # 如果只是純粹把gcode_cmd寫入檔案裡不需要回傳訊息，傳送serial時則需要等待回傳再繼續避免漏傳
        if read is True:
            grbl_out = step.readline()
            print gcode_cmd.strip() + ':' + grbl_out.strip()

def SliceMove(a,b,l,init,init_pos,step,Slice,write,read):
    V = b-a #求出a,b兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v #求出slice vector
        while dis_v > Slice:
            a = a + slice_v #移動一單位的slice vector
            DoRun(a,init,l,init_pos,step,write,read)
            dis_v = dis_v - Slice
        if dis_v >= 0: #假設Slice無法完整走完剩下的距離就直接走完
            DoRun(b,init,l,init_pos,step,write,read)