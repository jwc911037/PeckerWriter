#!/user/bin env python 
#-*- coding:utf8 -*-
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

# def OpenPort(port_name, port, baudrate):
#     try:
#         port_name.port = port
#         port_name.baudrate = baudrate
#         port_name.timeout = None
#         port_name.write_timeout = None
#         port_name.open()
#     except serial.SerialException:
#         print 'Counld Not Open Port: '+port_name.port

# def WriteMessages(msg,port_name):
#     port_name.write(msg)

def PosCaculator(pos,init,l):
    mpos = pos + init #原座標須加上一開始筆架所在位置
    roll = np.array([0.,0.])
    roll[0] = hypot(mpos[0], mpos[1]) #sqrt(X**2 + Y**2)
    roll[1] = hypot((l-mpos[0]), mpos[1]) #sqrt((L-X)**2 + Y**2)
    return roll

def DoRun(pos,init,l,init_pos):
    roll = PosCaculator(pos,init,l)
    pos_move = roll - init_pos
    gcode_cmd = 'X'+str(pos_move[0])+' Y'+str(pos_move[1])
    # step.write(gcode_cmd)
    # print 'Go to: ('+str(pos[0])+', '+str(pos[1])+')'
    # print gcode_cmd
    return gcode_cmd

Slice = 10. #每筆畫精細度設定為10mm
def SliceMove(a,b,l,init,init_pos,step,Slice):
    RX_BUFFER_SIZE = 128
    l_count = 0
    g_count = 0
    c_line = []

    V = b-a #求出a,b兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v #求出slice vector
        while dis_v > Slice:
            a = a + slice_v #移動一單位的slice vector

            l_count += 1 # Iterate line counter
            l_block = DoRun(a,init,l,init_pos).strip()
            c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
            grbl_out = ''
            while sum(c_line) >= RX_BUFFER_SIZE-1 | step.inWaiting() : #Check receiver buffer of serial
                out_temp = step.readline().strip() # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                    print "  Debug: ",out_temp # Debug response
                else :
                    grbl_out += out_temp;
                    g_count += 1 # Iterate g-code counter
                    grbl_out += str(g_count); # Add line finished indicator
                    del c_line[0] # Delete the block character count corresponding to the last 'ok'
            print 'Go to: ('+str(a[0])+', '+str(a[1])+')'
            print "SND: " + str(l_count) + " : " + l_block,
            step.write(l_block + '\n') # Send g-code block to grbl
            print "BUF:",str(sum(c_line)),"REC:",grbl_out   

            dis_v = dis_v - Slice
        if dis_v > 0: #假設Slice無法完整走完剩下的距離就直接走完
            l_count += 1 # Iterate line counter
            l_block = DoRun(b,init,l,init_pos).strip()
            c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
            grbl_out = ''
            while sum(c_line) >= RX_BUFFER_SIZE-1 | step.inWaiting() : #Check receiver buffer of serial
                out_temp = step.readline().strip() # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                    print "  Debug: ",out_temp # Debug response
                else :
                    grbl_out += out_temp;
                    g_count += 1 # Iterate g-code counter
                    grbl_out += str(g_count); # Add line finished indicator
                    del c_line[0] # Delete the block character count corresponding to the last 'ok'
            print 'Go to: ('+str(b[0])+', '+str(b[1])+')'
            print "SND: " + str(l_count) + " : " + l_block,
            step.write(l_block+'\n')
            print "BUF:",str(sum(c_line)),"REC:",grbl_out
                  
if __name__ == '__main__':
    global step,serv 
    step = serial.Serial()
    serv = serial.Serial()