#!/user/bin env python 
#-*- coding:utf8 -*-
import serial
import time
import ListComPort

#定義參數
#-------------------------
GCODE_FILE = 'gcode/penupdown.txt'

#步進馬達serial相關參數宣告
#STEP_MOTOR_PORT = 'COM8'
STEP_MOTOR_BAUDRATE = 115200

#伺服馬達seial相關參數宣告
#SERV_MOTOR_PORT = 'COM19'
SERV_MOTOR_BAUDRATE = 9600

#Gcode指令緩衝時間(s)
PAUSE_EACH_STEP = 0.5
#------------------------- 

#列出所有可用的comport
print ListComPort.serial_ports()
STEP_MOTOR_PORT = raw_input('Step COM: ')
SERV_MOTOR_PORT = raw_input('Serv COM: ')

if(STEP_MOTOR_PORT == '' or SERV_MOTOR_PORT == ''):
	print 'no accurate port now!'
else:
    step = serial.Serial()
    step.port = STEP_MOTOR_PORT
    step.baudrate = STEP_MOTOR_BAUDRATE
    step.timeout = 1

    serv = serial.Serial()
    serv.port = SERV_MOTOR_PORT
    serv.baudrate = SERV_MOTOR_BAUDRATE
    serv.timeout = 1
    try:
        #step.open()
        serv.open()
    except serial.SerialException:
        #print 'Counld not open port: '+step.port+' or '+serv.port
        #print 'Counld not open port: '+step.port
        print 'Counld not open port: '+serv.port

    #if step.isOpen() and serv.isOpen():
    #if step.isOpen():
    if serv.isOpen():
        #開啟gcode文件
        gcode = open(GCODE_FILE,'r');

        #啟動grbl
        #step.write("\r\n\r\n")
        #暫停兩秒等待grbl初始化(Grbl 0.9g ['$' for help])
        time.sleep(2)
        #清掉grbl初始化指令
        #step.flushInput()  

        # 讀取grbl檔送到serial port
        TmpPenValue = 0
        for line in gcode:
            l = line.strip() # Strip all EOL characters for consistency
            
            CurPenValue = l[-1] #內所定義的提放筆的值(Z值)
            if  CurPenValue != TmpPenValue:
                TmpPenValue = CurPenValue 
                serv.write(CurPenValue+'\n')
                #獲取Gcode
            print 'pen: '+CurPenValue+'\n',
            time.sleep(1)
            
            #之後ConvertGcode.py不會產生PAUSE Gcode，而改由這裡直接送出
            #step.write('G4 P'+PAUSE_EACH_STEP+'\n')
            #print 'Sending: ' + l,
            #step.write(l + '\n') # Send g-code block to grbl   
            #grbl_out = step.readline() # Wait for grbl response with carriage return
            #print ' : ' + grbl_out.strip()   

        #結束後關閉gcode檔案及serial port
        gcode.close()
        #step.close()
        serv.close()    
    else:
        print 'the port is down.'