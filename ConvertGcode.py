#!/user/bin env python 
#-*- coding:utf8 -*-
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from math import sqrt

#formula to modify axis x &ｙ
def MODIFY_POS(x, y, L):
    mX = sqrt(x**2 + y**2)
    mY = sqrt((L-x)**2 + y**2)
    return mX,mY

OUTPUT_FILE = 'gcode/test0606.txt'
TARGET_IMG = 'img/r.jpg'
LENGTH_OF_BOARD = 1075
INIT_POS_X = 0
INIT_POS_Y = 900
starX, starY = MODIFY_POS(INIT_POS_X, INIT_POS_Y, LENGTH_OF_BOARD)

gcode = open(OUTPUT_FILE,'wb')
im=Image.open(TARGET_IMG)

gcode.write('G92 X0 Y0 Z0\n')#set current pos. as zero pos.
for x in range(im.size[0]):
    for y in range(im.size[1]):
  
        curX = x + INIT_POS_X
        curY = y + INIT_POS_Y
        mX, mY = MODIFY_POS(curX, curY, LENGTH_OF_BOARD)
        mX = mX - starX
        mY = mY - starY

        if im.getpixel((x,y))[0]<200:
            gcode.write('G0 X' + str(mX) + ' Y' + str(mY) + ' Z1\n')#pen writes        
        else:
            #gcode.write('G0 X' + str(mX) + ' Y' + str(mY) + ' Z2\n')#pen up

gcode.write('G28\n') #set go home afer drawing finished

gcode.close()