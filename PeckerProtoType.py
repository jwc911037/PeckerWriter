#!/user/bin env python 
#-*- coding:utf8 -*-
import sys
import serial
import serial.tools.list_ports
import time
from math import sqrt

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
    #make sure both step & serv port are open    
    if step.isOpen() and serv.isOpen():
        gcode_file = raw_input('Gcode File: ')
        gcode = open('gcode/'+gcode_file,'r')
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
        TmpPenValue = 2

        for l in gcode:
            l = line.strip() # Strip all EOL characters for consistency
            CurPenValue = l[-1] #內所定義的提放筆的值(Z值)
            if  CurPenValue != TmpPenValue:
                TmpPenValue = CurPenValue 
                serv.write(CurPenValue+'\n')
                #獲取Gcode
            print 'pen: '+CurPenValue+'\n',
            time.sleep(1)
            step.write('G4 P1\n')
            print 'Sending: ' + l,
            step.write(l + '\n') # Send g-code block to grbl   
            grbl_out = step.readline() # Wait for grbl response with carriage return
            print ' : ' + grbl_out.strip()

        gcode.close()
        serv.close()
        step.close()
        print 'Done! Have a nice day!'
    else:
        print 'Sorry, '+step.port+' Or '+serv.port+' Is Down!'
        
    
