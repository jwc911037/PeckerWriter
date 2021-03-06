#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *
from Tkinter import StringVar
from PIL import ImageTk, Image
import sys,os
import ttk
import tkFileDialog
import serial
import serial.tools.list_ports
import time
import Pecker
import ContourDetect
import numpy as np
from math import *

#說明書----------------------------------------------------------------------------------------------------#
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 50
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw =Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background='#FFFF93', relief='solid', borderwidth=1,
                       font=("微軟正黑體", "13", "normal"))
        label.pack(ipadx=3)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

#說明書----------------------------------------------------------------------------------------------------#

#主畫面----------------------------------------------------------------------------------------------------#
class GUI(Frame): 
    def __init__(self,master):
        window= Frame(master)
        window.pack()
        window.configure(background='#344253')
        

        self.COM=[]
        self.port_list = list(serial.tools.list_ports.comports())
        if len(self.port_list) <= 0:
            self.COM.append('No Port Available!')
        else:
            for port in self.port_list:
                port_serial = port[0]
                self.COM.append(port_serial)

        #logo
        self.img=ImageTk.PhotoImage(Image.open("UI_img/logo.png"))
        self.logo=Label(window, image=self.img, bg='#344253')
        self.logo.grid(column=0,row=0,columnspan=5,padx=20,pady=10)  
        #frame包canvas
        self.frame=Frame(window,width=700,height=470)
        self.frame.grid(column=1,row=3,columnspan=15,rowspan=20,padx=30,pady=10)
        self.canvas=Canvas(self.frame,width=700,height=470,bg='white',cursor='heart')
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        self.linex=self.canvas.create_line(0,20,700,20, dash=(4, 2),fill='#7B7B7B')
        self.liney=self.canvas.create_line(20,0,20,470, dash=(4, 2),fill='#7B7B7B')
        self.circle=self.canvas.create_oval(10,10,30,30,outline='black',fill='#A9D18F',width=2)
        self.liney2=self.canvas.create_line(680,0,680,470, dash=(4, 2),fill='#7B7B7B')
        self.circle2=self.canvas.create_oval(670,10,690,30,outline='black',fill='#A9D18F',width=2)
        #picture
        self.img3=ImageTk.PhotoImage(Image.open("UI_img/picture.png"))
        self.picture=Button(window, image=self.img3, bg='#344253',command=self.open_img)
        self.picture.grid(column=0,row=1,columnspan=3,padx=20)
        self.button1_ttp = CreateToolTip(self.picture, "請選擇圖片")
        #delete
        self.img4=ImageTk.PhotoImage(Image.open("UI_img/trash.png"))
        self.trash=Button(window, image=self.img4, bg='#344253',command=self.delete_img)
        self.trash.grid(column=13,row=1,columnspan=2,rowspan=2)
        self.button3_ttp = CreateToolTip(self.trash, "刪除圖片")
        #下拉步進馬達com
        self.lab1=Label(window,text='步進馬達com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
        self.lab1.grid(column=16, row=2,rowspan=2)
        self.lab1_ttp = CreateToolTip(self.lab1, "請選擇步進馬達連接埠")

        self.box_value1 = StringVar()
        self.box1 = ttk.Combobox(window, textvariable=self.box_value1,state='readonly',width=10)
        self.box1['values'] = (self.COM) 
        self.box1.bind('<<ComboboxSelected>>',self.Choice)
        self.box1.grid(column=17, row=3,columnspan=2)
        #下拉伺服馬達com
        self.lab2=Label(window,text='伺服馬達com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
        self.lab2.grid(column=16,row=3,rowspan=2,padx=10,pady=50)
        self.lab2_ttp = CreateToolTip(self.lab2, "請選擇伺服馬達連接埠")
        
        self.box_value2 = StringVar()
        self.box2 = ttk.Combobox(window, textvariable=self.box_value2,state='readonly',width=10)
        self.box2['values'] = (self.COM) 
        self.box2.bind('<<ComboboxSelected>>',self.Choice)
        self.box2.grid(column=17, row=3,columnspan=2,rowspan=2,padx=10)
        #connect
        self.img7=ImageTk.PhotoImage(Image.open("UI_img/connect.png"))
        self.connect=Button(window, image=self.img7, bg='#344253',command=self.open)
        self.connect.grid(column=19,row=2,rowspan=2,padx=10,pady=20)
        self.button5_ttp = CreateToolTip(self.connect, "連接")
        #grbl
        self.frame2=Frame(window,width=30,height=14)
        self.frame2.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
        self.t=Text(self.frame2,height=14,width=30, bg='#477979',fg='white',font=('Calibri',14,'bold'),padx=10,pady=5)
        self.t.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
        self.vbar=ttk.Scrollbar(self.frame2,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.t.yview)
        self.t.config(yscrollcommand=self.vbar.set)
        self.t.pack(side=LEFT,expand=True,fill=BOTH)
        self.t_ttp = CreateToolTip(self.t, "圖檔之gcode碼顯示處")

        #send
        self.img8=ImageTk.PhotoImage(Image.open("UI_img/send.png"))
        self.send=Button(window, image=self.img8, bg='#344253')
        self.send.grid(column=15,row=10,columnspan=3)
        self.button6_ttp = CreateToolTip(self.send, "傳送")

        # self.ser = Serial()  
        # self.ser.setPort(self.port) 
    

    def open_img(self):
        global img2,resized
        global photo
        fileName = tkFileDialog.askopenfilename(filetypes = (("JPEG", "*.jpg;*.jpeg"),("PNG", "*.png")))
        original=Image.open(fileName)
        r=float(660)/float(700)
        width=int(original.size[0]*r)
        height=int(original.size[1]*r)
        resized = original.resize((width,height),Image.BILINEAR)
        img2 = ImageTk.PhotoImage(resized)
        photo=self.canvas.create_image(350,235,anchor='center',image=img2)
        # self.canvas.bind("<B1-Motion>", move_image)
        self.canvas.focus_set()
    # def move_image(self,event):
    #     global photo
    #     # 刪除前一步驟圖片位置
    #     self.canvas.delete(photo)
    #     # 新圖片位置
    #     x = event.x
    #     y = event.y
    #     # 新增圖片新的位置
    #     photo = self.canvas.create_image(x, y, image=img2,anchor='center')
    #     self.canvas.update()
    def delete_img(self):
        global photo
        self.canvas.delete(photo)
    def Choice(self,event):
        step_port = self.box_value1.get()
        serv_port = self.box_value2.get()
        list = self.COM
        if step_port in list:  
            self.port1 = step_port
            return self.port1
        if serv_port in list:  
            self.port2 = serv_port
            return self.port2

    def open(self):
        step = serial.Serial(self.port1,115200)
        # serv = serial.Serial(self.port2,9600)
        
        context1 = "print 'hi'"
        n = step.write(context1)  
        output = step.read(n)  
        print output    
        self.t.insert(0.0,output) 

    def close(self):
        self.ser.close()


root = Tk()
root.title('home')
root.resizable(0,0)
root.geometry('1150x630+40+20')
root.configure(background='#344253')
#icon
root.iconbitmap(default='UI_img/icon.ico')
app = GUI(root)  
root.mainloop()  