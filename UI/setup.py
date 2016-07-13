#!/usr/bin/python
# -*- coding: UTF-8 -*-
#設定頁面
import Tkinter as tk
import os,sys
from PIL import ImageTk,Image

window=tk.Tk()
window.title('Setup')
window.geometry('470x500')
window.resizable(0,0)
window.configure(background='#344253')
#icon
window.iconbitmap(default='UI_img/icon.ico')
img1=ImageTk.PhotoImage(Image.open("UI_img/setup.png"))
setup2=tk.Label(window, image=img1, bg='#344253').grid(row=0,column=0,columnspan=20,padx=20,pady=10)
tk.Label(window,text='size',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=1,column=0,columnspan=2)
tk.Label(window,text='width',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=1,column=3)
e=tk.Entry(window,width=10).grid(row=1,column=4,padx=20)
tk.Label(window,text='mm',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=1,column=5)
tk.Label(window,text='height',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=2,column=3)
e=tk.Entry(window,width=10).grid(row=2,column=4,padx=20)
tk.Label(window,text='mm',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold')).grid(row=2,column=5)
img2=ImageTk.PhotoImage(Image.open("UI_img/size.png"))
size=tk.Button(window, image=img2, bg='#344253').grid(row=3,column=1,columnspan=3,pady=10)
img3=ImageTk.PhotoImage(Image.open("UI_img/ok.png"))
ok=tk.Button(window, image=img3, bg='#344253').grid(row=3,column=4,columnspan=2,pady=10)
img4=ImageTk.PhotoImage(Image.open("UI_img/question.png"))
question=tk.Button(window, image=img4, bg='#344253').grid(row=3,column=6,pady=10)
tk.Label(window,text='illustration',fg='#FFFFFF',bg='#344253',font=('Calibri',15,'bold'),width=10,height=1).grid(row=4,column=0,columnspan=2,pady=10,padx=40)

img5=ImageTk.PhotoImage(Image.open("UI_img/illus.png"))
illus=tk.Label(window, image=img5, bg='#344253').grid(row=5,column=0,columnspan=20)

window.mainloop()
