#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *
from Tkinter import StringVar
from PIL import ImageTk, Image
import sys,os
import ttk
import tkFileDialog
import Pecker
import numpy as np
from math import sqrt,hypot
import ttk
import serial.tools.list_ports
import serial
import time

window = Tk()
window.geometry('500x600')

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

def DoRun(pos,init,l,init_pos,step,write):
    roll = PosCaculator(pos,init,l)
    pos_move = roll - init_pos
    gcode_cmd = 'X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'
    if write is True:
        step.write(gcode_cmd)
    # print 'Go to: ('+str(pos[0])+', '+str(pos[1])+')'
    # print 'SND: '+gcode_cmd
    var1="Go to: ("+str(pos[0])+", "+str(pos[1])+")"+"  "
    var2="SND: "+gcode_cmd
    t.insert('insert',var1)
    t.insert('insert',var2)
    

# Slice = 10. #每筆畫精細度設定為10mm
def SliceMove(a,b,l,init,init_pos,step,Slice,write):
    V = b-a #求出a,b兩點的向量
    dis_v = hypot(V[0],V[1])
    if dis_v != 0: #有移動時
        v = V/dis_v #V的單位向量:v = V/|V|
        slice_v = Slice*v #求出slice vector
        while dis_v > Slice:
            a = a + slice_v #移動一單位的slice vector
            DoRun(a,init,l,init_pos,step,write)
            if write is True:
                msg_bytes = bytearray()
                while True:
                    msg = step.read()
                    if msg == b'\n':
                        print("RCV: " + msg_bytes.decode("utf-8"))
                        break
                    elif msg >= b' ':
                        # drop other control character such as 0xD
                        msg_bytes += msg
            dis_v = dis_v - Slice
        if dis_v > 0: #假設Slice無法完整走完剩下的距離就直接走完
            DoRun(b,init,l,init_pos,step,write)


def connect():
    Slice = 100. #每筆畫精細度設定為10mm
    board_len = float(elen.get())
    init = np.array(map(float,eint.get().split()))
    tmp = np.array([0.,0.])
    init_pos = PosCaculator(init,tmp,board_len)
    # print init_pos
    # t.insert('insert',init_pos)
    
 
    pos = np.array(map(float,epos.get().split()))
    # if len(pos)<1: break #不輸入值直接Enter即可結束程式
    SliceMove(tmp,pos,board_len,init,init_pos,None,Slice,False)    
    tmp = pos
    # raw_input('Finished! Press <Enter> to terminate the programe.')
    # t.delete(2,4)#刪除索引值从10到20之前的值
    epos.delete(0,END)#刪除所有值

COM = []
port_list = list(serial.tools.list_ports.comports())
if len(port_list) <= 0:
    COM.append('No Port Available!')
else:
    for port in port_list:
        port_serial = port[0]
        COM.append(port_serial)

Label(window,text='port : ',font=('Calibri',15,'bold')).pack()
class Application1:

    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly',width=10)
        self.box['values'] = (COM)
        #self.box.current(0)
        self.box.pack()
if __name__ == '__main__':
    app1 = Application1(window)  
# Label(window,text='port : ',font=('Calibri',15,'bold')).pack()
# eport=Entry(window,width=10).pack()
Label(window,text='板長 : ',font=('Calibri',15,'bold')).pack()
elen=Entry(window,width=10)
elen.pack()
Label(window,text='初始位置 : ',font=('Calibri',15,'bold')).pack()
eint=Entry(window,width=10)
eint.pack()
Label(window,text='移動位置 : ',font=('Calibri',15,'bold')).pack()
epos=Entry(window,width=10)
epos.pack()
Button(window,text='connect',command=connect).pack()

frame2=Frame(window,width=500,height=100).pack()
t=Text(frame2,height=100,width=500, bg='white',font=('Calibri',14,'bold'),padx=10,pady=5)
vbar=ttk.Scrollbar(frame2,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=t.yview)
t.config(yscrollcommand=vbar.set)
t.pack(side=LEFT,expand=True,fill=BOTH)

window.mainloop()