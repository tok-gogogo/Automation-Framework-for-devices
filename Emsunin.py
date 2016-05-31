#!/usr/bin/python 
#coding=gbk
import time
import win32gui
import win32ui
import win32api
import win32con
import os
import shutil
import sys
from pywinauto import application
from pywinauto.controls import HwndWrapper
from pywinauto import *

class uninst_progam:
    def __init__(self,path):
        self.progam_path = path
        #print self.progam_path
    def uninst_EMS_client(self):
        try:
            if (os.path.isfile(self.progam_path) == False):
                print 'The file %s didn\'t exist!!!'% (self.progam_path)
                return
            app = application.Application.start(self.progam_path)
            if (os.path.isfile(self.progam_path) == False):
                print 'The file %s didn\'t exist!!!'% (self.progam_path)
                return
            time.sleep(5)
            #print "start EMS_Client unist progam................."
            WINDOW_TITLE = u"EMS-client 卸载: 确认卸载"
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'卸载(&U)'
            app[WINDOW_TITLE][Bunton].Click()
            #KEY_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            #strTime = time.strftime(KEY_TIME_FORMAT)
            #print strTime
            #WINDOW_TITLE = u"EMS-client 卸载: 卸载文件"
            #app[u"EMS-client 卸载"].Wait('exists',40)
            WINDOW_TITLE = u"EMS-client 卸载"
            cnt = 0
            while cnt<60:
                try:
                    tmp_list = findwindows.find_windows(title=WINDOW_TITLE)
                    #print 'tmp_list:',tmp_list
                    if len(tmp_list)>0:
                        #print 'find the windows title:',WINDOW_TITLE
                        break
                except Exception,e:
                    cnt = cnt + 1
                    time.sleep(1)
                        #print 'not find : ' ,cnt,'  times' 
                    pass    
            #time.sleep(20)
            #strTime = time.strftime(KEY_TIME_FORMAT)
            #print strTime
            
            #app=application.Application().connect_(title_re=WINDOW_TITLE )
            app[WINDOW_TITLE][u'否(&N)'].Click()

            time.sleep(2)
            WINDOW_TITLE = u"EMS-client 卸载: 完成"
            app[WINDOW_TITLE][u'关闭(&L)'].Click()
          
            return "uninst EMS-client complete!!!!!!!"
        except Exception,e:
            print 'Exception:',e
            return "EMS_client uninst fail!!!!"
    def uninst_EMS_server(self):
        try:

            if (os.path.isfile(self.progam_path) == False):
                print 'The file %s didn\'t exist!!!'% (self.progam_path)
                return
            app = application.Application.start(self.progam_path)
            time.sleep(5)
            #print "start the EMS_server unist progam................."
            WINDOW_TITLE = u"CY-EMS-server 卸载: 确认卸载"
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'卸载(&U)'
            app[WINDOW_TITLE][Bunton].Click()
            time.sleep(2)
            
            WINDOW_TITLE = u'CY-EMS-server 卸载: 卸载文件'
            Button = u'关闭(&L)'
            Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
            while(Button_Property['IsEnabled'] == False):
                time.sleep(1)
                Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
                #print Button_Property['IsEnabled']
                
            WINDOW_TITLE = u'CY-EMS-server 卸载: 完成'
            app[WINDOW_TITLE][u'关闭(&L)'].DoubleClick()

            return "uninst EMS-server complete!!!!!!!"
        except Exception,e:
            print 'Exception:',e
            return "EMS_server uninst fail!!!!"
            
#安装网管客户端

class install_progam:
    def __init__(self,path,lisence_path = u'C:\\Documents and Settings\\dell\\桌面\\LISENCE(4).KEY'):
        self.progam_path = path
        self.lisence_path = lisence_path
    def install_EMS_client(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            if (os.path.isfile(self.progam_path) == False):
                print 'The file %s didn\'t exist!!!'% (self.progam_path)
                return

            app = application.Application.start(self.progam_path)
            time.sleep(5)
            #print "start EMS_client install progam................."
            WINDOW_TITLE = u"EMS-client 安装"
        
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].DoubleClick()
            WINDOW_TITLE = u'EMS-client 安装: 软件许可协议'
            #time.sleep(2)
            Bunton = u'我接受“许可证协议”中的条款(&A)'
            app[WINDOW_TITLE][Bunton].DoubleClick()
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()
            WINDOW_TITLE = u'EMS-client 安装: 选择安装位置'
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()
            WINDOW_TITLE = u'EMS-client 安装: 选择“开始菜单”文件夹'
            Button = u'安装(&I)'
            app[WINDOW_TITLE][Button].Click()

    
            #time.sleep(2)
            WINDOW_TITLE = u'EMS-client 安装: 复制文件'
            Button = u'下一步(&N) >'   
            Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
            while(Button_Property['IsEnabled'] == False):
                time.sleep(1)
                Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
                
            WINDOW_TITLE = u'EMS-client 安装: 已完成'
            app[WINDOW_TITLE][Bunton].Click()
            
            WINDOW_TITLE = u'EMS-client 安装: 已完成'
            Bunton = u'关闭'
            app[WINDOW_TITLE][u'关闭'].Click()

            return "EMS_client install success"
            shutil.copy(u'D:\\CYEMS\\client\\bin\\start.bat',u'D:\\CYEMS\\client')
            if (os.path.isfile(self.lisence_path) == False):
                return 'the lisence file isn\'t exists!!'
            else:
                shutil.copy(self.lisence_path,u'D:\\CYEMS\\client')
        except Exception,e:
            print 'Exception:',e
            return "EMS_client install unsuccess!!!!"
        
    def install_EMS_server(self):
        try:
            if (os.path.isfile(self.progam_path) == False):
                print 'The file %s didn\'t exist!!!'% (self.progam_path)
                return
            app = application.Application.start(self.progam_path)
            time.sleep(5)
            #print "start EMS_server install progam................."
            WINDOW_TITLE = u"CY-EMS-server 安装"
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()
            
            WINDOW_TITLE = u"CY-EMS-server 安装: 软件许可协议"
            #time.sleep(2)
            Bunton = u'我接受“许可证协议”中的条款(&A)'
            app[WINDOW_TITLE][Bunton].DoubleClick()
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()
            
            WINDOW_TITLE = u"CY-EMS-server 安装: 选择安装位置"   
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()

            WINDOW_TITLE = u"CY-EMS-server 安装: 选择“开始菜单”文件夹"
            Bunton = u'安装(&I)'
            app[WINDOW_TITLE][Bunton].Click()


            #time.sleep(1)
            WINDOW_TITLE = u"CY-EMS-server 安装: 复制文件"
            Button = u'下一步(&N) >'
            Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
            while(Button_Property['IsEnabled'] == False):
                time.sleep(1)
                Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
                
            #time.sleep(1)
            WINDOW_TITLE = u"CY-EMS-server 安装: 已完成"
            app[WINDOW_TITLE][Button].Click()
            
            Bunton = u'关闭'
            WINDOW_TITLE = u"CY-EMS-server 安装: 安装完成"
            app[WINDOW_TITLE][u'关闭'].Click()

            return "EMS_server install success"
        except Exception,e:
            print 'Exception:',e
            return "EMS_server install unsuccess!!!!"
            

if __name__ == "__main__":

    EMS = u'D:\\CYEMS\\client\\uninst.exe'
    uninst1 = uninst_progam(EMS)
    result = uninst1.uninst_EMS_client()
    print result
    
    EMS = u'E:\\client\\EMS-client(1).exe'
    we = install_progam(EMS)
    result = we.install_EMS_client()
    print result

    '''
    EMS = u'D:\\CYEMS\\server\\uninst.exe'
    uninst1 = uninst_progam(EMS)
    result = uninst1.uninst_EMS_server()
    print result
    
    EMS = u'C:\\Documents and Settings\\dell\\桌面\\EMS-server(2).exe'
    we = install_progam(EMS)
    result = we.install_EMS_server()
    print result
    '''

