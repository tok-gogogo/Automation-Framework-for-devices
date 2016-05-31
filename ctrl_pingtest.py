#-*- coding: UTF-8 -*- 
import os
import sys
import time
import string
import win32api
import win32gui
import win32ui
import win32con
import win32com.client
from win32con import KEYEVENTF_KEYUP
from WtLog import log_public

KEY_TIME_FORMAT = "%Y%m%d_%H%M%S"

#---------------------------------------
#--------------
#Error List
ERR_PING_TEST_0001 = 'error: Open the pingtest software failed.Please check the path whether exist./ErrorCode-pingtest-0001'
ERR_PING_TEST_0002 = 'error: Looking for the handle failed.Please check whether the handle exist./ErrorCode-pingtest-0002'
ERR_PING_TEST_0003 = 'error: Input message failed.Please check whether the calling function in accordance or the handle whether exist./ErrorCode-pingtest-0003'
ERR_PING_TEST_0004 = 'error: Get message failed.Please check whether the calling function in accordance or the handle whether exist./ErrorCode-pingtest-0004'
ERR_PING_TEST_0005 = 'error: Config log failed.Please check whether the calling function in accordance or the handle whether exist./ErrorCode-pingtest-0005'
ERR_PING_TEST_0006 = 'error: Edit failed.Please check whether the calling function in accordance./ErrorCode-pingtest-0006'
ERR_PING_TEST_0007 = 'error: Configuration packet size failed.Please check whether the calling function in accordance or the handle whether exist./ErrorCode-pingtest-0007'
ERR_PING_TEST_0008 = 'error: Control butten failed.Please check whether the calling function in accordance or the handle whether exist./ErrorCode-pingtest-0008'

ERR_PING_CLOSE_0001 = 'error: Edit the file failed.Please check whether the calling function in accordance or the file whether exist./ErrorCode-pingtest-0009'


def setEditText(hwnd, text, append=False):
    '''Set an edit control's text.
    
    Arguments:
    hwnd            The edit control's hwnd.
    text            The text to send to the control. This can be a single
                    string, or a sequence of strings. If the latter, each will
                    be become a a seperate line in the control.
    append          Should the new text be appended to the existing text?
                    Defaults to False, meaning that any existing text will be
                    replaced. If True, the new text will be appended to the end
                    of the existing text.
                    Note that the first line of the new text will be directly
                    appended to the end of the last line of the existing text.
                    If appending lines of text, you may wish to pass in an
                    empty string as the 1st element of the 'text' argument.

    Usage example:  print "Enter various bits of text."
                    setEditText(editArea, "Hello, again!")
                    time.sleep(.5)
                    setEditText(editArea, "You still there?")
                    time.sleep(.5)
                    setEditText(editArea, ["Here come", "two lines!"])
                    time.sleep(.5)
                    
                    print "Add some..."
                    setEditText(editArea, ["", "And a 3rd one!"], append=True)
                    time.sleep(.5)'''
    
    # Ensure that text is a list        
    try:
        text + ''
        text = [text]
    except TypeError:
        pass

    # Set the current selection range, depending on append flag
    if append:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             -1,
                             0)
    else:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             0,
                             -1)
                             
    # Send the text
    win32gui.SendMessage(hwnd,
                         win32con.EM_REPLACESEL,
                         True,
                       os.linesep.join(text))
                       
def findControls(topHwnd,
                 wantedText=None,
                 wantedClass=None,
                 selectionFunction=None):
    '''Find controls.
    You can identify controls using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required controls' captions must contain.
    wantedClass         Class to which the required controls must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired control.

    Returns:            The window handles of the controls matching the
                        supplied selection criteria.    

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        def findButtons(hwnd, windowText, windowClass):
                            return windowClass == "Button"
                        buttons = findControl(optDialog, wantedText="Button")
                        '''
    def searchChildWindows(currentHwnd):
        results = []
        childWindows = []
        try:
            win32gui.EnumChildWindows(currentHwnd,
                                      _windowEnumerationHandler,
                                      childWindows)
        except win32gui.error:
            # This seems to mean that the control *cannot* have child windows,
            # i.e. not a container.
            return
        for childHwnd, windowText, windowClass in childWindows:
            descendentMatchingHwnds = searchChildWindows(childHwnd)
            if descendentMatchingHwnds:
                results += descendentMatchingHwnds

            if wantedText and \
               not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
            if wantedClass and \
               not windowClass == wantedClass:
                continue
            if selectionFunction and \
               not selectionFunction(childHwnd):
                continue
            results.append(childHwnd)
        return results
        
    return searchChildWindows(topHwnd)

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))
                       
class pingtest():
    
    m_ERROR_MSG = "no error"    #recoard error message.
        
    def GetErrorInfo(self):        
       return self.m_ERROR_MSG
    
    def dic_keycode(self,str_s='A'):
        
        dic={'Backspace':8,'Tab':9,'Enter':13,'Shift':16,'Ctrl':17,'Alt':18,\
        'Caps Lock':20,'Esc':27,'Spacebar':32,'Page Up':33,'Page Down':34,\
        'End':35,'Home':36,'Left':37,'Up':38,'Right':39,'Down':40,'Insert':45,\
        'Delete':46,'Help':47,'Num Lock':144,'F1':112,'F2':113,'F3':114,'F4':115,\
        'F5':116,'F6':117,'F7':118,'F8':119,'F9':120,'F10':121,'F11':122,'F12':123}
        
        if len(str_s) == 1:
            #print '\n str_s:',str_s,ord(str_s)
            return ord(str_s)
        elif len(str_s)>1:
            if dic.has_key(str_s):
                #print '\n str_s:',str_s,dic[str_s]
                return dic[str_s]  
    
    def shortcut_keys (self,list_key=[],time=5):
        
        for x in list_key:
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,0,0)
            win32api.Sleep(time)
        for x in list_key:
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.Sleep(time)
            
        return True
    
    def Mouse_LB_click(self,hwnd):

        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
        time.sleep(1)
    
    def startapp(self,path):
        
        print 'Open the pingtest software,path:',path
        os.startfile(path)
        self.sleep('2')
        hwd = win32gui.FindWindow(None,"PingTest")
        if hwd:
            win32gui.SetForegroundWindow(hwd)    #置顶
            
        return True
        
    def sleep(self,TIME):
        
        time.sleep(string.atoi(TIME))
        
        return True
    
    def found_hwnd(self,hwd_n):
        
        hwd_n = string.atoi(hwd_n)
        hwd = win32gui.FindWindow(None,"PingTest")
        if hwd:
            
            ComboBox_list = findControls(hwd,wantedClass='Edit')
            #print ComboBox_list
            hwnd = ComboBox_list[hwd_n]
            #print hwnd
            return hwnd
        return False
    
    def input_msg(self,hwd_n,msg):
        
        hwd_edit = self.found_hwnd(hwd_n)
        #print hwd_edit
        setEditText(hwd_edit,msg)
        self.sleep('1')
        
        return True
    
    def get_msg(self,hwd_n):
        
        hwd_edit = self.found_hwnd(hwd_n)
        bufLen = 1024
        buf = win32gui.PyMakeBuffer(bufLen)
        n = win32gui.SendMessage(hwd_edit, win32con.WM_GETTEXT, bufLen, buf)
        #print 'Get the message:',buf[0:n]
        
        return buf[0:n]
    
    def file_edit(self,filename):
        
        try:
            packet_msg = self.get_msg('11')
        except:
            log_public(ERR_PING_TEST_0004)            
            self.m_ERROR_MSG = ERR_PING_TEST_0004
            return False 
        print 'Get the packet message:',packet_msg
        
        try:
            min_msg = self.get_msg('12')
        except:
            log_public(ERR_PING_TEST_0004)            
            self.m_ERROR_MSG = ERR_PING_TEST_0004
            return False 
        print 'Get the min message:',min_msg
        
        try:
            max_msg = self.get_msg('13')
        except:
            log_public(ERR_PING_TEST_0004)            
            self.m_ERROR_MSG = ERR_PING_TEST_0004
            return False
        print 'Get the max message:',max_msg
        
        try:
            avg_msg = self.get_msg('14')
        except:
            log_public(ERR_PING_TEST_0004)            
            self.m_ERROR_MSG = ERR_PING_TEST_0004
            return False
        print 'Get the avg message:',avg_msg
        
        list_1 = ''
        sep = '\\'
        list_1 = filename.split(sep)
        list_1.pop()
        file_name = sep.join(list_1)
        
        if os.path.exists(file_name) == False:
            
            msg = "Path does not exist not exists , I will help you mkdir this path:"+file_name
            print msg
            log_public(msg)
            os.mkdir(file_name)
        
        #filename为空，用默认filename 
        if filename == '':
            path1 = os.path.abspath(sys.argv[0])
            string=path1.split('\\')
            path_parent=string[0]
            filename=path_parent +'\\result_'
                
        tmp_file = filename +'_'+time.strftime(KEY_TIME_FORMAT)+'.txt'
        
        print 'To save the results to:',tmp_file
        file = open(tmp_file,'w')
        list_text = 'Packet:',packet_msg,'Min:',min_msg,'Max:',max_msg,'Avg:',avg_msg
        #print list_text
        list_text_str = str(list_text)
        print 'The file content:',list_text_str
        file.write(list_text_str)
        file.close()
        
        return True
    
    def config_edit(self,ip,packet,interv,count):
        
        print 'Input ip value:',ip
        
        try:
            self.input_msg('0',ip)
        except:
            log_public(ERR_PING_TEST_0003)            
            self.m_ERROR_MSG = ERR_PING_TEST_0003
            return False  
        
        print 'Input packet value:',packet
        
        try:
            self.input_msg('1',packet)
        except:
            log_public(ERR_PING_TEST_0003)            
            self.m_ERROR_MSG = ERR_PING_TEST_0003
            return False
        
        print 'Input interv value:',interv
        
        try:
            self.input_msg('2',interv)
        except:
            log_public(ERR_PING_TEST_0003)            
            self.m_ERROR_MSG = ERR_PING_TEST_0003
            return False
        
        print 'Input count value:',count
        
        try:
            self.input_msg('4',count)
        except:
            log_public(ERR_PING_TEST_0003)            
            self.m_ERROR_MSG = ERR_PING_TEST_0003
            return False
        
        return True
        
    def config_PacketSize(self,time,step,Flag):
        
        time = string.atoi(time)
        step = string.atoi(step)
        if Flag == 'Up':
            print 'Increasing number of:',time,',increase the step:',step
        elif Flag == 'Down':
            print 'Reduceing number of:',time,',reduce the step:',step
        hwd = win32gui.FindWindow(None,"PingTest")
        edit_packet_up = win32gui.FindWindowEx(hwd, None, 'msctls_updown32', 'Spin1')
        #print edit_packet_up
        self.Mouse_LB_click(edit_packet_up)
        self.shortcut_keys(['Down'])
        self.sleep('1')
        
        num = time * step
        n = 1
        while n <= num:
            self.shortcut_keys([Flag])
            n = n+1
        
        return True
    
    #type:Ping/Stop/Quit/Reset/Clear/Log File:/Error only
    def control_butten_ping(self):
        
        print 'Control button: Ping'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Ping')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
    
    def control_butten_stop(self,ip):
        
        print 'Control button: stop'
        hwd = win32gui.FindWindow(None,ip)
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Stop')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
        
    def control_butten_quit(self):
        
        print 'Control button: Quit'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Quit')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
    
    def control_butten_reset(self):
        
        print 'Control button: Reset'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Reset')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
    
    def control_butten_clear(self):
        
        print 'Control button: Clear'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Clear')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
    
    def control_butten_status(self):
        
        print 'Control button: status'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Error only')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        return True
        
    def config_log(self,log_name):
        
        print 'Control button: Log File'
        hwd = win32gui.FindWindow(None,"PingTest")
        hwd_butten = win32gui.FindWindowEx(hwd, None, 'Button', 'Log File:')
        #print hwd_butten
        self.Mouse_LB_click(hwd_butten)
        self.sleep('1')
        
        list_1 = ''
        sep = '\\'
        list_1 = log_name.split(sep)
        list_1.pop()
        file_name = sep.join(list_1)
        
        if os.path.exists(file_name) == False:
            
            msg = "Path does not exist not exists , I will help you mkdir this path:"+file_name
            print msg
            log_public(msg)
            os.mkdir(file_name)
        
        #log_name为空，用默认log_name
        if log_name == '':
            path1 = os.path.abspath(sys.argv[0])
            str=path1.split('\\')
            path_parent=str[0]
            self.dst=path_parent +'\\result_'
                
        log_name = log_name +'_'+time.strftime(KEY_TIME_FORMAT)+'.txt'
        print 'To save the log to:',log_name
        
        try:
            self.input_msg('6',log_name)
        except:
            log_public(ERR_PING_TEST_0003)            
            self.m_ERROR_MSG = ERR_PING_TEST_0003
            return False
        
        return True
     
    def ping_close(self,filename):
        
        try:
            self.file_edit(filename)
        except:
            log_public(ERR_PING_CLOSE_0001)            
            self.m_ERROR_MSG = ERR_PING_CLOSE_0001
            return False
        
        print 'Close the pingtest software.'
        self.shortcut_keys(['Alt','F4'])
        
        return True
    
    def ping_test(self,path,ip,packet,interv,count,time,step,Flag,log_name,test_time,status_flag,stop_flag,filename):
        
        try:
            self.startapp(path)
        except:
            log_public(ERR_PING_TEST_0001)            
            self.m_ERROR_MSG = ERR_PING_TEST_0001
            return False
        
        try:
            self.config_edit(ip,packet,interv,count)
        except:
            log_public(ERR_PING_TEST_0006)            
            self.m_ERROR_MSG = ERR_PING_TEST_0006
            return False
        
        try:
            self.config_PacketSize(time,step,Flag)
        except:
            log_public(ERR_PING_TEST_0007)            
            self.m_ERROR_MSG = ERR_PING_TEST_0007
            return False
        
        try:
            self.config_log(log_name)
        except:
            log_public(ERR_PING_TEST_0005)            
            self.m_ERROR_MSG = ERR_PING_TEST_0005
            return False
        
        try:
            self.control_butten_reset()
        except:
            log_public(ERR_PING_TEST_0008)            
            self.m_ERROR_MSG = ERR_PING_TEST_0008
            return False
        
        try:
            self.control_butten_clear()
        except:
            log_public(ERR_PING_TEST_0008)            
            self.m_ERROR_MSG = ERR_PING_TEST_0008
            return False
        
        if status_flag == '1':
            
            try:
                self.control_butten_status()
            except:
                log_public(ERR_PING_TEST_0008)            
                self.m_ERROR_MSG = ERR_PING_TEST_0008
                return False
            
        try:
            self.control_butten_ping()
        except:
            log_public(ERR_PING_TEST_0008)            
            self.m_ERROR_MSG = ERR_PING_TEST_0008
            return False   
        
        if stop_flag == '0':
            
            self.sleep(count)
        else:
            self.sleep(test_time)
            
            try:
                self.control_butten_stop(ip)
            except:
                log_public(ERR_PING_TEST_0008)            
                self.m_ERROR_MSG = ERR_PING_TEST_0008
                return False 
        
        if self.ping_close(filename) == False:
            return False
        
        return True
    
if __name__ == "__main__":
    
    test_ping=pingtest()
    
    test_ping.ping_test(path = r'E:\autotest\pingtest\pingtest.exe',ip = '192.168.10.110',packet = '222',\
    interv = '100',count = '100',time = '3',step = '4',Flag = 'Down',log_name = r'e:\pingtest\log',\
    status_flag = '0',stop_flag = '1',test_time = '10',filename= r'e:\test\result')
    