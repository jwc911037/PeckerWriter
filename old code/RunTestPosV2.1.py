#!/user/bin env python 
#-*- coding:utf8 -*-
import sys
import serial
import serial.tools.list_ports
import time
from math import sqrt
import numpy as np
#import ListComPort

#formula to modify Logical (X, Y) to Physical (X, Y)
def MODIFY_POS(LogX, LogY, L):
    PhysX = sqrt(LogX**2 + LogY**2)
    PhysY = sqrt((L-LogX)**2 + LogY**2)
    return PhysX,PhysY

def FindSliceY(x1,y1,x2,y2,curX):
    # (X)*m + (1)*b = Y 
    X = np.array([[x1,1], [x2,1]])
    Y = np.array([y1,y2])

    solve = np.linalg.solve(X, Y)
    m = solve[0]
    b = solve[1]
    curY = m*curX + b
    return curY

Slice = 10

LENGTH_OF_BOARD = float(raw_input('Length of Board: '))
INIT_POS = [float(n) for n in raw_input('Input Init Pos: ').split(' ')]
PhysStarX, PhysStarY = MODIFY_POS(INIT_POS[0], INIT_POS[1], LENGTH_OF_BOARD)

port_list = list(serial.tools.list_ports.comports())

# if len(port_list) < 0:
#     print 'No Serial Port Available Now!'
# else:
#     for port in port_list:
#         port_serial = port[0]
#         print "Available Port >> ",port_serial
#     STEP_MOTOR_PORT = raw_input('Select a Step Port: ')
#     STEP_MOTOR_BAUDRATE = 115200

#     step = serial.Serial()
#     step.port = STEP_MOTOR_PORT
#     step.baudrate = STEP_MOTOR_BAUDRATE
#     step.timeout = 5

    # try:
    #     step.open()
    # except serial.SerialException:
    #     print 'Counld Not Open Port: '+step.port

    if step.isOpen():
        #啟動grbl
        # step.write("\r\n\r\n")
        # #暫停兩秒等待grbl初始化(Grbl 0.9g ['$' for help])
        # time.sleep(2)
        # #清掉grbl初始化指令
        # step.flushInput()
        # # 讀取grbl檔送到serial port
        # TmpCurX = 0
        # TmpCurY = 0
        while True:
            try:
                pos = [float(n) for n in raw_input('Input Position:').split(' ')]
            except Exception:
                step.close()
                print step.port+' Is Closed. Have A Nice Day!'
                sys.exit(0)

            while abs(pos[0]-TmpCurX) > Slice:
                if (pos[0]-TmpCurX)> 0:
                    LogCurX = TmpCurX + Slice
                else:
                    LogCurX = TmpCurX - Slice
                    
                LogCurY = FindSliceY(TmpCurX, TmpCurY, pos[0], pos[1], LogCurX)
                TmpCurX = LogCurX
                TmpCurY = LogCurY

                LogCurX = LogCurX + INIT_POS[0]
                LogCurY = -LogCurY + INIT_POS[1]

                PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
                PhysCurX = PhysCurX - PhysStarX
                PhysCurY = PhysCurY - PhysStarY
                print 'G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)
                # step.write('G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)+'\n')
                # grbl_out = step.readline() # Wait for grbl response with carriage return
                # print '('+str(TmpCurX)+', '+str(TmpCurY)+') : ' + grbl_out.strip()
                # step.write('G4 P0.6')

            LogCurX = pos[0] + INIT_POS[0]
            LogCurY = -pos[1] + INIT_POS[1]
            PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
            PhysCurX = PhysCurX - PhysStarX
            PhysCurY = PhysCurY - PhysStarY
            print 'G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)
            # step.write('G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)+'\n')
            # grbl_out = step.readline() # Wait for grbl response with carriage return
            # print '('+str(pos[0])+', '+str(pos[1])+') : ' + grbl_out.strip()

            TmpCurX = pos[0]
            TmpCurY = pos[1]
    else:
        print 'Sorry, '+step.port+' Is Down!'
        
    
