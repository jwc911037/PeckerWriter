#!/user/bin env python 
#-*- coding:utf8 -*-
import numpy as np
from math import sqrt,hypot
import serial.tools.list_ports
import serial
import time

def ListPort():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        for port in port_list:
            available_port = port[0]
            print '>>> '+available_port
    else: print 'No available port.'

def OpenPort(port_name, port, baudrate):
    try:
        port_name.port = port
        port_name.baudrate = baudrate
        port_name.timeout = None
        port_name.write_timeout = None
        port_name.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+port_name.port

def SendMessages(msg,port_name):
    port_name.write(msg)

if __name__ == '__main__':
    s = serial.Serial()
    OpenPort(s,'COM24',115200)
    s.close()