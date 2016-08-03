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
from math import sqrt

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
window = Tk()
window.title('home')
window.resizable(0,0)
window.geometry('1150x650+200+100')
window.configure(background='#344253')
#icon
window.iconbitmap(default='UI_img/icon.ico')
#logo
img=ImageTk.PhotoImage(Image.open("UI_img/logo.png"))
logo=Label(window, image=img, bg='#344253')
logo.grid(column=0,row=0,columnspan=5,padx=20,pady=10)
#question
#img1=ImageTk.PhotoImage(Image.open("UI_img/question.png"))
#question=Button(window, image=img1, bg='#344253')
#question.grid(column=19,row=0,columnspan=2)

#frame包canvas
frame=Frame(window,width=700,height=470)
frame.grid(column=1,row=3,columnspan=15,rowspan=20,padx=30,pady=10)
#canvas=Canvas(window,width=700,height=470,bg='white')
canvas=Canvas(frame,width=700,height=470,bg='white',cursor='heart',scrollregion=(0,0,1000,1000))
canvas.grid(column=1,row=3,columnspan=15,rowspan=20,padx=30,pady=10)
hbar=ttk.Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=ttk.Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=700,height=470)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
canvas_ttp = CreateToolTip(frame, "編輯圖片 : 可任意擺放圖片位置、調整圖片大小與旋轉圖片")

def open_img():
    global img2
    global photo
    fileName = tkFileDialog.askopenfilename(filetypes = (("JPEG", "*.jpg;*.jpeg"),("PNG", "*.png"),("GIF", "*.gif")))
    original=Image.open(fileName)
    width=500
    r=float(width)/original.size[0]
    height=int(original.size[1]*r)
    resized = original.resize((width,height),Image.BILINEAR)
    img2 = ImageTk.PhotoImage(resized)
    photo=canvas.create_image(20,20,anchor='nw',image=img2)
    canvas.bind("<B1-Motion>", move_image)
def move_image(event):
    global photo
    # 刪除前一步驟圖片位置
    canvas.delete(photo)
    # 新圖片位置
    x = event.x
    y = event.y
    # 新增圖片新的位置
    photo = canvas.create_image(x, y, image=img2,anchor='center')
    canvas.update()

#picture
img3=ImageTk.PhotoImage(Image.open("UI_img/picture.png"))
picture=Button(window, image=img3, bg='#344253',command=open_img)
picture.grid(column=0,row=1,columnspan=3,padx=20)
button1_ttp = CreateToolTip(picture, "請選擇圖片")
#before_step
img4=ImageTk.PhotoImage(Image.open("UI_img/before_step.png"))
before_step=Button(window, image=img4, bg='#344253')
before_step.grid(column=12,row=1,columnspan=2,rowspan=2)
button2_ttp = CreateToolTip(before_step, "上一步")
#next_step
img5=ImageTk.PhotoImage(Image.open("UI_img/next_step.png"))
next_step=Button(window, image=img5, bg='#344253')
next_step.grid(column=13,row=1,columnspan=2,rowspan=2)
button3_ttp = CreateToolTip(next_step, "下一步")

#設定畫面----------------------------------------------------------------------------------------------------#
def setup_window():
    window_setup=Toplevel(window)
    window_setup.title('Setup')
    window_setup.geometry('470x500+500+200')
    window_setup.resizable(0,0)
    window_setup.configure(background='#344253')

    def colse_setup():
        window_setup.destroy()
    
    img11=ImageTk.PhotoImage(Image.open("UI_img/setup.png"))
    setup2=Label(window_setup, image=img11, bg='#344253')
    setup2.image=img11
    setup2.grid(row=0,column=0,columnspan=20,padx=20,pady=10)
    #size
    Label(window_setup,text='size',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=1,column=0,columnspan=2)
    #weight
    lab1=Label(window_setup,text='width',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold'))
    lab1.grid(row=1,column=3)
    lab1_ttp = CreateToolTip(lab1, "請輸入板子寬度")
    e=Entry(window_setup,width=10).grid(row=1,column=4,padx=20)
    #mm
    Label(window_setup,text='mm',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=1,column=5)
    #height
    lab2=Label(window_setup,text='height',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold'))
    lab2.grid(row=2,column=3)
    lab2_ttp = CreateToolTip(lab2, "請輸入板子長度")
    e=Entry(window_setup,width=10).grid(row=2,column=4,padx=20)
    #mm
    Label(window_setup,text='mm',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=2,column=5)
    #常用板子大小
    img12=ImageTk.PhotoImage(Image.open("UI_img/size.png"))
    size=Button(window_setup, image=img12, bg='#344253')
    size.image=img12
    size.grid(row=3,column=1,columnspan=3,pady=10)
    button1_ttp = CreateToolTip(size, "選擇常用大小")
    #確認鍵
    img13=ImageTk.PhotoImage(Image.open("UI_img/ok.png"))
    ok=Button(window_setup, image=img13, bg='#344253',command=colse_setup)
    ok.image=img13
    ok.grid(row=3,column=4,columnspan=2,pady=10)
    button2_ttp = CreateToolTip(ok, "確認")
    #?
    #img14=ImageTk.PhotoImage(Image.open("UI_img/question.png"))
    #question=Button(window_setup, image=img14, bg='#344253')
    #question.image=img14
    #question.grid(row=3,column=6,pady=10)
    #illustration
    Label(window_setup,text='illustration',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold'),width=10,height=1).grid(row=4,column=0,columnspan=2,pady=10,padx=40)
    img15=ImageTk.PhotoImage(Image.open("UI_img/illus.png"))
    illus=Label(window_setup, image=img15, bg='#344253')
    illus.image=img15
    illus.grid(row=5,column=0,columnspan=20)
    lab3_ttp = CreateToolTip(illus, "寬、高示意圖")
#設定畫面----------------------------------------------------------------------------------------------------#

#setup
img6=ImageTk.PhotoImage(Image.open("UI_img/setup_logo.png"))
setup=Button(window, image=img6, bg='#344253',command=setup_window)
setup.grid(column=14,row=1,columnspan=2,rowspan=2)
button4_ttp = CreateToolTip(setup, "設定")

#-----------輸入需要連接的藍芽/Serial Port----------#
#顯示所有目前可用的port
COM = []
port_list = list(serial.tools.list_ports.comports())
if len(port_list) <= 0:
    COM.append('No Port Available!')
else:
    for port in port_list:
        port_serial = port[0]
        COM.append(port_serial)
#下拉選藍芽com
lab1=Label(window,text='藍芽com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
lab1.grid(column=16, row=2,rowspan=2)
lab1_ttp = CreateToolTip(lab1, "請選擇藍芽連接埠")
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
        self.box.grid(column=17, row=3,columnspan=2)

#下拉選步進馬達com
lab2=Label(window,text='步進馬達com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
lab2.grid(column=16,row=3,rowspan=2,padx=10,pady=50)
lab2_ttp = CreateToolTip(lab2, "請選擇步進馬達連接埠")
class Application2:

    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly',width=10)
        self.box['values'] = (COM)
        #self.box.current(0)
        self.box.grid(column=17, row=3,columnspan=2,rowspan=2,padx=10)

if __name__ == '__main__':
    app1 = Application1(window)    
    app2 = Application2(window)
#-----------輸入需要連接的藍芽/Serial Port----------#
#connect
def insert_grbl():
    var="Grbl 0.9i ['$' for help"
    t.insert('insert',var)

img7=ImageTk.PhotoImage(Image.open("UI_img/connect.png"))
connect=Button(window, image=img7, bg='#344253',command=insert_grbl)
connect.grid(column=19,row=2,rowspan=2,padx=10,pady=20)
button5_ttp = CreateToolTip(connect, "連接")
#grbl
frame2=Frame(window,width=30,height=14)
frame2.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
t=Text(frame2,height=14,width=30, bg='#477979',fg='white',font=('Calibri',14,'bold'),padx=10,pady=5)
t.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
vbar=ttk.Scrollbar(frame2,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
t.config(yscrollcommand=vbar.set)
t.pack(side=LEFT,expand=True,fill=BOTH)
t_ttp = CreateToolTip(t, "圖檔之gcode碼顯示處")

#墨水量確定/輸出畫面----------------------------------------------------------------------------------------------------#
def send_window():
    window_send=Toplevel(window)
    window_send.title('send')
    window_send.geometry('300x200+600+300')
    window_send.resizable(0,0)
    window_send.configure(background='#344253')
    
    def colse_send():
        window_send.destroy()
    def output():
        window.withdraw()
        window_send.destroy()
        output=Toplevel(window)
        output.title('output')
        output.resizable(0,0)
        output.geometry('1150x630+200+100')
        output.configure(background='#344253')

        #logo
        img=ImageTk.PhotoImage(Image.open("UI_img/logo.png"))
        logo=Label(output, image=img, bg='#344253')
        logo.image=img
        logo.grid(column=0,row=0,columnspan=5,padx=20,pady=10)
        #question
        #img1=ImageTk.PhotoImage(Image.open("UI_img/question.png"))
        #question=Button(output, image=img1, bg='#344253')
        #question.image=img1
        #question.grid(column=19,row=0,columnspan=2)
        #canvas
        canvas=Canvas(output,width=700,height=470,bg='white')
        canvas.grid(column=1,row=3,columnspan=15,rowspan=20,padx=30,pady=10)
        #progressbar
        progress = ttk.Progressbar(output, orient="horizontal",length=700, mode="determinate")
        progress.grid(column=1,row=10,columnspan=15,rowspan=20,padx=30,pady=10)
        progress.start(100)
        progress_ttp = CreateToolTip(progress, "圖檔輸出的進度顯示")
        #picture
        img3=ImageTk.PhotoImage(Image.open("UI_img/picture2.png"))
        picture=Label(output, image=img3, bg='#344253')
        picture.image=img3
        picture.grid(column=0,row=1,columnspan=3,padx=20)
        #before_step
        img4=ImageTk.PhotoImage(Image.open("UI_img/before_step2.png"))
        before_step=Label(output, image=img4, bg='#344253')
        before_step.image=img4
        before_step.grid(column=12,row=1,columnspan=2,rowspan=2)
        #next_step
        img5=ImageTk.PhotoImage(Image.open("UI_img/next_step2.png"))
        next_step=Label(output, image=img5, bg='#344253')
        next_step.image=img5
        next_step.grid(column=13,row=1,columnspan=2,rowspan=2)
        #setup
        img6=ImageTk.PhotoImage(Image.open("UI_img/setup_logo2.png"))
        setup=Label(output, image=img6, bg='#344253')
        setup.image=img6
        setup.grid(column=14,row=1,columnspan=2,rowspan=2)
        #-----------輸入需要連接的藍芽/Serial Port----------#
        #顯示所有目前可用的port
        COM = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            COM.append('No Port Available!')
        else:
            for port in port_list:
                port_serial = port[0]
                COM.append(port_serial)
        #下拉選藍芽com
        lab1=Label(output,text='藍芽com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
        lab1.grid(column=16, row=2,rowspan=2)
        lab1_ttp = CreateToolTip(lab1, "請選擇藍芽連接埠")
        class serv_port:
            def __init__(self, parent):
                self.parent = parent
                self.combo()

            def combo(self):
                self.box_value = StringVar()
                self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly',width=10)
                self.box['values'] = (COM)
                #self.box.current(0)
                self.box.grid(column=17, row=3,columnspan=2)

        #下拉選步進馬達com
        lab2=Label(output,text='步進馬達com :',fg='#FFFFFF',bg='#344253',font=('Calibri,微軟正黑',12,'bold'))
        lab2.grid(column=16,row=3,rowspan=2,padx=10,pady=50)
        lab2_ttp = CreateToolTip(lab2, "請選擇步進馬達連接埠")
        class step_port:

            def __init__(self, parent):
                self.parent = parent
                self.combo()

            def combo(self):
                self.box_value = StringVar()
                self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly',width=10)
                self.box['values'] = (COM)
                #self.box.current(0)
                self.box.grid(column=17, row=3,columnspan=2,rowspan=2,padx=10)

        if __name__ == '__main__':
            connect1 = serv_port(output)    
            connect2 = step_port(output)
        #-----------輸入需要連接的藍芽/Serial Port----------#
        #connect
        img7=ImageTk.PhotoImage(Image.open("UI_img/connect2.png"))
        connect=Label(output, image=img7, bg='#344253')
        connect.image=img7
        connect.grid(column=19,row=2,rowspan=2,padx=10,pady=20)
        #grbl
        frame2=Frame(output,width=30,height=14)
        frame2.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
        t=Text(frame2,height=14,width=30, bg='#477979',fg='white',font=('Calibri',14,'bold'),padx=10,pady=5)
        t.grid(column=16,row=4,columnspan=15,rowspan=5,pady=20)
        vbar=ttk.Scrollbar(frame2,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=canvas.yview)
        t.config(yscrollcommand=vbar.set)
        t.pack(side=LEFT,expand=True,fill=BOTH)
        t_ttp = CreateToolTip(t, "圖檔之gcode碼顯示處")
        #pause
        def pause_window():
            window_pause=Toplevel(window)
            window_pause.title('pause')
            window_pause.geometry('300x200+600+300')
            window_pause.resizable(0,0)
            window_pause.configure(background='#344253')
            
            def colse_pause():
                window_pause.destroy()

            Label(window_pause,text='目前pecker已暫停!',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',14,'bold')).grid(row=0,column=0,columnspan=6,padx=65,pady=20)
            Label(window_pause,text='請按繼續繪圖',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',14,'bold')).grid(row=1,column=0,columnspan=6,padx=65,pady=10)
            img31=ImageTk.PhotoImage(Image.open("UI_img/move_on.png"))
            move_on=Button(window_pause, image=img31, bg='#344253',command=colse_pause)
            move_on.image=img31
            move_on.grid(row=2,column=0,columnspan=6,pady=10)

        img8=ImageTk.PhotoImage(Image.open("UI_img/pause.png"))
        pause=Button(output, image=img8, bg='#344253',command=pause_window)
        pause.image=img8
        pause.grid(column=16,row=10)
        pause_ttp = CreateToolTip(pause, "暫停圖檔輸出")
        #stop
        def stop_window():
            window_stop=Toplevel(window)
            window_stop.title('stop')
            window_stop.geometry('300x200+600+300')
            window_stop.resizable(0,0)
            window_stop.configure(background='#344253')
            
            def colse_pause():
                window_stop.destroy()
            def show_home():
                window.update()
                window.deiconify()
                window_stop.destroy()
                output.destroy()
                #im = Image.open("UI_img/white_bg.png")
                #photo2 = ImageTk.PhotoImage(im)
                #item=canvas.create_image(20,20,anchor=NW,image=photo2)

            Label(window_stop,text='請問您確定要終止pecker繪圖，',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',14,'bold')).grid(row=0,column=0,columnspan=6,padx=20,pady=20)
            Label(window_stop,text='並回home重新操作?',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',14,'bold')).grid(row=1,column=0,columnspan=6,padx=20,pady=10)
            img41=ImageTk.PhotoImage(Image.open("UI_img/ok.png"))
            ok=Button(window_stop, image=img41, bg='#344253',command=show_home)
            ok.image=img41
            ok.grid(row=2,column=2,pady=10)
            img42=ImageTk.PhotoImage(Image.open("UI_img/cancel.png"))
            cancel=Button(window_stop, image=img42, bg='#344253',command=colse_pause)
            cancel.image=img42
            cancel.grid(row=2,column=3,padx=20,pady=10)
        
        img9=ImageTk.PhotoImage(Image.open("UI_img/stop.png"))
        stop=Button(output, image=img9, bg='#344253',command=stop_window)
        stop.image=img9
        stop.grid(column=17,row=10)
        stop_ttp = CreateToolTip(stop, "終止圖檔輸出，pecker歸零")

    Label(window_send,text='目前墨水量 : ',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',12,'bold')).grid(row=0,column=0,columnspan=2,padx=20,pady=10)
    progress = ttk.Progressbar(window_send, orient="horizontal",length=250, mode="determinate")
    progress.grid(row=1,column=0,columnspan=4,padx=20,pady=10)
    progress.start(100)
    Label(window_send,text='請問您確定要送出?',fg='#FFFFFF',bg='#344253',font=('微軟正黑體',12,'bold')).grid(row=2,column=0,columnspan=6,padx=20,pady=10)
    img21=ImageTk.PhotoImage(Image.open("UI_img/ok.png"))
    ok=Button(window_send, image=img21, bg='#344253',command=output)
    ok.image=img21
    ok.grid(row=3,column=1,pady=10)
    img22=ImageTk.PhotoImage(Image.open("UI_img/cancel.png"))
    cancel=Button(window_send, image=img22, bg='#344253',command=colse_send)
    cancel.image=img22
    cancel.grid(row=3,column=2,padx=20,pady=10)
#墨水量確定/輸出畫面----------------------------------------------------------------------------------------------------#

#send
img8=ImageTk.PhotoImage(Image.open("UI_img/send.png"))
send=Button(window, image=img8, bg='#344253',command=send_window)
send.grid(column=15,row=10,columnspan=3)
button6_ttp = CreateToolTip(send, "傳送")

window.mainloop()
#主畫面----------------------------------------------------------------------------------------------------#