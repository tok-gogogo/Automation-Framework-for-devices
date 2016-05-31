#!/usr/bin/python 
#-*- coding: UTF-8 -*- 
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
from public import *

class EMS_uninst_install:
    def __init__(self,path,license_path = u'C:\\Documents and Settings\\dell\\桌面\\LISENCE(4).KEY'):
        self.progam_path = path
        self.license_path = license_path

    def uninst_EMS_client(self):
        result = {'result':False,'report':""}
        try:
            if (os.path.isfile(self.progam_path) == False):
                result['result'] = False
                result['report'] = 'The file ' +self.progam_path+' didn\'t exist!!!'
                return result 
            app = application.Application.start(self.progam_path)

            time.sleep(5)

            WINDOW_TITLE = u"EMS-client 卸载: 确认卸载"
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'卸载(&U)'
            app[WINDOW_TITLE][Bunton].Click()
            WINDOW_TITLE = u"EMS-client 卸载"
            cnt = 0
            while cnt<60:
                try:
                    tmp_list = findwindows.find_windows(title=WINDOW_TITLE)
                    if len(tmp_list)>0:
                        break
                except Exception,e:
                    cnt = cnt + 1
                    time.sleep(1)
                    pass    

            app[WINDOW_TITLE][u'否(&N)'].Click()

            time.sleep(2)
            WINDOW_TITLE = u"EMS-client 卸载: 完成"
            app[WINDOW_TITLE][u'关闭(&L)'].Click()
            result['result'] = True
            result['report'] = "uninst EMS-client complete!"
            return result

        except Exception,e:
            print 'Exception:',e
            result['result'] = False
            result['report'] = "EMS_client uninst fail!!!!"
            return result
    def uninst_EMS_server(self):
        result = {'result':False,'report':""}
        try:
            if (os.path.isfile(self.progam_path) == False):
                result['result'] = False
                result['report'] = 'The file ' +self.progam_path+' didn\'t exist!!!'
                return result
 
            app = application.Application.start(self.progam_path)
            time.sleep(5)
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
                
            WINDOW_TITLE = u'CY-EMS-server 卸载: 完成'
            app[WINDOW_TITLE][u'关闭(&L)'].DoubleClick()
            
            result['result'] = True
            result['report'] = "uninst EMS-server complete!"
            return result
        except Exception,e:
            print 'Exception:',e
            result['result'] = False
            result['report'] = "EMS_server uninst fail!!!!"
            return result 

    def install_EMS_client(self):
        result = {'result':False,'report':""}
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            if (os.path.isfile(self.progam_path) == False):
                result['result'] = False
                result['report'] = 'The file ' +self.progam_path+' didn\'t exist!!!'
                return result

            app = application.Application.start(self.progam_path)
            time.sleep(5)
            #print "start EMS_client install progam................."
            WINDOW_TITLE = u"EMS-client 安装"
        
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].DoubleClick()
            WINDOW_TITLE = u'EMS-client 安装: 软件许可协议'
            
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

            WINDOW_TITLE = u'EMS-client 安装: 复制文件'
            Button = u'下一步(&N) >'   
            Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
            while(Button_Property['IsEnabled'] == False):
                time.sleep(1)
                Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
                
            WINDOW_TITLE = u'EMS-client 安装: 已完成'
            app[WINDOW_TITLE][Bunton].Click()
            
            WINDOW_TITLE = u'EMS-client 安装: 安装完成'
            Bunton = u'关闭'
            app[WINDOW_TITLE][u'关闭'].Click()


            shutil.copy(u'D:\\CYEMS\\client\\bin\\start.bat',u'D:\\CYEMS\\client')
            if (os.path.isfile(self.license_path) == False):
                result['result'] = False
                result['report'] = 'EMS_client install success but the license file isn\'t exists!!'
                return result
            else:
                shutil.copy(self.license_path,u'D:\\CYEMS\\client')
                
            result['result'] = True
            result['report'] = "EMS_client install success"
            return result
        except Exception,e:
            print 'Exception:',e
            result['result'] = False
            result['report'] = "EMS_client install unsuccess!"
            return result
            #return "EMS_client install unsuccess!!!!"
        
    def install_EMS_server(self):
        result = {'result':False,'report':""}
        try:
            if (os.path.isfile(self.progam_path) == False):
                result['result'] = False
                result['report'] = 'The file ' +self.progam_path+' didn\'t exist!!!'
                return result
            app = application.Application.start(self.progam_path)
            time.sleep(5)
 
            WINDOW_TITLE = u"CY-EMS-server 安装"
            app=application.Application().connect_(title_re = WINDOW_TITLE )
            Bunton = u'下一步(&N) >'
            app[WINDOW_TITLE][Bunton].Click()
            
            WINDOW_TITLE = u"CY-EMS-server 安装: 软件许可协议"

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

            WINDOW_TITLE = u"CY-EMS-server 安装: 复制文件"
            Button = u'下一步(&N) >'
            Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
            while(Button_Property['IsEnabled'] == False):
                time.sleep(1)
                Button_Property = HwndWrapper.HwndWrapper(app[WINDOW_TITLE][Button]).GetProperties()
                
            WINDOW_TITLE = u"CY-EMS-server 安装: 已完成"
            app[WINDOW_TITLE][Button].Click()
            
            Bunton = u'关闭'
            WINDOW_TITLE = u"CY-EMS-server 安装: 安装完成"
            app[WINDOW_TITLE][u'关闭'].Click()
            
            result['result'] = True
            result['report'] = "EMS_server install success"
            return result
            #return "EMS_server install success"
        except Exception,e:
            print 'Exception:',e
            result['result'] = False
            result['report'] = "EMS_server install unsuccess!"
            return result
            #return "EMS_server install unsuccess!!!!"
            
    def ems_op(self,keyword,filename=ur'C:\Documents and Settings\dell\桌面\temp.ini'):
        try:
            cmd = 'self.'+keyword.strip()
            report = apply(eval(cmd),()) 
            log_print(report)
            result  = self.reporterlog(filename,report)
            return result
        except Exception,e:
            print e
            return False
        
        
    def reporterlog(self,filename,report):
        dic = {'uninst_EMS_client':'EMS-client_uninst',
               'install_EMS_client':'EMS-client_install',
               'uninst_EMS_server':'EMS-server_uninst',
               'install_EMS_server':'EMS-server_install'}
        str_be = ''
        if report['report'].find('uninst')>-1:
            str_be  = 'uninst'
        else:
            str_be  = 'install'
        
        if report['report'].find('server')>-1:
            str_af  = 'server'
        else:
            str_af  = 'client'
        key = str_be + '_EMS_'+str_af
        meth = 'self.' + key
        log_op = reporter(filename)
        if report['result']==True:
            restr ='True'
        else:
            restr ='False'
        if replaceini(filename,'result',dic[key],restr)==False:
            log_op.append(dic[key],report)
        else:
            replaceini(filename,'report',dic[key],report['report'])
        return report['result']
        
        
            
class reporter:
    def __init__(self,filename):
        self.filename = filename
    def write(self,project,report):
        f = open(self.filename,'w')
        s = '[' + project + ']' + '\n'
        if report['result'] == True:
            s = s + 'result = True\n' + 'report = ' + report['report'] + '\n'
        else:
            s = s + 'result = False\n'+'report = ' + report['report'] + '\n'
        f.write(s)
        f.close()
    def append(self,project,report):
        f = open(self.filename,'a')
        f.write('[' + project + ']' + '\n')
        if report['result'] == True:
            s = 'result = True\n'+'report = '+report['report']+'\n'
        else:
            s = 'result = False\n'+'report = '+report['report']+'\n'
        f.write(s)
        f.close()

if __name__ == "__main__":
    filename = ur'C:\Documents and Settings\dell\桌面\temp.ini'
    EMS = u'D:\\CYEMS\\client\\uninst.exe'
    uninst1 = EMS_uninst_install(EMS)
    print uninst1.ems_op('uninst_EMS_client')
    EMS = ur'E:\client\EMS-client(1).exe'
    license_path = ur'E:\client\LISENCE.KEY'
    we = EMS_uninst_install(EMS,license_path)
    print we.ems_op('install_EMS_client')
    '''
    report = reporter(filename)
    project = 'EMS-client_uninst'
    EMS = u'D:\\CYEMS\\client\\uninst.exe'
    uninst1 = EMS_uninst_install(EMS)
    result = uninst1.uninst_EMS_client()
    print 'result:',result
    report.write(project,result)
    print 'report:',report.append(project,result)
    
    EMS = ur'E:\client\EMS-client(1).exe'
    license_path = ur'E:\client\LISENCE.KEY'
    project = 'EMS-client_install'
    we = EMS_uninst_install(EMS)
    result = we.install_EMS_client()
    print 'result:',result
    report.append(project,result)
    print 'report:',report.append(project,result)
    '''

    '''
   
    EMS = u'D:\\CYEMS\\server\\uninst.exe'
    project = 'EMS-server_uninst'
    uninst1 = EMS_uninst_install(EMS)
    result = uninst1.uninst_EMS_server()
    report.append(project,result)
    #print result['report']
    
    EMS = u'C:\\Documents and Settings\\dell\\桌面\\EMS-server(2).exe'
    project = 'EMS-server_install'
    we = EMS_uninst_install(EMS)
    result = we.install_EMS_server()
    report.append(project,result)
    #print result['report']
    '''

