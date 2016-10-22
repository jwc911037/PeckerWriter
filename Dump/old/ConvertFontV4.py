#!/user/bin env python 
#-*- coding:utf8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import *
import numpy as np

def PosCaculator(pos,init,l):
    # pos[1] = -pos[1] #由下往上畫的座標調整
    #----------計算座標轉換----------#
    actual_pos = pos+init #原座標須加上一開始筆架所在位置
    modified_pos = np.array([0.,0.])
    modified_pos[0] = hypot(actual_pos[0], actual_pos[1]) #sqrt(X**2 + Y**2)
    modified_pos[1] = hypot((l-actual_pos[0]), actual_pos[1]) #sqrt((L-X)**2 + Y**2)
    #----------計算座標轉換----------#
    # pos[1] = -pos[1] #計算完畢後恢復原值
    return 5.*modified_pos

if __name__ == '__main__':
    font = ImageFont.truetype("font/BubblegumSans-Regular.otf", 50)
    im = Image.new("RGB", (100,55), (255,255,255))
    draw = ImageDraw.Draw(im)
    draw.text((2,2), "abcd", font=font, fill=(0,0,0))
    # 20160804圖片翻轉處理
    # im.transpose(Image.ROTATE_180).transpose(Image.FLIP_LEFT_RIGHT).save("img/abcd.jpg")
    im.save('img/abcd.jpg')

    board_len = float(raw_input('Length of Board: '))
    init = np.array(map(float,raw_input('Input Init Pos: ').split()))

    gcode = open('gcode/peka.txt','wb')
    im=Image.open('img/seed.jpg')

    start = np.array([0.,0.])
    init_pos = PosCaculator(init,start,board_len)

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pos = np.array([x,y])
            pos_move = PosCaculator(pos,init,board_len)
            pos_move -=init_pos
            if im.getpixel((x,y))[0] < 200:
                gcode.write('G1 X'+str(pos_move[0])+' Y'+str(pos_move[1])+' Z1 F15\n')
            else:
                gcode.write('G1 X'+str(pos_move[0])+' Y'+str(pos_move[1])+' Z2 F15\n')

    gcode.close()
    print 'Covertd to Gcode Susses!'