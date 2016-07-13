#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Tkinter as tk
from Tkinter import StringVar
from PIL import ImageTk, Image
import sys,os
import ttk
import tkFileDialog
window = tk.Tk()
window.title('pecker')
window.resizable(0,0)
window.geometry('1000x600')
window.configure(background='#344253')
#icon
window.iconbitmap(default='UI_img/icon.ico')
#logo
img=ImageTk.PhotoImage(Image.open("UI_img/logo.png"))
logo=tk.Label(window, image=img, bg='#344253')
logo.grid(column=0,row=0,columnspan=5)
#question
img1=ImageTk.PhotoImage(Image.open("UI_img/question.png"))
question=tk.Button(window, image=img1, bg='#344253')
question.grid(column=22,row=0)
#canvas
canvas=tk.Canvas(window,width=700,height=470,bg='blue')
canvas.grid(column=1,row=3,columnspan=15,rowspan=11,padx=10,pady=10)
def open_img():
    fileName = tkFileDialog.askopenfilename(filetypes = (("JPEG", "*.jpg;*.jpeg"),("PNG", "*.png")))
    img2=ImageTk.PhotoImage(Image.open(fileName))
    canvas2=tk.Canvas(window,width=700,height=470,bg='white')
    canvas2.create_image(350,225,image=img2)
    canvas2.grid(column=1,row=3,columnspan=15,rowspan=11,padx=10,pady=10)
#picture
img3=ImageTk.PhotoImage(Image.open("UI_img/picture.png"))
picture=tk.Button(window, image=img3, bg='#344253',command=open_img)
picture.grid(column=0,row=1,columnspan=3)
#before_step
img4=ImageTk.PhotoImage(Image.open("UI_img/before_step.png"))
before_step=tk.Button(window, image=img4, bg='#344253')
before_step.grid(column=12,row=1,columnspan=2,rowspan=2)
#next_step
img5=ImageTk.PhotoImage(Image.open("UI_img/next_step.png"))
next_step=tk.Button(window, image=img5, bg='#344253')
next_step.grid(column=13,row=1,columnspan=2,rowspan=2)
#setup
img6=ImageTk.PhotoImage(Image.open("UI_img/setup_logo.png"))
setup=tk.Button(window, image=img6, bg='#344253')
setup.grid(column=14,row=1,columnspan=2,rowspan=2)

#下拉選com
class Application:

    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly',width=10)
        self.box['values'] = ('com1', 'com2', 'com3')
        self.box.current(0)
        self.box.grid(column=16, row=3,columnspan=2)

if __name__ == '__main__':
    app = Application(window)    

#connect
def insert_grbl():
    var="Grbl 0.9i ['$' for help"
    t.insert('insert',var)

img7=ImageTk.PhotoImage(Image.open("UI_img/connect.png"))
setup=tk.Button(window, image=img7, bg='#344253',command=insert_grbl)
setup.grid(column=18,row=3,columnspan=3,padx=10)
#grbl
t=tk.Text(window,height=15,width=24, bg='#477979',fg='white',font=('Calibri',14,'bold'),padx=10,pady=5)
t.grid(column=17,row=4,columnspan=6,rowspan=9)
#send
img8=ImageTk.PhotoImage(Image.open("UI_img/send.png"))
setup=tk.Button(window, image=img8, bg='#344253')
setup.grid(column=16,row=13,columnspan=2,padx=5)
window.mainloop()