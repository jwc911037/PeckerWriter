#!/user/bin env python 
#-*- coding:utf8 -*-
import Pecker
import serial.tools.list_ports
import serial
import time

<<<<<<< HEAD
=======
# gname = raw_input('Gcode:')


# Pecker.ListPort()
# step_port = raw_input('step_port:')
# serv_port = raw_input('serv_port:')
# step = serial.Serial(step_port,115200)
# serv = serial.Serial(serv_port,9600)

# tstart = time.asctime( time.localtime(time.time()) )
# print 'Initialize grbl...'
# step.write("\r\n\r\n")
# time.sleep(2)
# step.flushInput()
>>>>>>> origin/master
def sndgcode(step,gname):
    gcode = open(gname,'r')
    for line in gcode:
        l = line.strip()
        if l.startswith('Z'):
            continue
            # pen = l.split('Z')[1]
            # step.write('G4 P1\n')
            # print l + ':' + grbl_out.strip()
            # grbl_out = step.readline()         
            # serv.write(pen+'\n')
            # step.write('G4 P1\n')
            # grbl_out = step.readline()
            # print l + ':' + grbl_out.strip()
        else:
            step.write(l+'\n')
            grbl_out = step.readline()
            print l + ':' + grbl_out.strip()
    gcode.close()
    step.close()
    # serv.close() 
<<<<<<< HEAD

=======
# tend = time.asctime( time.localtime(time.time()) )
# raw_input('Press <Enter> to terminate the prog.')
# print tstart,tend
>>>>>>> origin/master
if __name__ == '__main__':
    gname = raw_input('Gcode:')
    step_port = raw_input('step_port:')
    # serv_port = raw_input('serv_port:')
    step = serial.Serial(step_port,115200)
    # serv = serial.Serial(serv_port,9600)
    sndgcode(step_port,gname)