#!/user/bin env python 
#-*- coding:utf8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import sqrt
#formula to modify Logical (X, Y) to Physical (X, Y)
def MODIFY_POS(LogX, LogY, L):
    PhysX = sqrt(LogX**2 + LogY**2)
    PhysY = sqrt((L-LogX)**2 + LogY**2)
    return PhysX,PhysY

LENGTH_OF_BOARD = float(raw_input('Length of Board: '))
INIT_POS = [float(n) for n in raw_input('Input Init Pos: ').split(' ')]
PhysStarX, PhysStarY = MODIFY_POS(INIT_POS[0], INIT_POS[1], LENGTH_OF_BOARD)

font = ImageFont.truetype("font/VTC-BadTattooHandOne.ttf", 150)
im = Image.new("RGB", (400,200), (255,255,255))
draw = ImageDraw.Draw(im)
draw.text((30,50), "Rose", font=font, fill=(0,0,0))
im.save("img/rose.jpg")

gcode = open('gcode/rose.txt','wb')
im=Image.open('img/rose.jpg')
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
