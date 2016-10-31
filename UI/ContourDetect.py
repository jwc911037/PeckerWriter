#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
import cv2
from math import hypot

def bubbleSort(idx,order):
    for passnum in range(len(idx)-1,0,-1):
        for i in range(passnum):
            if idx[i]>idx[i+1]:
                # exchange idx
                tmp = idx[i]
                idx[i] = idx[i+1]
                idx[i+1] = tmp
                # exchange order
                tmp_o = order[i]
                order[i] = order[i+1]
                order[i+1] = tmp_o

# img = raw_input('Enter Img:')
# fname = raw_input('File Save:')
def cntdetect(img,fname):
    global im
    fhand = open(fname,'wb')
    im = cv2.imread(img)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,125,255,0)
    imgray,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt_num = len(contours)
    # print cnt_num
    dst_idx = list()
    dst_order = range(cnt_num)

    for i in range(cnt_num):
        cnt = contours[i]
        a = sum(cnt)
        dst = round(hypot(float(a[0][0])/len(cnt),float(a[0][1])/len(cnt)),2)
        dst_idx.append(dst)
    bubbleSort(dst_idx,dst_order)
    # print dst_order
    # print dst_idx

    fhand.write('G1\n')
    fhand.write('Z up\n')
    for i in dst_order:
        cnt = contours[i]
        cv2.drawContours(im, [cnt], 0, (0,255,0),0)
        fhand.write('X'+str(cnt[0][0][0])+' Y'+str(cnt[0][0][1])+'\n')
        fhand.write('Z down\n')
        for c in range(len(cnt)):
            # print 'X',float(cnt[c][0][0]),' Y',float(cnt[c][0][1])
            fhand.write('X'+str(cnt[c][0][0])+' Y'+str(cnt[c][0][1])+'\n')
        fhand.write('X'+str(cnt[0][0][0])+' Y'+str(cnt[0][0][1])+'\n')
        # print 'X',float(cnt[0][0][0]),' Y',float(cnt[0][0][1])
        fhand.write('Z up\n')
    fhand.write('X0 Y0\n')
    # raw_input('Press <Enter> to terminate the prog..')
    fhand.close()

# cv2.imshow('im', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
if __name__ == '__main__':
    img = raw_input('Enter Img:')
    fname = raw_input('File Save:')
    cntdetect(img,fname)
    cv2.imshow('im', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()