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
ERR_OMNIPEEK_START_STARTAPP_0001 = 'error: Open the omnipeek application software failed.Please check the path whether exist or omnipeek application application installed./ErrorCode-Omnipeek-0001'
ERR_OMNIPEEK_START_SELECT_NETWORKCARD_0002 = 'error: Select network adapter failed.Please check whether the calling function in accordance with the requirements or the card whether exist./ErrorCode-Omnipeek-0002'
ERR_OMNIPEEK_START_SELECT_CHANNEL_0003 = 'error: Select channel failed.Please check whether the calling function in accordance or the channel whether exist./ErrorCode-Omnipeek-0003'
ERR_SAVE_RESULT_SETEDITTEXT_0004 = 'error: Call setEditText failed.Please check whether the calling function in accordance./ErrorCode-Omnipeek-0004'

def findTopWindow(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of a top level window.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which the required window's captions must contain.
    wantedClass         Class to which the required window must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.
                    
    Raises:
    WinGuiAutoError     When no window found.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
    '''
    topWindows = findTopWindows(wantedText, wantedClass, selectionFunction)
    if topWindows:
        
        return topWindows[0]
    else:
        raise WinGuiAutoError("No top level window found for wantedText=" +
                               repr(wantedText) +
                               ", wantedClass=" +
                               repr(wantedClass) +
                               ", selectionFunction=" +
                               repr(selectionFunction))

def findTopWindows(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of top level windows.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which required windows' captions must contain.
    wantedClass         Class to which required windows must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.

    Returns:            A list containing the window handles of all top level
                        windows matching the supplied selection criteria.

    Usage example:      optDialogs = findTopWindows(wantedText="Options")
    '''
    results = []
    topWindows = []
    win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
    for hwnd, windowText, windowClass in topWindows:
        if wantedText and not _normaliseText(wantedText) in _normaliseText(windowText):
            continue
        if wantedClass and not windowClass == wantedClass:
            continue
        if selectionFunction and not selectionFunction(hwnd):
            continue
        results.append(hwnd)
    return results

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))

def _normaliseText(controlText):
    '''Remove '&' characters, and lower case.
    Useful for matching control text.'''
    return controlText.lower().replace('&', '')
                              
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

      
class omnipeek():
    
    m_ERROR_MSG = "no error"    #recoard error message.
        
    def GetErrorInfo(self):        
       return self.m_ERROR_MSG

    def __init__(self):
         
         self.filename = ''
         self.dst = ''
         self.tmp_file = ''
         self.t_hwnd = 0
         self.flag_save = '0'
    
    def sleep(self,TIME):
        time.sleep(string.atoi(TIME))
        return True
    
    def startapp(self,path):
        
        os.startfile(path)
		#shell = win32com.client.Dispatch("WScript.Shell")
        #shell.Run("OPeek")
        return True
        
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
    
    def shortcut_keys(self,list_key=[],time=5):
        
        for x in list_key:
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,0,0)
            win32api.Sleep(time)
        for x in list_key:
            tmp = self.dic_keycode(x)
            win32api.keybd_event(tmp,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.Sleep(time)
        return True
    
    #Click Current Place
    def click_CurrentPlace(self,tmp=(259, 178)):
        
        win32api.SetCursorPos(tmp)
        self.sleep('1')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tmp[0], tmp[1])
        self.sleep('0.05')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tmp[0], tmp[1])
        self.sleep('0.05')
        
    def select_networkCard(self,networkCard_Flag= '3'):
        
        n = 1
        num = 5
        if networkCard_Flag == '1':
            num = 5
        elif networkCard_Flag == '2':
            num = num + 1
        elif networkCard_Flag == '3':
            num = num + 2
                 
        while n <= num:
            self.shortcut_keys(['Down'])
            n+=1
        self.sleep('2')
        return True
    
    def Mouse_LB_click(self,hwnd):

        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
        self.sleep('1')
        
    def selece_Channel(self,channel = '1'):
            
        #1 channel
        self.shortcut_keys(['Home'])
        n = 1
        num = 0
        if channel == '2':
            num = 2
        elif channel == '3':
            num = 4
        elif channel == '4':
            num = 6
        elif channel == '5':
            num = 9 
        elif channel == '6':
            num = 12 
        elif channel == '7':
            num = 15 
        elif channel == '8':
            num = 18 
        elif channel == '9':
            num = 20 
        elif channel == '10':
            num = 22
        elif channel == '11':
            num = 24 
        elif channel == '12':
            num = 26 
        elif channel == '13':
            num = 28
            
        while n <= num:
            self.shortcut_keys(['Ctrl','Down'])
            n+=1
        return True
        
    def omnipeek_start(self,path,networkCard_Flag,channel,timesleep):
        
        print 'Open the omnipeek application software'
        try:
            self.startapp(path)
        except:
            #log_public(ERR_OMNIPEEK_START_STARTAPP_0001)            
            self.m_ERROR_MSG = ERR_OMNIPEEK_START_STARTAPP_0001
            return False
        self.sleep('18')
        
        '''
        print 'To maximize the window'
        try:
            self.shortcut_keys(['Alt','Spacebar','X'])
        except Exception ,exc_str:
            print(exc_str)
            print 'Window to maximize success'
            return False
        '''
        self.sleep('1')
        hwnd0 = win32gui.FindWindow("OmniPeek", 'OmniPeek - [Start Page]')
        win32gui.SetForegroundWindow(hwnd0)
        self.sleep('1')
        print 'Click on the New Capture'
        self.shortcut_keys(['Ctrl','N'])
        
        self.sleep('1')
        hwd = findTopWindow(wantedText='Capture Options')
        win32gui.SetForegroundWindow(hwd)
        #win32gui.MoveWindow(hwd,0,0,510,460,1)    #Move the window
        self.sleep('1')
        
        #Adapter_networkCard
        print 'Click on the Adapter,Select',networkCard_Flag,'network card.'
        h = win32gui.FindWindowEx(hwd, None, 'SysTreeView32', None)
        #print h
        self.Mouse_LB_click(h)
        self.shortcut_keys(['Home'])
        self.shortcut_keys(['Down'])
        self.sleep('1')
        
        #Select network card
        hw = win32gui.FindWindowEx(hwd, None, None, 'Adapter')
        hwn = win32gui.FindWindowEx(hw, None, 'SysTreeView32', None)
        self.Mouse_LB_click(hwn)
        self.shortcut_keys(['Home'])
        self.sleep('1')
        try:
            result = self.select_networkCard(networkCard_Flag)
        except:
            log_public(ERR_OMNIPEEK_START_SELECT_NETWORKCARD_0002)            
            self.m_ERROR_MSG = ERR_OMNIPEEK_START_SELECT_NETWORKCARD_0002
            return False
        
        if result != True:
            print 'Select network card failed'
            #点击取消
            button_hwd = win32gui.FindWindowEx(hwd, None, 'Button', '取消')
            self.Mouse_LB_click(button_hwd)
            self.sleep('1')
            return False
        
        #802.11_channel
        self.sleep('1')
        print 'Begin to choose the channel:',channel
        h = win32gui.FindWindowEx(hwd, None, 'SysTreeView32', None)
        self.Mouse_LB_click(h)
        self.shortcut_keys(['Down'])
        self.sleep('1')
        
        h = win32gui.FindWindowEx(hwd, None, None, '802.11')
        hwnd = win32gui.FindWindowEx(h, None, 'Button', '&Number:')
        self.Mouse_LB_click(hwnd)
        self.sleep('1')
        
        channel_h = win32gui.FindWindowEx(h, None, 'ComboBox', None)
        #print channel_h
        bufLen = 1024
        buf = win32gui.PyMakeBuffer(bufLen)
        n = win32gui.SendMessage(channel_h, win32con.WM_GETTEXT, bufLen, buf)
        #print buf[0:n]
        
        #Determine if there's any available channel
        if n == 0:
            print 'Have no channel to choose'
            #点击取消
            button_hwd = win32gui.FindWindowEx(hwd, None, 'Button', '取消')
            #print button_hwd
            self.Mouse_LB_click(button_hwd)
            #print '点击 取消'
            self.sleep('1')
            return False
        
        if string.atoi(channel) >= 1:
            self.Mouse_LB_click(channel_h)
            try:
                self.selece_Channel(channel)
            except:
                log_public(ERR_OMNIPEEK_START_SELECT_CHANNEL_0003)            
                self.m_ERROR_MSG = ERR_OMNIPEEK_START_SELECT_CHANNEL_0003
                return False
            self.shortcut_keys(['Enter'])
        self.sleep('1')
        print 'Select channel success'
        
        #点击确定
        button = win32gui.FindWindowEx(hwd, None, 'Button', '确定')
        #print 'button :',button
        self.Mouse_LB_click(button)
        self.sleep('8')
        
        #点击Start Capture
        print 'Begin to capture package'
        self.shortcut_keys(['Ctrl','Y'])             #根据快捷键点击
        self.sleep(timesleep)
        print 'After waiting for ',timesleep,'seconds Stop capture package'
        self.shortcut_keys(['Ctrl','Y'])             #点击Stop Capture
        
        return True
        
    def omnipeek_save(self,dst):
        
        result = False
        
        list_1 = ''
        sep = '\\'
        list_1 = dst.split(sep)
        list_1.pop()
        self.filename = sep.join(list_1)
        
        if os.path.exists(self.filename) == False:
            
            msg = "Path does not exist not exists , I will help you mkdir this path:"+self.filename
            print msg
            log_public(msg)
            os.mkdir(self.filename)
            
        self.dst = dst
        
        self.sleep('2')
        h = win32gui.FindWindow("OmniPeek", None)
        win32gui.SetForegroundWindow(h)    #置顶
        self.sleep('5')
        
        print 'Begin to save the test results'
        self.shortcut_keys(['Ctrl','S'])
        self.sleep('2')
        hwd = win32gui.FindWindow(None, '另存为')
        self.sleep('1')
        #print hwd
        
        #判断窗口存在
        if hwd:
            
            self.flag_save = '1'
            win32gui.SetForegroundWindow(hwd)
            edit_list = findControls(hwd,wantedClass='Edit')
            #print edit_list
            for x in edit_list:
                rect_list = win32gui.GetWindowRect(x)
                t_dx = rect_list[2]-rect_list[0]
                t_dy = rect_list[3]-rect_list[1]
                t_tuple = (t_dx ,t_dy)
                if t_tuple ==(224,13): 
                    self.t_hwnd = x
                    break
            if self.t_hwnd == 0:
                h = win32gui.FindWindowEx(hwd, None, 'Button', '取消')
                self.Mouse_LB_click(h)
                result = False
                
            #dst为空，用默认dst
            if self.dst == '':
                path1 = os.path.abspath(sys.argv[0])
                str=path1.split('\\')
                path_parent=str[0]
                self.dst=path_parent +'\\result_'
                
            self.tmp_file = self.dst +'_'+time.strftime(KEY_TIME_FORMAT)
            print 'To save test results to:',self.tmp_file
            
            try:
                setEditText(self.t_hwnd,self.tmp_file)
            except:
                log_public(ERR_SAVE_RESULT_SETEDITTEXT_0004)            
                self.m_ERROR_MSG = ERR_SAVE_RESULT_SETEDITTEXT_0004
                result = False
            self.sleep('1')
            
            print 'Input the file name is successful, click save'    
            self.shortcut_keys(['Alt','S'])   #点击保存按钮
            self.sleep('2')
            result = True
        else:
            print 'No test results can be saved'
            
            result = True
        
        return result
    
    def omnipeek_close(self):
            
        print 'Close the omnipeek application software'
        hwnd = win32gui.FindWindow('OmniPeek',None) 
        win32gui.SetForegroundWindow(hwnd)
        self.shortcut_keys(['Alt','F'])
        self.sleep('1')
        self.shortcut_keys(['X'])
        self.sleep('1')
        
        hwd = win32gui.FindWindow(None,'OmniPeek')
        #print hwd
        #The window exist
        if hwd:
            win32gui.SetForegroundWindow(hwd)    #置顶
            self.sleep('1')
            self.shortcut_keys(['Alt','Y'])
            self.sleep('5')
        
        return True
    
    def omnipeek_test(self,path,networkCard_Flag,channel,timesleep,dst):
        
        if self.omnipeek_start(path,networkCard_Flag,channel,timesleep) == False:
            
            if self.omnipeek_close() == False:
                return False
            return False
        
        if self.omnipeek_save(dst) == False:
            
            if self.flag_save == '1':
                
                print 'Close the omnipeek application software'
                hwnd0 = win32gui.FindWindow('OmniPeek',None)
                win32gui.SetForegroundWindow(hwnd0)
                self.shortcut_keys(['Alt','F'])
                self.sleep('1')
                self.shortcut_keys(['X'])
                self.sleep('1')
                
                hwnd1 = win32gui.FindWindow(None,'OmniPeek')
                #print hwnd1
                if hwnd1:
                    win32gui.SetForegroundWindow(hwnd1)    #置顶
                    self.sleep('1')
                    self.shortcut_keys(['Alt','N'])
                    self.sleep('1')
                
                hwnd2 = win32gui.FindWindow(None,'OmniPeek')
                #print hwnd2
                if hwnd2:
                    win32gui.SetForegroundWindow(hwnd2)    #置顶
                    self.sleep('1')
                    self.shortcut_keys(['Alt','Y'])
                    self.sleep('5')
                    
            return False
        
        if self.omnipeek_close() == False:
            return False
        
        return True
    
if __name__ == "__main__":
    
    test_omnipeek = omnipeek()
    test_omnipeek.omnipeek_test(path = r"C:\Program Files\WildPackets\OmniPeek\OPeek.exe",networkCard_Flag = '2',channel = '6',timesleep = '5',dst = r'E:\we\123')

        

