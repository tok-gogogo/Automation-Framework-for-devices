#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        telnet_class.py
# Purpose:     telnet class of users
#
# Author:      gongke
#
# Created:     2013/01/13
# RCS-ID:      $Id: telnet_class.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication 
from email.mime.image import MIMEImage
from public import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
import base64
import time 
reload(sys)
sys.setdefaultencoding("utf-8")

class smtpemail:
    def __init__(self,SMTPSERVER='smtp.gmail.com',USERNAME='autotestzoomnet@gmail.com',PASSWORD='Autotest',POSTFIX='autotestzoomnet@gmail.com',DEBUG ='1',PORT='25',TIMEOUT='20'):
        self.username = USERNAME
        self.password = PASSWORD
        self.server = SMTPSERVER
        self.postfix = POSTFIX
        self.debug = string.atoi(DEBUG)
        self.result = False
        self.email_cc =[]
        self.email_to =[]
        self.email_to_fail=[]
        self.port = string.atoi(PORT)
        self.timeout = string.atoi(TIMEOUT)
        self.email_dic={'mailto_list':1,'mailcc_list':2,'mailfrom_user':3,'mailfrom_passwd':4,'mail_smtpserver':5,'mail_timeout':6,'mail_smtpport':7,'send_email_Flag':8,'mailto_fail_list':9}
        self.dic_email_file={}
    
    def send_mail_text(self,to_list=[],cc_list=[],sub='test',content='test',codePlugin = [],version='test',text='test',email_Flag='html'):
        self.email = smtplib.SMTP()
        self.email.set_debuglevel(self.debug)
        
        #msg = MIMEText(content,_subtype='html',_charset='gb2312')
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.postfix
        msg['To']=','.join(to_list)
        msg['Cc']=','.join(cc_list)
        #msg.attach(content)    #ÓÊ¼þÕýÎÄ
        #msg.set_payload(content)
        msg.attach(MIMEText( content, email_Flag ) ) 
        
        test = '\r'+ '\r' + '\r' 
        msg.attach(MIMEText( test ,email_Flag ) )
        
        msg.attach(MIMEText(open(codePlugin[-1]['subject'],"r").read(),_subtype='plain',_charset='gb2312'))
        
        test = '\r'+ '\r' + '\r' 
        msg.attach(MIMEText( test ,email_Flag ) )
        
        for plugin in codePlugin:
            #mitFile =MIMEText(open(plugin['subject']).read())
            #mitFile['Content-Type']='application/octet-stream'
            #tmp_str = 'attachment;filename ="' + plugin['subject'].split('\\')[-1] + '"'
            #mitFile['Content-Disposition']=tmp_str
            mitFile = MIMEApplication( open(plugin['subject'],'rb').read(), )
            mitFile.add_header( 'content-disposition', 'attachment', filename=plugin['subject'].split('\\')[-1] )
            msg.attach( mitFile )
        
        try:
            
            #self.email = smtplib.SMTP(self.server,self.port,self.timeout)
            
            self.email.connect(self.server)
            
            self.email.ehlo()
            self.email.starttls()
            self.email.ehlo()
            
            self.email.login(self.username,self.password)
            self.email.sendmail(self.postfix,to_list,msg.as_string())
            time.sleep(5)
            self.result = True
            
        except Exception,e:
            print str(e)
            self.result =False
            
    def getresult(self):
        if self.result:
            print 'send email success'
        else:
            print 'send email fail'
        return self.result
    
    def close(self):
        self.email.quit()
    
    def read_mail_to_cc_list(self,filename=''):
        #tmp_dic = {}
        #print '***********read_mail_to_cc_list fuction**********'
        if len(filename)==0:
            path1 = os.path.abspath(sys.argv[0])
            filepath = os.path.dirname(path1)
            filepath_lotus = filepath + '\\auto_conf'
            if os.path.exists(filepath_lotus) == False:
                msg = filepath_lotus  + " not exists"
                log_print(msg)
                return False
        filename = filepath_lotus + '\\lotus.conf'
        if os.path.isfile(filename) ==False:
            msg = filename  + " not exists"
            print msg
            info_public(msg)
            return False
        file_object = open(filename,"r")
        textlist = file_object.readlines()
        file_object.close()
        
        self.email_cc =[]
        self.email_to =[]
        lotus_email=''
        lotus_email_people=[]
        #print '*********************'
        for line in textlist:
            lotus_email =(line.split('$'))[0].strip()
            print line
            if self.email_dic.has_key(lotus_email):
                if self.email_dic[lotus_email] == 1:
                    [self.email_to.append(x.strip()) for x in (line.split('$'))[1].split(',')]
                elif self.email_dic[lotus_email] == 2:
                    [self.email_cc.append(x.strip()) for x in (line.split('$'))[1].split(',')]
                elif self.email_dic[lotus_email] == 3:
                    
                    self.username = self.postfix = (line.split('$'))[1].split(',')[0].strip()
                    #print 'self.username,self.postfix',self.username,self.postfix
                elif self.email_dic[lotus_email] == 4:
                    self.password  = (line.split('$'))[1].split(',')[0].strip()
                    #print 'self.password',self.password
                elif self.email_dic[lotus_email] == 5:
                    self.server = (line.split('$'))[1].split(',')[0].strip()
                elif self.email_dic[lotus_email] == 6:
                    self.timeout = (line.split('$'))[1].split(',')[0].strip()
                elif self.email_dic[lotus_email] == 7:
                    self.port  = (line.split('$'))[1].split(',')[0].strip()
                elif self.email_dic[lotus_email] == 8:
                    self.dic_email_file['send_email_Flag']  = (line.split('$'))[1].split(',')[0].strip()
                elif self.email_dic[lotus_email] == 9:
                    [self.email_to_fail.append(x.strip()) for x in (line.split('$'))[1].split(',')]
                    #print 'send_email_Flag:',self.dic_email_file['send_email_Flag']
                    #print '##########################\n'
        self.dic_email_file['mailto_list'] = self.email_to
        self.dic_email_file['mailcc_list'] = self.email_cc
        self.dic_email_file['mailto_fail_list'] = self.email_to_fail
        self.dic_email_file['mail_user'] = self.username
        self.dic_email_file['mail_postfix'] = self.postfix
        self.dic_email_file['mail_passwd'] = self.password
        self.dic_email_file['mail_smtpserver'] = self.server
        self.dic_email_file['mail_timeout'] = self.timeout
        self.dic_email_file['mail_port'] = self.port
        
        #print 'self.dic_email_file:',self.dic_email_file
        #self.dic_email_file={'mailto_list':self.email_to,'mailcc_list':self.email_cc,'mail_user':self.username,'mail_postfix':self.postfix,'mail_passwd':self.password,'mail_smtpserver':self.server,'mail_timeout':self.timeout,'mail_port':self.port}  
        #return tmp_dic
        return True

'''
if __name__=='__main__':
    
    version = 'MIPS_1018R31T2_P18B_ZTE_NETMAX'
    mailto_list=["gongke@zoomnetcom.com","gongke@zoomnetcom.com"]
    mailcc_list=["gongke@zoomnetcom.com","gongke@zoomnetcom.com"]
    sub = 'this is the AC version: ' + version + ' auto test result'
    content ='Dear all:'  +'\r' + 'this is the AC version: '+version +' autoest result'+'\r'+'Please see the Plugin' 
    text='test'
    email_Flag = 'plain'
    codePlugin = [{'subject' : 'E:\\Simu_server\\result\\result__step1_ac_20130311_104552.txt', 'content' : '1abc'}, {'subject' : 'E:\\Simu_server\\result\\result__step1_ac_20130313_104443.txt', 'content' : '2abc'}] 
    testmail = smtpemail()
    testmail.read_mail_to_cc_list()
    print 'testmail.dic_email_file:', testmail.dic_email_file
    mailto_list = testmail.dic_email_file['mailto_list']
    mailcc_list = testmail.dic_email_file['mailcc_list']
    testmail.send_mail_text(mailto_list,mailcc_list,sub,content,codePlugin,version,text,email_Flag)
    testmail.getresult()
'''
            
    