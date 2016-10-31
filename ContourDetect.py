#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
import cv2
img = raw_input('Enter Img:')
fname = raw_input('File Save:')
fhand = open('gcode/Unajusted/'+fname,'wb')
  
im = cv2.imread('img/'+img)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print len(contours)
fhand.write('G1\n')
fhand.write('Z up\n')
for i in range(len(contours)):
    cnt = contours[i]
    cv2.drawContours(im, [cnt], 0, (0,255,0),-1)
    fhand.write('X'+str(cnt[0][0][0])+' Y'+str(cnt[0][0][1])+'\n')
    fhand.write('Z down\n')
    for c in range(len(cnt)):
        # print 'X',float(cnt[c][0][0]),' Y',float(cnt[c][0][1])
        fhand.write('X'+str(cnt[c][0][0])+' Y'+str(cnt[c][0][1])+'\n')
    fhand.write('X'+str(cnt[0][0][0])+' Y'+str(cnt[0][0][1])+'\n')
    # print 'X',float(cnt[0][0][0]),' Y',float(cnt[0][0][1])
    fhand.write('Z up\n')
fhand.write('X0 Y0\n')
raw_input('Press <Enter> to terminate the prog..')
fhand.close()

cv2.imshow('im', im)
cv2.waitKey(0)
cv2.destroyAllWindows()