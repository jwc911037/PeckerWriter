#!/user/bin env python 
#-*- coding:utf8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import sqrt
import sys
import serial
import serial.tools.list_ports
import time
#座標轉換公式
def modify_pos(LogX, LogY, L):
    PhysX = sqrt(LogX**2 + LogY**2)
    PhysY = sqrt((L-LogX)**2 + LogY**2)
    return PhysX,PhysY
#產生文字圖片
def make_font(text):
	font = ImageFont.truetype("font/VTC-BadTattooHandOne.ttf", 150)
	im = Image.new("RGB", (400,200), (255,255,255))
	draw = ImageDraw.Draw(im)
	draw.text((30,50), text, font=font, fill=(0,0,0))
	im.save("img/"+text+".jpg")
#將文字圖片轉成Gcode
def convert_font(text):
    gcode = open('gcode/'+text+'.txt','wb')
    im=Image.open('img/'+text+'.jpg')
    #gcode.write('G92 X0 Y0 Z0\n')#set current pos. as zero

    for x in range(im.size[0]):
        for y in range(im.size[1]):

            LogCurX = -x + INIT_POS[0]
            LogCurY = y + INIT_POS[1]
            PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
            PhysCurX = PhysCurX - PhysStarX
            PhysCurY = PhysCurY - PhysStarY

            if im.getpixel((x,y)) == (0,0,0):
                gcode.write('G1 X'+str(PhysCurX)+' Y'+str(PhysCurY)+' Z2 F10\n')
            else:
                gcode.write('G1 X'+str(PhysCurX)+' Y'+str(PhysCurY)+' Z1 F10\n')

    gcode.write('G28\n') #set go home afer drawing finished
    gcode.close()
#顯示所有可用的serial port
def list_port():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) < 0:
        print 'No Serial Port Available Now!'
    else:
        for port in port_list:
            port_serial = port[0]
            print port_serial
"""
#開啟port
def open_port(port_name, port, baudrate, timeout):
    port_name =serial.Serial()
    port_name.port = port
    port_name.baudrate = baudrate
    port_name.timeout = timeout
    try:
        port_name.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+port_name.port
"""
#執行提放筆
def do_pen(tar_port):
    serv=serial.Serial(tar_port, 9600, timeout= 1)
    if serv.isOpen():
        serv.flushInput()
        last_status = '0'
        while True:
            try:
                pen_status = raw_input('Input 1 or 2 to wake the pen: ')
            except Exception:
                serv.close()
                print step.port+' Is Closed. Have A Nice Day!'
                break
            
            if pen_status != '1' and pen_status != '2':
                serv.close()
                print serv.port+' Is Closed. Have A Nice Day!'
                break
            if pen_status != last_status:
                print pen_status,' ',last_status
                serv.write(pen_status+'\n')
            print pen_status+' done!'
            last_status = pen_status
    else:
        print 'Sorry, '+serv.port+' Is Down!'
if __name__ == '__main__':
    list_port()
    port = raw_input('Input: ')
    do_pen(port)