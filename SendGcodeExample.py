#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import serial.tools.list_ports
import serial
import time

gname = raw_input('Gcode:')
gcode = open(gname,'r')

Pecker.ListPort()
step_port = raw_input('step_port:')
serv_port = raw_input('serv_port:')
step = serial.Serial(step_port,115200)
serv = serial.Serial(serv_port,9600)
print 'Initialize grbl...'
step.write("\r\n\r\n")
time.sleep(2)
step.flushInput()

for line in gcode:
    l = line.strip()
    if l.startswith('Z'):
        pen = l.split('Z')[1]
        step.write('G4 P2\n')
        grbl_out = step.readline()         
        serv.write(pen+'\n')
        step.write('G4 P1\n')
        grbl_out = step.readline()
    else:
        step.write(l+'\n')
        grbl_out = step.readline()
        print 'RCV:' + grbl_out.strip()
        
raw_input('Press <Enter> to terminate the program.')
gcode.close()
step.close()
serv.close() 