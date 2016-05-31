#-----------------------------------------------------------------------------
# Name:        SetSerial.py
# Purpose:     serial command.create serial port connection. send "mycommand","findcommand".
#               close connection by close().function.
# Author:      <chen sheng cong>
#
# Created:     2013/03/04
# RCS-ID:      $Id: SetSerial.py $
# Copyright:   (c) 2006
# Licence:     <0.0.1>
#-----------------------------------------------------------------------------
import serial
import time
import string
from WtLog import log_public

#-------------------------
KEY_RT = "\r"
KEY_TAB = "\t"
KEY_COM = "COM"
#-------------------------
KEY_INSERT_PL_LOGIN = "cwcos login:"
KEY_PL_PASS = "Password:"
KEY_INSERT_PL_COMMAND="cwcos#"
KEY_MANAGE_PL_LOGIN = "Login:"
KEY_MANAGE_PL_LOGIN_SUB =  "BNOS>"
KEY_MANAGE_PL_COMMAND = "BNOS#"
KEY_MORE = "---more---"
#------------------------
KEY_SER_ERROR_001 = "please check port number and baudrate./error-001/Can not open serial port "
KEY_SER_ERROR_002 = "please check mycommand format./error-002/Can not send command: "
KEY_SER_ERROR_003 = "please check findcommand format./error-002/Can not find findcommand: "
KEY_SER_ERROR_004 = "please check serial connection./error-002/Can not send command: "


class clsSerial():
    m_ERROR_MSG = "no error"    #recoard error message.
    m_COMhld = None
    #-----------------------------------------------------------------------------
    # Name:         init fuction
    # param:        param1-number of device, numbering starts at zero. if everything fails, the user initialize the telnet class
    #               can specify a device string, note that this isn't portable anymore port will be opened if one is specified
    #               param2-baud rate      
    # explain:     
    # Author:       chen sheng cong
    #
    # Created:      2013/01/13
    #-----------------------------------------------------------------------------                
    def __init__(self,port = "1", baudrate="115200",Platf = "M"):
          
          
        myPort = string.atoi(port) - 1
        mybaudrate = string.atoi(baudrate)      
        self.result =False
        try:
            
            self.m_COMhld = serial.Serial(  
                                        myPort,
                                        mybaudrate,           
                                        bytesize=8,             # number of data bits
                                        parity='N',             # enable parity checking
                                        stopbits=1,             # number of stop bits
                                        timeout=1,              # set a timeout value, None to wait forever
                                        xonxoff=False,          # enable software flow control
                                        rtscts=False,           # enable RTS/CTS flow control
                                        writeTimeout=None,      # set a timeout for writes
                                        dsrdtr=False,           # None: use rtscts setting, dsrdtr override if True or False
                                        interCharTimeout=None   # Inter-character timeout, None to disable
                                         )       
            self.result = True
        except:                         
            log_public(KEY_SER_ERROR_001+KEY_COM+port)
            m_ERROR_MSG = KEY_SER_ERROR_001+KEY_COM+port
            self.result =False
            return None                             
                                     
     
        
        #print self.m_COMhld.portstr     #delete
        self.m_COMhld.write(KEY_RT)
        self.m_COMhld.write(KEY_RT) 

        #read1 = self.m_COMhld.read(100) #delete
        #print read1#delete

   

    #-----------------------------------------------------------------------------
    # Name:        mycommmand fuction
    # input param: SENDSTR:input this command string WAITSTR:the command wait string Mutiro
    # explain:     input command
    # Author:      chen sheng cong
    #
    # Created:     2013/03/04
    #
    #-----------------------------------------------------------------------------       
    def mycommand(self,SENDSTR,WAITSTR,TIMEOUTSTR):
        
        myTIMEOUT = string.atoi(TIMEOUTSTR) #string to int
        timeCount = 0
        
        if self.m_COMhld  == None :
            return False
        try:
            while timeCount < myTIMEOUT:            
           
                strRead = self.m_COMhld.read(1024) #read serial information,read 1024bytes a time.
                print strRead
                
                if strRead.find(WAITSTR) >=0:       #find string you waiting for.
                    self.m_COMhld.write(SENDSTR+KEY_RT)  # if find success,then send you are command

                    return True
                else:    
                    self.m_COMhld.write(KEY_RT)     #if not find,send return,wait 1 second,read next data.    
                    timeCount += 1
                    time.sleep(0.5)                
                    continue
        except:   
            log_public(KEY_SER_ERROR_004+SENDSTR)   #not find string,set error.
            m_ERROR_MSG = KEY_SER_ERROR_004+SENDSTR
            return False  
        
        log_public(KEY_SER_ERROR_002+SENDSTR)   #not find string,set error.
        m_ERROR_MSG = KEY_SER_ERROR_002+SENDSTR
        return True  
        
    #-----------------------------------------------------------------------------
    # Name:        mycommmand fuction
    # input param: SENDSTR:input this command string WAITSTR:the command wait string Mutiro
    # explain:     input command
    # Author:      chen sheng cong
    #
    # Created:     2013/03/04
    #
    #-----------------------------------------------------------------------------               
    def find_command(self,SENDSTR,WAITSTR,FINDSTR,TIMEOUT=10,RESENDFLAG=True):
        
        bstrEND = False
        bRet = False
        strMyFind = ""  #temp storage information
        bRet = self.mycommand(SENDSTR,WAITSTR,TIMEOUT)
        if bRet == False:        
            return False
        
        try:
            #check find string.
            while bstrEND == False:
                  
                strMyFind = self.m_COMhld.read(1024) #read serial information,read 1024bytes a time.
                print strMyFind
                    
                if strMyFind.find(FINDSTR) >=0:         #find string you waiting for.
                    self.KillMoreMark(strMyFind,WAITSTR)        # kill ---more---
                    return True
                else:    
                    if strMyFind.find(WAITSTR) >=0:
                        bstrEND = True
                    self.m_COMhld.write(KEY_RT)     #if not find,send return,wait 1 second,read next data.    
                    continue
        except: 
            log_public(KEY_SER_ERROR_004+SENDSTR)   #not find string,set error.
            m_ERROR_MSG = KEY_SER_ERROR_004+SENDSTR
            return False  
                        
        log_public(KEY_SER_ERROR_003+FINDSTR)   #not find string,set error.
        m_ERROR_MSG = KEY_SER_ERROR_003+FINDSTR 
        return True   
        
    
    def KillMoreMark(self,strCheck,strEnd):
        myFindCheck = strCheck
        bFindMore = True
        idx = 0
        
        try:        
            while bFindMore == True:        
                if myFindCheck.find(KEY_MORE) >= 0:
                    self.m_COMhld.write(KEY_TAB)                
                    myFindCheck = self.m_COMhld.read(1024)
                    print myFindCheck  
                    idx += 1 
                elif myFindCheck.find(strEnd) == -1:
                    self.m_COMhld.write(KEY_RT)                
                    myFindCheck = self.m_COMhld.read(1024)
                    print myFindCheck  
                    idx += 1 
                else:
                    bFindMore = False
        except:             
            log_public(KEY_SER_ERROR_004+strEnd)   #not find string,set error.
            m_ERROR_MSG = KEY_SER_ERROR_004+strEnd
            return False  
                            
        print "idx",idx
        return True

    #-----------------------------------------------------------------------------
    # Name:        close fuction
    # explain:     close serial port
    # Author:      chen sheng cong
    #
    # Created:     2013/03/04
    #
    #-----------------------------------------------------------------------------                                   
    def close(self): 
        
        if self.m_COMhld  == None :
            return False
                       
        self.m_COMhld.close() 
        print "test"
        return True
 
 
    #-----------------------------------------------------------------------------
    # Name:        sleep fuction
    # input param: myTIME:the time you want sleep(one second every times)
    # explain:     sleep time.
    # Author:      chen sheng cong
    #
    # Created:     2013/03/04
    #
    #-----------------------------------------------------------------------------                       
    def sleep(self,myTIME):
        int_time = string.atoi(myTIME)
        time.sleep(int_time)
        return True

    #-----------------------------------------------------------------------------
    # Name:        GetErrorInfo -get error information
    # ruturn:      return string.the string is error message. if no error happen ,it is "no error".
    # Author:      <chensc>
    #
    # Created:     2013/02/28
    #-----------------------------------------------------------------------------
    def GetErrorInfo(self):
       return self.m_ERROR_MSG
   
if __name__=='__main__':
    test = clsSerial()
    test.mycommand('root','cwcos login:','2')
   