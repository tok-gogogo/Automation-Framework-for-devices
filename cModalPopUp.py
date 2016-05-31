# -*- coding: gb18030 -*- 
""" 
cModalPopUp.py
Revised: Jan 9th 2006
Developer: plhdpk 
Description: Class to handle pop up windows

Licence: GNU General Public License (GPL)
This software is provided 'as-is', without any express or implied warranty.
In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software.
   If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
"""
# upgrade 2013/03/14,for control twice popup dialog. by chen sheng cong.
# upgrade 2013/04/13,for close IE broswer. by chen sheng cong.

import cPAMIE
import winGuiAuto
import win32gui
import time
import os, sys
import warnings
import threading
import traceback
import pprint

import win32con
import win32api
from public import *

IETITLE = u" -- 网页对话框"
IECLASS = "Internet Explorer_TridentDlgFrame"        
        
warnings.filterwarnings("ignore")

class handlePopup(threading.Thread):
    """ Construct a popup handler thread.
    parameters:
        type      - The type of popup to expect.
        *args     - One or more arguments to handle the popup, usually just a
                    control name such as 'OK' or 'Cancel' works but sometimes a
                    file name or string is needed as well.
    """

    showDebugging = False            # Show debug print lines?

    def __init__(self, type, *args):
        threading.Thread.__init__(self);
        self.wga = winGuiAuto;
        self.wn = win32gui;
        self.popupType = type;
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu'
        path_parent = Getfindpath(path1,findstr)
        autoconfigFile = path_parent + '\\auto_conf\\version.ini'
        autoversion_str = read_ini(autoconfigFile,'Popup_debug','ACweb Debug')
        if autoversion_str.startswith('on')==True:
            self.showDebugging =True
            showDebugging = True
        if type == 'ChooseFile':
            self.command = self.enterTextAndClickControl;
            self.popupName = 'Choose File';
            self.args = args;
        elif type == 'Alert':
            self.command = self.clickControl;
            self.popupName = 'Microsoft Internet Explorer';
            self.args = args;
        elif type == 'Confirm':
            self.command = self.clickControl;
            self.popupName = 'Microsoft Internet Explorer';
            self.args = args;
        elif type == 'Confirm_passwd':
            self.command = self.enterTextPasswdClickControl;
            self.popupName = 'Microsoft Internet Explorer';
            self.args = args;
            
        elif type == 'Prompt':
            self.command = self.enterTextAndClickControl;
            self.popupName = 'Explorer User Prompt';
            self.args = args;            
        else:
            self.command = self.clickControl;
            self.popupName = 'Microsoft Internet Explorer'
            self.args = 'Cancel;'

#    def run(self):
#        """ Override Threading's run() method.  Finds the dialog and calls
#        the required command with the arguments supplied in the constructor.
#        TODO: Need to find an exit strategy if the dialog is not found.
#        parameters:
#            None
#        returns:
#            Nothing
#        """
#        count = 10
#        while(count <> 0):
#            time.sleep(1);
#            try:
#                hwnd = self.wn.FindWindow("#32770", self.popupName)
#               
#               
#                try:
#                   
#                    apply(self.command, (hwnd, self.args,))
#                    time.sleep(1)
#                    return 
#                except:
#                    if self.showDebugging:
#                        (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
#                        print sys.exc_info()
#                        traceback.print_exc(ErrorTB)
#            except:
# 
#                pass
#
#            count -= 1;
#        return

    def run(self):
        """ Override Threading's run() method.  Finds the dialog and calls
        the required command with the arguments supplied in the constructor.
        TODO: Need to find an exit strategy if the dialog is not found.
        parameters:
            None
        returns:
            Nothing
        """
        count = 10
        while(count <> 0):
            time.sleep(2);
            try:
                hwnd = self.wn.FindWindow("#32770", self.popupName)              
                if hwnd != 0 : #not renturn at once
                    try:
                        apply(self.command, (hwnd, self.args,))
                        time.sleep(1)
                        return 
                    except:
                        if self.showDebugging:
                            (ErrorType,ErrorValue,ErrorTB)=sys.exc_info()
                            print sys.exc_info()
                            traceback.print_exc(ErrorTB) 
            except:
                pass
            count -= 1;
        return
    
    def enterTextPasswdClickControl(self, hwnd, args):
        text=args[0];
        control=args[1];
        if self.showDebugging:
            #print "Text and Control is: %s %s" %(text, control)
            x = self.wga.dumpWindow(hwnd) # dump out all the controls
            pprint.pprint(x) # print out all the controls
        inputBoxs = self.wga.findControls(hwnd,
                    wantedClass="Edit")
        
        tmp_hwd =[]
        time.sleep(1)
        #print 'inputBoxs before set:',inputBoxs
        inputBoxs = list(set(inputBoxs))
        #print 'inputBoxs:',inputBoxs
        for x in inputBoxs:
            #print 'x:',x,' edit  :',self.wga.getEditText(x)
            if x in tmp_hwd:
                continue
            else:
                tmp_hwd.append(x)
            #print 'x:',x,'  get:',self.wga.getEditText(x),'  len:',len(self.wga.getEditText(x))
            if len(self.wga.getEditText(x))==1:
                if self.wga.getEditText(x)[0]=='':
                    self.wga.setEditText(x, text)
            else:
                continue
                
            #print 'enterTextPasswdClickControl here'
        time.sleep(.5)
        buttons = self.wga.findControls(hwnd,
                    wantedClass="Button",
                    wantedText=control)
        #time.sleep(1)
        for b in buttons:
            self.wga.clickButton(b)
        
            
    def enterTextAndClickControl(self, hwnd, args):
        """ Used for file choosers or prompt dialogs that enter text into a text box.
            parameters:
                hwnd:       - The handle to the dialog.
                args[0]     - The text to set in the text box in the dialog.
                args[1]     - The button control name.
            returns:
                Nothing
        """
        text=args[0];
        control=args[1];
        
        if self.showDebugging:
            print "Text and Control is: %s %s" %(text, control)
            x = self.wga.dumpWindow(hwnd) # dump out all the controls
            pprint.pprint(x) # print out all the controls
        inputBox = self.wga.findControl(hwnd,
                    wantedClass="Edit")
        self.wga.setEditText(inputBox, text)
        time.sleep(.5)
        buttons = self.wga.findControls(hwnd,
                    wantedClass="Button",
                    wantedText=control)
        print 'buttons:',buttons
        for b in buttons:
            self.wga.clickButton(b)

    def clickControl(self, hwnd, args):
        """ Used for simple dialogs that just have buttons such as 'ok', 'cancel'
            or 'clear'.
            parameters:
                hwnd:       - The handle to the dialog.
                args[0]     - The button control name.
            returns:
                Nothing
        """
        controlText = args[0];
        if self.showDebugging:
            x = self.wga.dumpWindow(hwnd) # dump out all the controls
            pprint.pprint(x) # print out all the controls
        button = self.wga.findControl(hwnd,
                    wantedClass="Button",
                    wantedText=controlText)
        self.wga.clickButton(button)
        
        #find more one time. if find another save name dialog,click it. chen sheng cong/2013/03/14
        time.sleep(1)   
        hwnd = self.wn.FindWindow("#32770", self.popupName)
                        
        if hwnd != 0:
            button = self.wga.findControl(hwnd,
                    wantedClass="Button",
                    wantedText=controlText)
            self.wga.clickButton(button) #for popup two dialogs.       
        
        hwnd = win32gui.FindWindow(IECLASS,IETITLE)
        print "test1",hwnd
        if hwnd != 0:
            print "test2"
            time.sleep(1)     
            win32api.SendMessage(hwnd,win32con.WM_CLOSE,0,0)  
        