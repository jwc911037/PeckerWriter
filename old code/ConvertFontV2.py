#!/user/bin env python 
#-*- coding:utf8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import *
import numpy as np

def PosCaculator(pos,init,l):
    pos[1] = -pos[1] #由下往上畫的座標調整
    #----------計算座標轉換----------#
    actual_pos = pos+init #原座標須加上一開始筆架所在位置
    modified_pos = np.array([0.,0.])
    modified_pos[0] = hypot(actual_pos[0], actual_pos[1]) #sqrt(X**2 + Y**2)
    modified_pos[1] = hypot((l-actual_pos[0]), actual_pos[1]) #sqrt((L-X)**2 + Y**2)
    #----------計算座標轉換----------#
    pos[1] = -pos[1] #計算完畢後恢復原值
    return modified_pos

if __name__ == '__main__':
    # font = ImageFont.truetype("font/VTC-BadTattooHandOne.ttf", 50)
    # im = Image.new("RGB", (90,65), (255,255,255))
    # draw = ImageDraw.Draw(im)
    # draw.text((10,10), "R", font=font, fill=(0,0,0))
    # im.save("img/r.jpg")

    board_len = float(raw_input('Length of Board: '))
    init = np.array(map(float,raw_input('Input Init Pos: ').split()))

    gcode = open('gcode/rose1.txt','wb')
    im=Image.open('img/rose.jpg')
    # gcode.write('G92 X0 Y0 Z0\n')
    # gcode.write('G1 F50\n')

    start = np.array([0.,0.])
    init_pos = PosCaculator(init,start,board_len)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pos = np.array([x,y])
            pos_move = PosCaculator(pos,init,board_len)
            pos_move -=init_pos

            if im.getpixel((x,y)) == (0,0,0):
                gcode.write('G1 X'+str(pos_move[0])+' Y'+str(pos_move[1])+' Z1\n')
            # else:
            #     gcode.write('G1 X'+str(pos_move[0])+' Y'+str(pos_move[1])+' Z2\n')

    # gcode.write('G28\n')
    gcode.close()
    print 'Covertd to Gcode Susses!'