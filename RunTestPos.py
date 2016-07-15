#!/user/bin env python 
#-*- coding:utf8 -*-
import sys
import serial
import serial.tools.list_ports
import time
from math import sqrt
#import ListComPort

#formula to modify Logical (X, Y) to Physical (X, Y)
def MODIFY_POS(LogX, LogY, L):
    PhysX = sqrt(LogX**2 + LogY**2)
    PhysY = sqrt((L-LogX)**2 + LogY**2)
    return PhysX,PhysY

LENGTH_OF_BOARD = float(raw_input('Length of Board: '))
INIT_POS = [float(n) for n in raw_input('Input Init Pos: ').split(' ')]
PhysStarX, PhysStarY = MODIFY_POS(INIT_POS[0], INIT_POS[1], LENGTH_OF_BOARD)

#print ListComPort.serial_ports()
port_list = list(serial.tools.list_ports.comports())

if len(port_list) < 0:
    print 'No Serial Port Available Now!'
else:
    for port in port_list:
        port_serial = port[0]
        print "Available Port >> ",port_serial
    STEP_MOTOR_PORT = raw_input('Select a Step Port: ')
    STEP_MOTOR_BAUDRATE = 115200

    step = serial.Serial()
    step.port = STEP_MOTOR_PORT
    step.baudrate = STEP_MOTOR_BAUDRATE
    step.timeout = 5

    try:
        step.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+step.port

    if step.isOpen():
        #啟動grbl
        step.write("\r\n\r\n")
        #暫停兩秒等待grbl初始化(Grbl 0.9g ['$' for help])
        time.sleep(2)
        #清掉grbl初始化指令
        step.flushInput()
        # 讀取grbl檔送到serial port
        while True:
            try:
                pos = [float(n) for n in raw_input('Input Position:').split(' ')]
            except Exception:
                step.close()
                print step.port+' Is Closed. Have A Nice Day!'
                sys.exit(0)

            LogCurX = pos[0] + INIT_POS[0]
            LogCurY = pos[1] + INIT_POS[1]
            PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
            PhysCurX = PhysCurX - PhysStarX
            PhysCurY = PhysCurY - PhysStarY
            print 'G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)
            step.write('G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)+'\n')
            grbl_out = step.readline() # Wait for grbl response with carriage return
            print ' : ' + grbl_out.strip()
    else:
        print 'Sorry, '+step.port+' Is Down!'
        
    
