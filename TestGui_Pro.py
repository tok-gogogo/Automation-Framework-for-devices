#-*- coding: UTF-8 -*-
import array
import ctypes
import struct

import win32api
import win32con
import win32gui
import win32ui
import os
import sys
import win32process
import win32con
#import win32api
import string
from ctypes import *
import pprint
import random

import time
from win_exec import *
from public import * 
#import commctrl
import types
import pyhk
#import re
import sys
sys.setdefaultencoding("utf-8") 
from pywinauto import *
from win_GUI import *
from py_mysql import *
CYC_Num = 400

def Mac_write(DoingFlag = True,timesleep='2'):
    print 'DoingFlag:',DoingFlag
    print "Mac_write"
    clsname ="MAC地址数据库获取"
    time.sleep(string.atoi(timesleep)*2)
    lresults = findTopWindows(clsname)
    while True:
        
        test = opSQL()
        test.init_sql("host=192.168.22.18")
        #sqlcmd = "update allmactable set Status='unuse' where Status='used'"
        sqlcmd = "select * from allmactable  where Status='used'"
        msg = test.update(sqlcmd)
        test.ModifyTable(msg)
        test.close_mysql() 
          
        lbutton= findControls(lresults[0],wantedText="写入",wantedClass="Button")
        str_a =controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']
        if   str_a == True:
            clickButton(lbutton[0])
        if  DoingFlag ==False:
            time.sleep(string.atoi(timesleep)*3)
            break
        time.sleep(string.atoi(timesleep)*2)
        clsname1 ="ONUtest"
        lresults1 = findTopWindows(clsname1)
        if len(lresults1)>0:
            
            lbutton1= findControls(lresults1[0],wantedClass="Button") 
            if lbutton1==None:
                continue
            if len(lbutton1)>0:
                clickButton(lbutton1[0])
        
    time.sleep(string.atoi(timesleep)*3)
    win32gui.SendMessage(lresults[0],win32con.WM_CLOSE,0,0)
    return True

def Product_test(DoingFlag=True,timesleep='2'):
    print 'DoingFlag:',DoingFlag
    print "Product_test"
    clsname ="当前操作员"
    lresults = findTopWindows(clsname)
    
    while True:
        lbutton= findControls(lresults[0],wantedText="写入",wantedClass="Button")
        print 'lbutton:',lbutton
        str_a =controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']
        if   str_a == True:
            clickButton(lbutton[0])
        print '11111'
        time.sleep(string.atoi(timesleep)*2)
        clsname1 ="ONUtest"
        lresults1 = findTopWindows(clsname1)
        print '111112'
        if len(lresults1)>0:
            lbutton1= findControls(lresults1[0],wantedClass="Button")
            clickButton(lbutton1[0])
        
        print 'DoingFlag:',DoingFlag
        if  DoingFlag ==False:
            time.sleep(string.atoi(timesleep)*2)
            print '111113'
            break
    time.sleep(string.atoi(timesleep)*3)
    while True:
        str_a =controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']
        if   str_a == True:
            win32gui.SendMessage(lresults[0],win32con.WM_CLOSE,0,0)
            break
    return True

def Bar_code(DoingFlag=True,timesleep='2'):
    print 'DoingFlag:',DoingFlag
    print "Bar_code"
    clsname ="打印条形码"
    time.sleep(string.atoi(timesleep)*2)
    lresults = findTopWindows(clsname)
    while True:
        lbutton= findControls(lresults[0],wantedText="确定",wantedClass="Button")
        str_a =controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']
        if   str_a == True:
            clickButton(lbutton[0])
        time.sleep(string.atoi(timesleep)*2)
        clsname1 ="ONUtest"
        lresults1 = findTopWindows(clsname1)
        if len(lresults1)>0:
            lbutton1= findControls(lresults1[0],wantedClass="Button") 
            clickButton(lbutton1[0])
        if  DoingFlag ==False:
            time.sleep(string.atoi(timesleep)*3)
            break
    time.sleep(string.atoi(timesleep)*3)
    win32gui.SendMessage(lresults[0],win32con.WM_CLOSE,0,0)
    return True
def Itester_test(DoingFlag = True,timesleep='2'):
    return True

def Sqlquery_test(DoingFlag=True,timesleep='2'):
    print 'DoingFlag:',DoingFlag
    print "Sqlquery_test"
    time.sleep(string.atoi(timesleep)*2)
    clsname ="数据库查询"
    lresults = findTopWindows(clsname)
    print 'lresults:',lresults
    while True:
        lcontrol= findControls(lresults[0],wantedClass="ComboBox")
        print 'lcontrol:',lcontrol
        value = random.randint(1,controls.win32_controls.ComboBoxWrapper(lcontrol[0]).ItemCount())
        #value = 2
        if value == controls.win32_controls.ComboBoxWrapper(lcontrol[0]).ItemCount():
            value = value - 1
        controls.win32_controls.ComboBoxWrapper(lcontrol[0]).Select(value)
        lcontrol1= findControls(lresults[0],wantedText="查询",wantedClass="Button")
        if controls.win32_controls.ComboBoxWrapper(lcontrol[1]).ItemCount() ==0 :
            clickButton(lcontrol1[1])
        time.sleep(string.atoi(timesleep)*2)
        
        value = random.randint(0,controls.win32_controls.ComboBoxWrapper(lcontrol[1]).ItemCount())
        print 'value1:',value
        lcontrol1= findControls(lresults[0],wantedClass="Button")
        print 'lcontrol1:',lcontrol1
        value = 0
        if value != controls.win32_controls.ComboBoxWrapper(lcontrol[1]).ItemCount():
            #controls.win32_controls.ComboBoxWrapper(lcontrol[0]).Select(value)
            controls.win32_controls.ButtonWrapper(lcontrol1[4]).Check()
            tup1  =  win32gui.GetWindowRect(lcontrol[1])
            print "tup1:",tup1
            win32api.SetCursorPos((tup1[2]-10,tup1[3]+10))
            time.sleep(0.1)
            win32gui.SendMessage(lcontrol[1], win32con.CB_SHOWDROPDOWN,1, 0)
            win32gui.SendMessage(lcontrol[1], win32con.CB_SETCURSEL, 0, 0)
            #win32gui.SendMessage(lcontrol[1], win32con.WM_SETFOCUS, 0, 0 )
            time.sleep(0.1)
            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tup1[2]-10,tup1[3]+10) 
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tup1[2]-10,tup1[3]+10)
            time.sleep(0.1)
            #win32gui.SendMessage(lcontrol[1], win32con.WM_SETFOCUS, 0, 0 )
            #time.sleep(0.1)
        value = random.randint(0,controls.win32_controls.ComboBoxWrapper(lcontrol[2]).ItemCount())
        print 'value2:',value
        value = 0
        if value != controls.win32_controls.ComboBoxWrapper(lcontrol[2]).ItemCount():
            controls.win32_controls.ButtonWrapper(lcontrol1[8]).Check()
            tup1  =  win32gui.GetWindowRect(lcontrol[2])
            win32api.SetCursorPos((tup1[2]-10,tup1[3]+10))
            time.sleep(0.1)
            print "tup2:",tup1
            win32gui.SendMessage(lcontrol[2], win32con.CB_SHOWDROPDOWN, 1, 0)
            win32gui.SendMessage(lcontrol[2], win32con.CB_SETCURSEL, 0, 0)
            #win32gui.SendMessage(lcontrol[2], win32con.WM_SETFOCUS, 0, 0 )
            time.sleep(0.1)
            win32api.SetCursorPos((tup1[2]-10,tup1[3]+10))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,tup1[2]-10,tup1[3]+10) 
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,tup1[2]-10,tup1[3]+10)
            time.sleep(0.1)
            #win32gui.SendMessage(lcontrol[2], win32con.CB_SHOWDROPDOWN, 0, 0)
            #win32gui.SendMessage(lcontrol[2], win32con.WM_SETFOCUS, 0, 0 )
            
            #win32api.SetCursorPos((tup1[2]-10,tup1[3]+10))
            #time.sleep(0.1)
            
            #win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 13, 0 )
            #time.sleep(0.1)
            #win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 13, 0 )
        time.sleep(0.1)
        clickButton(lcontrol1[1])
        if  DoingFlag ==False:
            time.sleep(string.atoi(timesleep)*3)
            break
        time.sleep(string.atoi(timesleep)*30)
        #break
    time.sleep(string.atoi(timesleep)*3)
    win32gui.SendMessage(lresults[0],win32con.WM_CLOSE,0,0)
    return True

def Author_test(DoingFlag = True,timesleep='2'):
    print 'DoingFlag:',DoingFlag
    print "Author_test"
    time.sleep(string.atoi(timesleep))
    clsname ="权限管理界面"
    lresults = findTopWindows(clsname)
    print 'lresults:',lresults
    while True:
        x = None
        lbutton= findControls(lresults[0],wantedClass="Button")
        print 'lbutton:',lbutton
        value = random.randint(1,3)
        if value==1:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') ==r'单板测试':
                    if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                elif str_a[0].encode('gb2312') ==r'整机测试':
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
                elif str_a[0].encode('gb2312') ==r'维修测试':
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
        elif value==2:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') ==r"单板测试":
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
                elif str_a[0].encode('gb2312') ==r"整机测试":
                    if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                        controls.win32_controls.ButtonWrapper(x).Check()
                elif str_a[0].encode('gb2312') ==r"维修测试":
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
        elif value==3:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') ==r"单板测试":
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
                elif str_a[0].encode('gb2312') ==r"整机测试":
                    controls.win32_controls.ButtonWrapper(x).UnCheck()
                elif str_a[0].encode('gb2312') ==r"维修测试":
                    if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
        
        for x in lbutton:
            str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
            if str_a[0].encode('gb2312') ==r"单板测试":
                continue
            elif str_a[0].encode('gb2312') ==r"整机测试":
                continue
            elif str_a[0].encode('gb2312') ==r"维修测试":
                continue
            else:
                controls.win32_controls.ButtonWrapper(x).UnCheck()
        for z in range(0,3):
            value = random.randint(1,5)
            if value==1:
                for x in lbutton:
                    str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                    if str_a[0].encode('gb2312') ==r"权限修改权限":
                        if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                        break
            elif value==2:
                for x in lbutton:
                    str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                    if str_a[0].encode('gb2312') ==r"产品测试权限":
                        if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                        break
            elif value==3:
                for x in lbutton:
                    str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                    if str_a[0].encode('gb2312') ==r'启动itester权限':
                        if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                        break
            elif value==4:
                for x in lbutton:
                    str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                    if str_a[0].encode('gb2312') ==r'mac写入权限':
                        if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                        break
            elif value==5:
                for x in lbutton:
                    str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                    if str_a[0].encode('gb2312') ==r'打印条码':
                        if controls.win32_controls.ButtonWrapper(x).GetCheckState()==0:
                            controls.win32_controls.ButtonWrapper(x).Check()
                        break
                    
        clsname ="权限管理界面"
        lresults1 = findTopWindows(clsname)
        lcontrol= findControls(lresults1[0],wantedClass="RichEdit20A") 
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        value = random.randint(2,10)
        TYPE  = ''.join(random.sample(chars,value))
        setEditText(lcontrol[0],TYPE) 
        for x in lbutton:
            str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
            if str_a[0].encode('gb2312') ==r'确定':
                clickButton_Post(x)
                break
        value = random.randint(1,2)
        time.sleep(string.atoi(timesleep)*2)
        clsname = r"提示"
        lresults2 = findTopWindows(clsname)
        print 'lresults2:',lresults2
        if len(lresults2)>0:
            if value == 1:
                lcontrol= findControls(lresults2[0],wantedText="确定",wantedClass="Button")
            else:
                lcontrol= findControls(lresults2[0],wantedText="取消",wantedClass="Button")
            clickButton(lcontrol[0])
        if DoingFlag==False:
            break
    time.sleep(string.atoi(timesleep)*3)
    win32gui.SendMessage(lresults[0],win32con.WM_CLOSE,0,0)
    return True

def Product_Run_Mac_new(app='F:\\code\\zhangping\\Release0113\\Release\\ONUtest.exe',UseName="zhangpin",Passwd="123456",TYPE="ONU",RandFlag='1',timesleep='2',DoingFlagstr='TRUE'):
    test_win = win_gui()
    os.chdir(os.path.dirname(app))
    
    test_win.startapp_chdir(app)
    print "Path dir:",os.getcwd()
    app_winauto = Application()
    app_winauto.connect_(path = app)
    clsname ="欢迎使用高锐产测工具"
    lresults = 0
    while True:
        try:
            lresults = findTopWindows(clsname)
            if lresults>0:
                break
        except Exception,e:
            pass
        time.sleep(2)
    leditcontrols = findControls(lresults[0],wantedClass="Edit")
    l2=[]
    for i in leditcontrols:
        if i not in l2:
            l2.append(i)
    #l2.append(i) for i in leditcontrols if not i in l2]
    #setEditText(l2[3],TYPE)
    #setEditText(l2[0],UseName)
    setEditText(l2[1],Passwd)
    time.sleep(4)
    
    lbutton= findControls(lresults[0],wantedText="登录",wantedClass="Button")
    for x in lbutton:
        str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
        if str_a[0].encode('gb2312') =='登录':
            clickButton(x)
            break
        
    '''
    time.sleep(3)
    clsname ="ONUtest"
    lresults = findTopWindows(clsname)
    print 'lresults2222:',lresults
    
    for x in lresults:
        lbutton= findControls(x,wantedText="确定",wantedClass="Button")
        print 'lbutton:',lbutton
        if len(lbutton)>0:
            clickButton(lbutton[0])
            break
    time.sleep(2) 
    clsname ="欢迎使用高锐产测工具"
    lresults = findTopWindows(clsname)
    
    leditcontrols = findControls(lresults[0],wantedClass="Edit")
    print 'leditcontrols:',leditcontrols
    l2=[]
    for i in leditcontrols:
        if i not in l2:
            l2.append(i)
    #l2.append(i) for i in leditcontrols if not i in l2]
    #setEditText(l2[3],TYPE)
    #setEditText(l2[0],UseName)
    setEditText(l2[1],Passwd)
    time.sleep(4)
   
    
    lbutton= findControls(lresults[0],wantedText="登录",wantedClass="Button")
    for x in lbutton:
        str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
        if str_a[0].encode('gb2312') =='登录':
            clickButton(x)
            break
    '''
    clsname ="测试导航"
    lresults = 0
    time.sleep(2)
    while True:
        print 'Op 测试导航'
        try:
            lresults = findTopWindows(clsname)
            print 'lresults111:',lresults
            if lresults>0:
                break
        except Exception,e:
            pass
        time.sleep(2)
    
    while True:
        lbutton = 0;
        print 'Op mac地址操作'
        try:
            
            lbutton= findControls(lresults[0],wantedText="mac地址操作",wantedClass="Button")
            print 'lbutton:',lbutton
            if len(lbutton)>0:
                clickButton_Post(lbutton[0])
                break
        except Exception,e:
            print e;
            pass
        time.sleep(2)
    
    lresults = 0
    while True:
        print 'Op MAC地址数据库获取'
        try:
            clsname ="MAC地址数据库获取"
            lresults = findTopWindows(clsname)
            print 'lresults:',lresults
            if lresults>0:
                break
        except Exception,e:
            print e
            pass
        time.sleep(2)
    StopFlag = False
    while True:
        print 'Op MAC'
        while True:
            print 'Op writepn'
            leditcontrols = 0
            try:
                leditcontrols = findControls(lresults[0],wantedClass="RichEdit20A")
                print 'leditcontrols:',leditcontrols
                if len(leditcontrols)>0:
                    break
            except Exception,e:
                print e
                pass
            time.sleep(2)
        
        value_cyc ='cys'
        global CYC_Num;
        CYC_Num =CYC_Num+1
        value_cyc=value_cyc+str(CYC_Num)
        setEditText(leditcontrols[1],value_cyc)
        time.sleep(5)
        while True:
            print 'Op pnbutton'
            lbutton = 0;
            try:
                lbutton= findControls(lresults[0],wantedText="PN写入",wantedClass="Button")
                print 'lbutton:',lbutton
                if len(lbutton)>0:
                    if controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']==True:
                        clickButton_Post(lbutton[0])
                        break
            except Exception,e:
                print e
                pass
            time.sleep(10)
    
        while True:
            lbutton = 0;
            print 'Op MAC写入'
            try:
                lbutton= findControls(lresults[0],wantedText="MAC写入",wantedClass="Button")
                print 'lbutton:',lbutton
                if len(lbutton)>0:
                    print 'Button status:', controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']
                    if controls.win32_controls.ButtonWrapper(lbutton[0]).GetProperties()['IsEnabled']==True:
                        clickButton_Post(lbutton[0])
                        break
            except Exception,e:
                pass
            time.sleep(10)
        
        while True:
            leditcontrols = findControls(lresults[0],wantedClass="RichEdit20A")
            if getEditText(leditcontrols[0])[-2].find('此次MAC写')>-1:
                if len(getEditText(leditcontrols[2])[0])>0:
                    if getEditText(leditcontrols[2])[0].find('失败')>0:
                        StopFlag = True
                time.sleep(15)
                break
            else:
                time.sleep(15)
                continue
        if StopFlag:
            break
        
        
    
    
def Product_Run(app='E:\\VCDll\\ONUtest1028\\ONUtest\\Debug\\ONUtest.exe',UseName="zhangpin",Passwd="123456",TYPE="ONU",RandFlag='1',timesleep='2',DoingFlagstr='TRUE'):
    test_win = win_gui()
    
    os.chdir(os.path.dirname(app))
    test_win.startapp(app)
    app_winauto = Application()
    app_winauto.connect_(path = app)
    value = 1
    clsname ="欢迎使用高锐产测工具"
    lresults = findTopWindows(clsname)
    Doflag = False
    if DoingFlagstr=="TRUE":
        Doflag = True
   
    leditcontrols = findControls(lresults[0],wantedClass="Edit")
    l2=[]
    [l2.append(i) for i in leditcontrols if not i in l2]
    setEditText(l2[2],TYPE)
    setEditText(l2[0],UseName)
    setEditText(l2[1],Passwd)
    
    
    time.sleep(string.atoi(timesleep))
    
    lbutton= findControls(lresults[0],wantedText="登录",wantedClass="Button")
    
    time.sleep(string.atoi(timesleep))
    for x in lbutton:
        str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
        print  'str_a:',str_a[0].encode('gb2312')
        if str_a[0].encode('gb2312') =='登录':
            clickButton(x)
            break
            
    if RandFlag=='0':
        value = random.randint(1,6)
    elif RandFlag=='1':
        value = 1
    elif RandFlag =='2':
        value = 2
    elif RandFlag =='3':
        value = 3
    elif RandFlag =='4':
        value = 4
    elif RandFlag =='5':
        value = 5
    elif RandFlag =='6':
        value = 6
    else:
        print "Error:the button not find!!!!"
    time.sleep(string.atoi(timesleep)*2)
    clsname ="测试导航"
    lresults = findTopWindows(clsname)
    
    lbutton= findControls(lresults[0],wantedClass="Button")
    
    print 'value:',value
    num = 0
    while True:
        if RandFlag=='0':
            value = random.randint(1,6)
        if value == 1:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='mac地址操作':
                    clickButton_Post(x)
                    Mac_write(DoingFlag =Doflag)
                    break
        elif value ==2:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='整机测试':
                    clickButton_Post(x)
                    Product_test(DoingFlag =Doflag)
                    break
            
            
        elif value == 3:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='条码打印':
                    clickButton_Post(x)
                    Bar_code(DoingFlag =Doflag)
                    break
        elif value ==4:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='itester对接':
                    clickButton_Post(x)
                    Itester_test(DoingFlag =Doflag)
                    break
            
        elif value ==5:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='权限管理':
                    clickButton_Post(x)
                    Author_test(DoingFlag =Doflag)
                    break
        elif value ==6:
            for x in lbutton:
                str_a =controls.win32_controls.ButtonWrapper(x).GetProperties()['Texts']
                if str_a[0].encode('gb2312') =='数据库查询':
                    clickButton_Post(x)
                    Sqlquery_test(DoingFlag =Doflag)
                    break
        num+=1
        print 'run total:',num, ' nums'
        time.sleep(string.atoi(timesleep))
        #break
            
    
    
if __name__ == "__main__": 
    
    #TestPath =raw_input("please input the produce path:")
    #Product_Run(TestPath)
    TestPath = 'F:\\code\\zhangping\\ReleaseNOreset0113\\Release\\ONUtest.exe'
    Product_Run_Mac_new(TestPath)