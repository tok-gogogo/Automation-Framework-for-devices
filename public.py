 #-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        public.py
# Purpose:     public  fuction
#
# Author:      gongke
#
# Created:     2013/01/15
# RCS-ID:      $Id: public.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import time
import os
import logging
from logging import handlers
import re   
import filecmp
import sys
from SMTP_email import *
import shutil
from stat import ST_CTIME, ST_MTIME
from types import *
import base64
import hashlib
import traceback

import xlrd
import sys,ConfigParser

#sys.setdefaultencoding("utf-8")

copyFileCounts  = 0 
WIDTH_STR = 25
WIDTH_STR_VALUE = 80
KEY_TIME_FORMAT_PUBLIC = "%Y%m%d%H%M%S" 

def read_ini(file,keyword,param):
    configfp = None
    try:
        configfp = open(file,"r")
    except IOError:
            msg = file + " is not found"
            log_print(msg)
    config = ConfigParser.ConfigParser()
    config.readfp(configfp)
    configfp.close()
    try:
        tmpstr = config.get(param,keyword)
        msg = 'file:'+file+' ,param:' + param+' , keyword:'+keyword +' ,value:' +tmpstr
        #log_print(msg)
        return tmpstr
    except ConfigParser.NoOptionError:
        msg = keyword + "not found under section "+param + ' in ' + file
        log_print(msg)
        return ''
    
    
def get_readvalue(keyword='OS',model = 'OS SYSTEM'):
    path1 = os.path.abspath(sys.argv[0])
    findstr = 'Simu'
    path_parent = Getfindpath(path1,findstr)
    autoconfigFile = path_parent + '\\auto_conf\\version.ini'
    return read_ini(autoconfigFile,keyword,model).strip()
    

def encrypt(key, s): 
    b = bytearray(str(s).encode("gbk")) 
    #print b
    n = len(b) # 求出 b 的字节数 
    c = bytearray(n*2) 
    j = 0 
    for i in range(0,n): 
        b1 = b[i] 
        b2 = b1 ^ key # b1 = b2^ key 
        c1 = b2 % 16 
        c2 = b2 // 16 # b2 = c2*16 + c1 
        c1 = c1 + 65 
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码 
        c[j] = c1 
        c[j+1] = c2 
        j = j+2 
    #print c.decode("gbk")
    return c.decode("gbk") 
 
def decrypt(key, s): 
    c = bytearray(str(s).encode("gbk")) 
    n = len(c) # 计算 b 的字节数 
    if n % 2 != 0 : 
        return "" 
    n = n // 2 
    b = bytearray(n) 
    j = 0 
    for i in range(0, n): 
        c1 = c[j] 
        c2 = c[j+1] 
        j = j+2 
        c1 = c1 - 65 
        c2 = c2 - 65 
        b2 = c2*16 + c1 
        b1 = b2^ key 
        b[i]= b1 
    #print(b.decode("gbk"))
    try: 
        return b.decode("gbk") 
    except: 
        return "failed" 

def checktime():
    key = 11
    model = 'Encryption'
    keyword = 'En1'
    key_other='1234567089'
    value = decrypt(key,decrypt(key,get_readvalue(keyword,model)))
    #print get_readvalue(keyword,model)
    #value = base64.b64decode(value)
    strTime = time.strftime(KEY_TIME_FORMAT_PUBLIC)
    strTime = strTime+key_other
    #print string.atoi(value),string.atoi(strTime)
    print string.atoi(strTime[:12])
    print string.atoi(value[:12])
    if string.atoi(strTime[:12])<=string.atoi(value[:12]):
        return True
    
    return False
'''
def checktime():
    model = 'Encryption'
    keyword = 'En1'
    msg = base64.b64decode(get_readvalue(keyword,model))
    print 'msg',msg
    time_value = base64.b64decode(msg)
    strTime = time.strftime(KEY_TIME_FORMAT_PUBLIC)
    if string.atoi(strTime)<=string.atoi(strTime):
        return True
    #encoded1 = base64.b64encode(strTime)
    return False
'''
   
def Calculation(mac,time_get='20150431232323'):
    key = 11
    key_other='1234567089'
    key_mac = ' Company:cykj Build id: 201403032515 Name:AutoTestTool'
    mac = mac + key_mac
    msg = hashlib.md5(mac).hexdigest()
    msg = hashlib.md5(msg).hexdigest()
    print 'Getvalue md5:',msg
    time_get =time_get +key_other
    msg = encrypt(key,encrypt(key,time_get))
    #msg = base64.b64encode(msg)
    print 'time msg:',msg

    

def checkVersion_PC(version_os ='English'):
    model = 'Encryption'
    keyword = 'En2'
    mac_list = get_mac(version_os)
    #print 'mac_list:',mac_list
    if mac_list ==None:
        return False
    for x in mac_list:
        x = x + ' Company:cykj Build id: 201403032515 Name:AutoTestTool'
        #print 'get:',get_readvalue(keyword,model)
        #print 'Getvalue:',hashlib.md5(hashlib.md5(x).hexdigest()).hexdigest()
        if hashlib.md5(hashlib.md5(x).hexdigest()).hexdigest() == get_readvalue(keyword,model).strip():
            return True
    return False
    
def get_mac(version_os ='English'):
    #print 'version_os:',version_os
    #print os.name
    if os.name == 'nt':
        try:
            
            CmdLine = 'ipconfig /all'
            r = os.popen(CmdLine).read()
            #    print r
            #print 'find:','物理地址.*?([0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2})'.decode('utf8')
            if r:
                if version_os=='English':
                    L = re.findall('Physical Address.*?([0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2})', r)
                elif version_os=='zhangli':
                    L=['20-1A-06-7C-4B-58']
                elif version_os=='zha':
                    L=['3C-97-0E-FE-9A-0D']
                else:
                    L = re.findall('物理地址.*?([0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2}-[0-9,A-F]{2})'.decode('utf8'), r)
                #print 'MAC:',L
                return L
        except:
            pass
        
    elif os.name == "posix":
        try:
            ret = ''
            CmdLine = 'ifconfig'
            r = os.popen(CmdLine).read()
            print r
            if r:
                L = re.findall('HWaddr.*?([0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2}:[0-9,A-F]{2})', r)
                return L
        except:
            pass
    else:
        pass
    return None


    
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]            
def Bin2toDec(string_num):
    #binary to dec
    return str(int(string_num,2))

def DectoBin2(string_num):
    #dec to binary
    num = int(string_num)
    mid=[]
    while True:
        if num==0:
            break
        num,rem=divmod(num,2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])
    
def HextoDec(string_num):
    #hex to dec
    return str(int(string_num.upper(), 16))
         
def DectoHex(string_num):
    #Dec to hex
    num = int(string_num)
    mid=[]
    while True:
        if num==0:
            break
        num,rem=divmod(num,16)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])

def HextoBin2(string_num):
    #hex to binary
    return DectoBin2(HextoDec(string_num.upper()))

def Bin2toHex(string_num):
    #binary to hex
    return DectoHex(Bin2toDec(string_num))

def del_file_path(path='C:\\Documents and Settings\\dell\\Local Settings\\Temp',start ='tmp'):
    rootdir=path
    for f in os.listdir(rootdir):
        if f.startswith(start)==True:
            filepath = os.path.join( rootdir, f )
            if os.path.isfile(filepath):
                os.remove(filepath)
                print filepath+" removed!"
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath,True)
                print "dir "+filepath+" removed!"
        
        
def ip_to_int(str_ip):
    sum = 0
    for j,i in enumerate(str_ip.split('.')[::-1]):
        sum=sum + 256**j*string.atoi(i)
    return sum

def int_to_ip(num):
    str_num =''
    for i in range(3,-1,-1):
        if i==3:
            str_num= str(num/256**i%256)
        else:
            str_num = str_num+'.'+ str(num/256**i%256)
    return str_num
        
def ip_increase_param(ip_addr,step):
    return int_to_ip(ip_to_int(ip_addr) + step)
    
def mac_increase_param_13(mac_addr1='ffffffffffff',mac_addr2='000000000001',num_step=1):
    mac_int1 = HextoDec(mac_addr1)
    mac_int2 = HextoDec(mac_addr2).lstrip('0')
    mac_int1=string.atoi(mac_int1) + string.atoi(mac_int2)*num_step
    mac_addr_new = DectoHex( str(mac_int1))
    if mac_addr_new =='1000000000000':
        mac_addr_new='1'
    mac_addr_new =mac_addr_new.rjust(12,'0')
    tmp_list =[]
    num = 2
    while True:
        tmp_list.append(mac_addr_new[num-2:num])
        num = num +2
        if num >12:
            break
    mac_addr_new=''.join(tmp_list)
    return mac_addr_new
def mac_increase_param(mac_addr1='ff:ff:ff:ff:ff:ff',mac_addr2='00:00:00:00:00:01',num_step=1):
    separator =':'
    separator1 = ':'
    if mac_addr1.find(':')>-1:
        separator =':'
    elif mac_addr1.find('-')>-1:
        separator ='-'
    if mac_addr2.find(':')>-1:
        separator1 =':'
    elif mac_addr2.find('-')>-1:
        separator1 ='-'
    mac_list1 = mac_addr1.split(separator)
    mac_list2 =  mac_addr2.split(separator1)
    mac_int1 = HextoDec(('').join(mac_list1))
    mac_int2 = HextoDec(('').join(mac_list2)).lstrip('0')
    mac_int1=string.atoi(mac_int1) + string.atoi(mac_int2)*num_step
    mac_addr_new = DectoHex( str(mac_int1))
    if mac_addr_new =='1000000000000':
        mac_addr_new='1'
    mac_addr_new =mac_addr_new.rjust(12,'0')
    tmp_list =[]
    num = 2
    while True:
        tmp_list.append(mac_addr_new[num-2:num])
        num = num +2
        if num >12:
            break
    mac_addr_new = separator.join(tmp_list)
    return mac_addr_new

def del_relist(list_l):
    re_list=[]
    for x in list_l:
        if x not in re_list:
            re_list.append(x)
    return re_list

def mac_increase(mac_addr='ff:ff:ff:ff:ff:ff',step = 1):
    separator =':'
    if mac_addr.find(':')>-1:
        separator =':'
    elif mac_addr.find('-')>-1:
        separator ='-'
    mac_list = mac_addr.split(separator)
    mac_int = HextoDec(('').join(mac_list))
    mac_int=string.atoi(mac_int) + step
    mac_addr_new = DectoHex( str(mac_int))
    if mac_addr_new =='1000000000000':
        mac_addr_new='1'
    mac_addr_new =mac_addr_new.rjust(12,'0')
    tmp_list =[]
    num = 2
    while True:
        tmp_list.append(mac_addr_new[num-2:num])
        num = num +2
        if num >12:
            break
    mac_addr_new = separator.join(tmp_list)
    return mac_addr_new
        
        
def log_print(mes,Flag_Except=False):
    print mes
    if Flag_Except==True:
        log_print(repr(sys.exc_info()))
        log_print(repr(traceback.format_exc()))
    sys.stdout.flush()
    info_public(mes)

def write_tmp_file(msg,path1='\\dist\\tmp_date\\tmp_param_jiaob.ini',path2='\\tmp_date\\tmp_param_jiaob.ini'):
    while True:
        try:
            tmp_path = os.path.abspath(sys.argv[0])
            if tmp_path.find('dist')>-1:
                tmp_path = find_parentpath() +path1
            else:
                tmp_path = find_parentpath() +path2
            fp_object = open(tmp_path,'w')
            msg = msg +'\r\n'
            fp_object.writelines(msg)
            fp_object.close()
            break
        except Exception ,e:
            log_print(e)
            pass
        
    
def info_public(s,LogPath='c:\Simu_server\AutoTestLog.log'):
    #global LOG
    #create log object
    if (os.path.isfile(LogPath))==False:
        path1 = os.path.abspath(sys.argv[0])
        filepath = os.path.dirname(path1)
        LogPath = filepath + "\\AutoTestLog.log"
        f=open(LogPath,'a')
        f.close()
    
    
    #filepath_conf = os.path.dirname(os.path.abspath(sys.argv[0])) +'\\auto_conf\\version.ini'
    #if read_ini(filepath_conf,'SendFlag','UDP_SEND').upper().strip()=='ON':
        #Host_Ip = read_ini(filepath_conf,'Localhost','UDP_SEND')
        #handler_udp = logging.handlers.DatagramHandler(Host_Ip,9999)
        #handler_udp.send(repr(s))
        #handler_udp.close()
    
    LOG= logging.getLogger("WtLog")
    #set log level.have 5 kinds.(DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG.setLevel(logging.INFO )
    #create handler,create file name
    handler =logging.FileHandler(LogPath)
    #define format you want to show
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    #input your format
    handler.setFormatter(formatter)
    
    #add your handler
    LOG.addHandler(handler)
    #write log informain
    LOG.info(s)  
    LOG.removeHandler(handler)
    
def get_run_path():
    dir_p = ''
    file = os.path.abspath(sys.argv[0])
    findstr = 'Simu'
    dir_p = Getfindpath(file,findstr)
    return dir_p

def path_Rm_file(path,file_find):
    for root, dirs, files in os.walk(path, False):
        for name in files:
            if name.find(file_find)>-1:
                os.remove(os.path.join(root, name))
    return True




def path_Rm(path):
    for root, dirs, files in os.walk(path, False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    return True

def path_copy(Oldpath,Newpath):
    os.chdir(Oldpath)
    fromdir = Oldpath
    todir = Newpath
    for root,dirs,files in os.walk(fromdir):
        for filename in files:
            path=os.path.join(root,filename)
            shutil.copyfile(path,'%s/%s'%(todir,filename))
            #stat1=os.stat(os.path.join(fromdir,filename))
            #os.utime(os.path.join(todir,filename),(stat1[ST_CTIME], stat1[ST_MTIME]))
    return True

copyFileCounts = 0  
  

def copyFiles(sourceDir, targetDir):  
    global copyFileCounts  
    print sourceDir  
    print "%s µ±Ç°´¦ÀíÎÄ¼þ¼Ð%sÒÑ´¦Àí%s ¸öÎÄ¼þ" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), sourceDir,copyFileCounts)  
    for f in os.listdir(sourceDir):  
        sourceF = os.path.join(sourceDir, f)  
        targetF = os.path.join(targetDir, f)  
                
        if os.path.isfile(sourceF):  
            #´´½¨Ä¿Â¼  
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            copyFileCounts += 1  
              
            #ÎÄ¼þ²»´æÔÚ£¬»òÕß´æÔÚµ«ÊÇ´óÐ¡²»Í¬£¬¸²¸Ç  
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):  
                #2½øÖÆÎÄ¼þ  
                open(targetF, "wb").write(open(sourceF, "rb").read())  
                print "%s %s ¸´ÖÆÍê±Ï" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF)  
            else:  
                print "%s %s ÒÑ´æÔÚ£¬²»ÖØ¸´¸´ÖÆ" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF)  
        if os.path.isdir(sourceF):  
            copyFiles(sourceF, targetF)  
    
def Getfindpath(path,findstr=''):
    list_path = path.split('\\')
    parentpath = ''
    for i in range(len(list_path)):
        if i==0:
            parentpath=list_path[i]
        else:
            parentpath = parentpath + '\\'+list_path[i]
        if len(findstr)==0:
            continue
        if list_path[i].find(findstr)>-1:
            break
    return parentpath   
    
def file_exist(file,Flag=False):
    if os.path.isfile(file) ==False:
        msg = file  + "not exists"
        #print msg
        if Flag==True:
            info_public(msg)
        return False
    return True
    

def File_change(file):
    tmp_list = file.split('\\')
    file = '/'.join(tmp_list)
    return file

def find_parentpath(findstr='Simu_'):
    path1 = os.path.abspath(sys.argv[0])
    path_parent = Getfindpath(path1,findstr)
    return path_parent

def Write_tmp_file(file_name,keyword):
    file_object = open(file_name,'w')
    file_object.write(keyword)
    file_object.close()

def Read_tmp_file_path(file_name):
    if file_exist(file_name)==False:
        msg = 'Not find the file:' + file_name
        log_print(msg)
    file_object = open(file_name,'r')
    textlist = file_object.readlines()
    file_object.close()
    tmp_str = ''
    for x in textlist:
        if len(x)>0:
            tmp_str = x
            break
    return tmp_str

def Get_tmp_file_name(filename):
    if filename.find(':')<0:
            tmp_path_case = find_parentpath() + '\\tmp_result\\' +'tmp_case_path.log'
            tmp_case_path = Read_tmp_file_path(tmp_path_case)
            if len(tmp_case_path) < 0 :
                log_print('tmp file path error!!!!')
                return False
            filename = tmp_case_path + '\\'+ filename
    return filename
def path_exist(path):
    if os.path.exists(path) ==False:
        msg = path  + "not exists"
        print msg
        info_public(msg)
        return False
    return True


def lotus_send(version,codePlugin,text='test',email_Flag = 'plain',list_result=[]):
        content ='Dear all:'  +'\r' + 'this is the OLT/ONU version: '+version +' autoest result'+'\r'+'Please see the Plugin' 
       
        if len(list_result) == 0:
            #sub = 'this is the AC version: ' + version + ' auto test result'
            sub =  version + ' auto test result:'
        else:
            sub =  version + ' auto test result:' + '/'.join(list_result) + ' = '  + str(string.atoi(list_result[0])*100/string.atoi(list_result[1])) + '%'
      
        #text='test'
        #email_Flag = 'plain'
        #codePlugin = [{'subject' : 'E:\\Simu_server\\result\\result__step1_ac_20130311_104552.txt', 'content' : '1abc'}, {'subject' : 'E:\\Simu_server\\result\\result__step1_ac_20130313_104443.txt', 'content' : '2abc'}] 
        testmail =  smtpemail()
        testmail.read_mail_to_cc_list()
        print 'dic_email_file read:', testmail.dic_email_file
        if sub.find('100')>-1:
            mailto_list = testmail.dic_email_file['mailto_list']
        else:
            mailto_list = testmail.dic_email_file['mailto_fail_list']
            
        mailcc_list = testmail.dic_email_file['mailcc_list']
        send_flag = testmail.dic_email_file['send_email_Flag']
        if send_flag=='1':
            testmail.send_mail_text(mailto_list,mailcc_list,sub,content,codePlugin,version,text,email_Flag)
            testmail.getresult()
        return True
    

def kill_program(pidname = 'iexplore.exe',findstr='Explorer'):
        result =False
        REC_read= 'wmic process where caption="'+pidname+'" get caption,commandline /value'
        REC_kill=  'TASKKILL /F /IM ' + pidname
        print_mes = os.popen(REC_read).read() 
        print print_mes
        info_public(print_mes)
        if print_mes.find(findstr)>-1:
            print_mes = os.popen(REC_kill).read() 
            print print_mes
            info_public(print_mes)
        return result
    
def replaceini(filename,keyword,param,value):
    file_object = open(filename,"r")
    textlist = file_object.readlines()
    file_object.close()
    Flag_param = False
    Flag_keyword = False
    Flag_new_param = False
    filename_tmp = os.path.dirname(filename) + '\\tmp_ini_p12.ini'
    file_object_tmp = open(filename_tmp,"w")
    opFlag = False
    for s in textlist:
        tmp_str =''
        if s.find('[')>-1 and s.find(']')>-1:
            Flag_new_param =True
            tmp_str = s[s.find('['):s.find(']')]
        else:
            Flag_new_param =False
        if Flag_new_param==True:
            if tmp_str.find(param)>-1:
                Flag_param =True
            else:
                Flag_param =False
        if Flag_new_param ==False and  s.find('=')>-1 and Flag_param ==True:
            if s.find(keyword)>-1:
                s = s[:s.find('=')] +' = ' + value + '\n'
                opFlag =True
        file_object_tmp.writelines(s) 
    file_object_tmp.close()
    os.remove(filename)
    os.rename(filename_tmp,filename)
    if opFlag ==False:
        msg = 'not find:' + filename + ' or not find param:' +param + ' or not find keyword:' +keyword
    return  opFlag
    
def file_all(endword=['.pcap','.pcp']):
    
    path_list=['C:\\','D:\\','E:\\','F:\\','G:\\']
    
    for x in path_list:
        try:
            for root,dirs,files in os.walk(x):
                for name in dirs:
                    if name.startswith('Simu')==True:
                        msg=root+'\\'+name
                        print msg
                        
        except Exception,e:
            pass
    #file_del('C:\\',endword)
    '''
    for x in path_list:
        file_del(x,endword)
        break
    '''

def multiple_replace(text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)
    
def file_del(path,endword=['.pcap','.pcp']):
    try:
            for root,dirs,files in os.walk(path):
                for file in files:
                    for y in endword:
                        if file.endswith(y)==True:
                            name = root +'\\'+file
                            print name
                            os.remove(name)
    except Exception,e:
        log_print(e)
        pass
    
                    #all_file_list.append(name)
    #print '*****************all_file_list:***********',all_file_list
    return True
    

def env_rm_file(file):
    #os.remove(file)
    if file_exist(file):
        os.remove(file)
    return True

def clear_env_rm_file(file):
    #os.remove(file)
    if file_exist(file):
        os.remove(file)
    fp = open(file, 'a')
    fp.close()
    return True

def find_path(pathname,path):
    abspath=''
    for root, dirs, files in os.walk(path, False):
        for name in dirs: 
            if name.find(pathname)>-1:
                abspath = os.path.join(root,name)
                break
    return abspath


def readfile(filename,findstr,separator=':'):
    value = ''
    file_object = open(filename,"r")
    textlist = file_object.readlines()
    file_object.close()
    for x in textlist:
        if x.find(findstr)>-1:
            value = x.split(separator)[-1].strip()  
    return value

def count_line_file(filename):
        count=-1
        file_object1 = open(filename,'r')
        textlist = file_object1.readlines()
        count=len(textlist)
        file_object1.close()
        return count
    
def writefile(filename,findstr,value,separator=':',file_mode ='tmp_resource.log'):
    #print 'writefile:',filename,findstr,value
    file_object = open(filename,"r")
    textlist = file_object.readlines()
    file_object.close()
    path1 = os.path.dirname(filename)
    new_filename =path1 + '\\' + file_mode
    if file_exist(new_filename):
        os.remove(new_filename)
    fp = open(new_filename, 'a')
    
    writefile_flag = False
    for x in textlist:
        if x.find(findstr)>-1:
            #print x
            #fp.write('\n')
            tmp_str= x.split(separator)[0]+separator + value + '\n'
            
            fp.write(tmp_str)
            #print tmp_str
            writefile_flag = True
            
        else:
            fp.write(x) 
    if writefile_flag==False:
        
        #tmp_str= x.split(separator)[0]+separator
        #tmp_str = tmp_str.ljust(WIDTH_STR) + value
        #tmp_str = tmp_str.rjust(WIDTH_STR_VALUE)
        tmp_str='\n'+ findstr +separator + value + '\n'
        fp.write(tmp_str)
        
        
    fp.close()
    
    #time.sleep(20)
    shutil.copy(new_filename,filename)
    
    return 
    
def cmd_command(command,find_str,time_wait=10,resend_flag=True):
    num = 0
    while True:
        info = os.popen(command).read()
        log_print(info)
        regex = re.compile(find_str)
        #print regex
        re_result=regex.findall(info)
        log_print( re_result)
        if re_result:
            log_print( "find this command ")
            break
        else:
            if num >=3:
                log_print( "this command not find")
                return False  
        num = num +1
    #time.sleep(30)
    return True    

def cmd_command1(command,find_str,time_wait=10,resend_flag=True):
    num = 0
    while True:
        #print "find_str:",find_str
        #time.sleep(20)
        info = os.popen(command).read()
        log_print(info)
        regex = re.compile(find_str)
        #print regex
        re_result=regex.findall(info)
        log_print( re_result)
        if re_result:
            log_print( "find this command ")
            break
        
    #time.sleep(30)
    return True  

def Remove_File(src,end='.pcap',flag=True):
    for i in os.listdir(src):
        filepath = src + os.sep + i
        if os.path.isdir(filepath):
            if flag==True:
                Remove_File(filepath,end,flag)
        elif i.endswith(end):
            os.remove(os.path.join(src,i))

if __name__ == "__main__":
    mac ='00-0B-2F-1E-8F-24'
    #print get_mac('English')
    Calculation(mac)
    checkVersion_PC()
    #checktime()
    #file_all(endword=['.pcap','.pcp'])




