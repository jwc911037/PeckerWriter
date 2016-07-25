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

def FindLinearY(x1,y1,x2,y2,curX):
    a = (y2-y1)/(x2-x1)
    b = y1 - a*x1
    curY = a*curX + b
    return curY

LENGTH_OF_BOARD = float(raw_input('Length of Board: '))
INIT_POS = [float(n) for n in raw_input('Init Pos: ').split(' ')]
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
    SERV_MOTOR_PORT = raw_input('Select a Serv Port: ')
    STEP_MOTOR_BAUDRATE = 115200
    SERV_MOTOR_BAUDRATE = 9600

    step = serial.Serial()
    step.port = STEP_MOTOR_PORT
    step.baudrate = STEP_MOTOR_BAUDRATE
    step.timeout = 5

    serv = serial.Serial()
    serv.port = SERV_MOTOR_PORT
    serv.baudrate = SERV_MOTOR_BAUDRATE
    serv.timeout = 5

    try:
        step.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+step.port

    try:
        serv.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+serv.port

    if step.isOpen() and serv.isOpen():
        #let the pen down first
        serv.write('2\n')

        #initialize grbl
        step.write("\r\n\r\n")
        #waite 2s for grbl initialization
        time.sleep(2)
        #clear the grbl init. message
        step.flushInput()

        #start to send gcode to serial port...

        TmpCurX = 0
        TmpCurY = 0

        while True:
            try:
                pos = [float(n) for n in raw_input('Input Position:').split(' ')]
            except Exception:
                step.close()
                print step.port+' Is Closed. Have A Nice Day!'
                sys.exit(0)

            while abs(pos[0]-TmpCurX) > 1:
                LogCurX = TmpCurX + 1
                LogCurY = FindLinearY(TmpCurX, TmpCurY, pos[0], pos[1], LogCurX)
                TmpCurX = LogCurX
                TmpCurY = LogCurY

                LogCurX = LogCurX + INIT_POS[0]
                LogCurY = LogCurY + INIT_POS[1]
                PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
                PhysCurX = PhysCurX - PhysStarX
                PhysCurY = PhysCurY - PhysStarY
                print 'G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)
                step.write('G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)+'\n')
                grbl_out = step.readline() # Wait for grbl response with carriage return
                print ' : ' + grbl_out.strip()

                serv.write('1\n')
                step.write('G4 P0.5\n')
                serv.write('2\n')
                step.write('G4 P0.5\n')

            LogCurX = -pos[0] + INIT_POS[0]
            LogCurY = pos[1] + INIT_POS[1]
            PhysCurX, PhysCurY = MODIFY_POS(LogCurX, LogCurY, LENGTH_OF_BOARD)
            PhysCurX = PhysCurX - PhysStarX
            PhysCurY = PhysCurY - PhysStarY
            print 'G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)
            step.write('G0 X'+str(PhysCurX)+' Y'+str(PhysCurY)+'\n')
            grbl_out = step.readline() # Wait for grbl response with carriage return
            print ' : ' + grbl_out.strip()

            serv.write('1\n')
            step.write('G4 P0.5\n')
            serv.write('2\n')
            step.write('G4 P0.5\n')
    else:
        print 'Sorry, '+step.port+' Or '+serv.port+' Is Down!'
        
    
