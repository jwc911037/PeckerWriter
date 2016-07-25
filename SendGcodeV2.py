#!/user/bin env python 
#-*- coding:utf8 -*-
import serial.tools.list_ports
import serial
import time

def ListPort():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) > 0:
        for port in port_list:
            available_port = port[0]
            print '>>> '+available_port

def OpenPort(port_name, port, baudrate):
    try:
        port_name.port = port
        port_name.baudrate = baudrate
        port_name.timeout = 0.5
        port_name.open()
    except serial.SerialException:
        print 'Counld Not Open Port: '+port_name.port

if __name__ == '__main__':
    step = serial.Serial()
    serv = serial.Serial()
    ListPort()
    step_port = raw_input('step_port: ')
    serv_port = raw_input('serv_port: ')
    try:
       OpenPort(step,step_port,115200)
       OpenPort(serv,serv_port,9600)

       tmp_pen_value = '2'
       serv.write(tmp_pen_value+'\n')

       step.write("\r\n\r\n")
       #暫停兩秒等待grbl初始化(Grbl 0.9g ['$' for help])
       time.sleep(2)
       #清掉grbl初始化指令
       step.flushInput()

       ready = raw_input('Enter to Start!')

       gcode = open('gcode/r.txt','r');
       step.write('G92 X0 Y0 Z0\n')
       step.write('G1 F50\n')
       for line in gcode:
           l = line.strip() # Strip all EOL characters for consistency
           
           pen_value = l[-1] #內所定義的提放筆的值(Z值)
           if  pen_value != tmp_pen_value:
               tmp_pen_value = pen_value 
               serv.write(pen_value+'\n')
               time.sleep(1)

           step.write(l + '\n')    
           grbl_out = step.readline()
           print l+' : ' + grbl_out.strip()
       #結束後回到原點及關閉gcode檔案、port
       serv.write('1\n')
       step.write('G1 X0 Y0 Z0\n')
       gcode.close()
       step.close()
       serv.close() 
    except Exception:
        print 'there is some bugs!'
        step.close()
        serv.close()
        raise     