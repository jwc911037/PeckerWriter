#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *  
from serial import * 
import serial.tools.list_ports 
import ttk  
import numpy as np

class GUI(Frame): 
	def __init__(self,master):
		frame = Frame(master)
		frame.pack()

		self.port = 0
		self.baudrate = 115200  
		#serial port
		self.lab1 = Label(frame,text='port : ',font=('Calibri',15,'bold'))
		self.lab1.grid(row = 0,column = 0)

		self.box_value = StringVar()
		self.box = ttk.Combobox(frame, textvariable=self.box_value,state='readonly',width=10)
		self.box['values'] = ('COM1','COM2','COM3','COM4') 
		self.box.bind('<<ComboboxSelected>>',self.Choice)
		self.box.grid(row = 0,column = 1)
		#板長
		self.lab2 = Label(frame,text='板長 : ',font=('Calibri',15,'bold'))
		self.lab2.grid(row = 1,column = 0)

		self.elen = Entry(frame,width=10)
		self.elen.grid(row = 1,column = 1)
		#初始位置
		self.lab3 = Label(frame,text='初始位置 : ',font=('Calibri',15,'bold'))
		self.lab3.grid(row = 2,column = 0)

		self.eint = Entry(frame,width=10)
		self.eint.grid(row = 2,column = 1)
		#open serial
		self.button1 = Button(frame,text='connect',command=self.open)
		self.button1.grid(row = 3,column = 0)
		#close serial
		self.button2 = Button(frame,text='close port',command=self.close)
		self.button2.grid(row = 3,column = 1)
		#移動位置
		self.lab3 = Label(frame,text='移動位置 : ',font=('Calibri',15,'bold'))
		self.lab3.grid(row = 4,column = 0)

		self.epos = Entry(frame,width=10)
		self.epos.grid(row = 4,column = 1)
		#move
		self.button3 = Button(frame,text='move')
		self.button3.grid(row = 5,column = 0,columnspan=2)
		#show
		self.show = Text(frame,width = 70,height = 50,wrap = WORD)
		self.show.grid(row = 6,column = 0,columnspan=2,rowspan = 4)

		self.ser = Serial()  
		self.ser.setPort(self.port) 
		tmp = np.array([0.,0.])
		step = self.ser

	def Choice(self,event):
		context = self.box_value.get()
		list = ["COM1",'COM2','COM3','COM4']
		if context in list:  
			self.port = list.index(context)
			self.ser.setPort(self.port)
			self.ser.setBaudrate(self.baudrate)

	def open(self):
		self.ser.open()
		context1 = "print 'hi'"
		n = self.ser.write(context1)  
		output = self.ser.read(n)  
		print output    
		self.show.insert(0.0,output) 

	def close(self):
		self.ser.close()

	def PosCaculator(pos,init,l):
		mpos = pos + init #原座標須加上一開始筆架所在位置
		roll = np.array([0.,0.])
		roll[0] = round(hypot(mpos[0], mpos[1]),2) #sqrt(X**2 + Y**2)
		roll[1] = round(hypot((l-mpos[0]), mpos[1]),2) #sqrt((L-X)**2 + Y**2)
		return roll

	def DoRun(self,pos,init,l,init_pos,step,write):
		roll = PosCaculator(pos,init,l)
		pos_move = roll - init_pos
		gcode_cmd = 'X'+str(pos_move[0])+' Y'+str(pos_move[1])+'\n'
		if write is True:
				step.write(gcode_cmd)
		var1="Go to: ("+str(pos[0])+", "+str(pos[1])+")"+"  "
		var2="SND: "+gcode_cmd
		self.show.insert('insert',var1)
		self.show.insert('insert',var2)

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
				DoRun(self,b,init,l,init_pos,step,write)

	def move(self):
		global tmp
		step = self.ser
		Slice = 100. #每筆畫精細度設定為10mm
		board_len = float(self.elen.get())
		init = np.array(map(float,self.eint.get().split()))
		init_pos = PosCaculator(init,tmp,board_len)
		pos = np.array(map(float,self.epos.get().split()))
		# if len(pos)<1: break #不輸入值直接Enter即可結束程式
		SliceMove(tmp,pos,board_len,init,init_pos,step,Slice,True)
		tmp = pos
		# raw_input('Finished! Press <Enter> to terminate the programe.')
		# t.delete(2,4)#刪除索引值从10到20之前的值
		self.epos.delete(0,END)#刪除所有值


root = Tk()  
root.title("simple_test")  
root.geometry('500x600')
app = GUI(root)  
root.mainloop()  


