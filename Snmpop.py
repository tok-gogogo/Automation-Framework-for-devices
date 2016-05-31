#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        SNMP_OPER.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/12/21
# RCS-ID:      $Id: SNMP_OPER.py $,USE FOR snmp operation
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
from global_parame import *
import os,sys,time,string,types,WtLog,ConfigParser,xlrd,re, random
from wtResult import clsWtResult
from public import *
import locale,codecs
import subprocess
import telnet_class

'''
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp import debug
from pysnmp.proto.rfc1902 import ObjectName
'''

class SnmpAuto():
    def __init__(self,SnmpconfigFile ='',debug_flag='1'):
        self.list_type = []
        self.debug_flag =debug_flag
        self.opsnmpdic_result={}
        self.dic_oidvalue={'String':0, 'ObjID':1, 'TimeTicks':2, 'INTEGER':3, 'Integer32':4, 'EnumVal':5, 'Gauge':6, 
                           'Counter':7, 'NetAddr':8, 'IpAddr':9, 'Unsigned':10, 'Counter64':11, 'BitString':12,'Opaque':13}
        '''
        if debug_flag =='1':
            debug.setLogger(debug.Debug('all'))
        '''
        if SnmpconfigFile=='':
            path = get_run_path()
            SnmpconfigFile = path + '\\auto_conf\\mib_config.ini'
        self.SnmpconfigFile = SnmpconfigFile
        self.oid_op_error ={0:'not operation oid',1:'receive not response ',2:'response info not find the Keyword',
                            3:' No Such Object available on this agent at this OID',4:'not leaf oid',5:'not entry oid',
                            6:'PASS',7:'not leaf or max-access  read-write or read-create cannot set',8:'Not find the oid type',
                            9:' Wrong Type'}
        
        
    def GetconfigFile(self):
        try:
            configfp = open(self.SnmpconfigFile,"r")
        except IOError:
            msg = "config.ini is not found"
            
            log_print(msg)
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(configfp)
        configfp.close()
    
        
    def GetTyperange(self,Type):
        range_value ='None'
        try:
            keyword = Type + ' Type'
            range_value = self.config.get(keyword,"Size").strip()
            #log_print(range_value)
        except Exception ,exc_str:
            msg = 'Not Found the  Size under section '  + keyword + ' in config.ini.'
            log_print(exc_str)
            log_print(msg)
            pass
        return range_value
        
    def Getprotocol(self):
        dic = {'SNMPV2C':'2c','SNMPV1':'1','SNMPV3':'3'}
        try:
            tmp_str = self.config.get("Protocal","protocol")
            tmp_str = tmp_str.strip().upper()
            if dic.has_key(tmp_str):
                self.protocol = dic[tmp_str]
                msg = 'self.protocol:' + self.protocol
                if self.debug_flag=='1': 
                    log_print(msg)
            else:
                log_print('the protocol write error use init protocol snmp2c')
                self.protocol = '2c'
        except ConfigParser.NoOptionError:
            msg = "protocol is not found under section Protocal in config.ini."
            
            log_print(msg)
    
    def GetGeneral(self):
        try:
            tmp_str = self.config.get("General","Read")
            self.Read  = tmp_str.strip()
            msg = 'self.Read:' + self.Read
            if self.debug_flag=='1': 
                log_print(msg)
            tmp_str = self.config.get("General","Write")
            self.Write  = tmp_str.strip()
            msg = 'self.Write:' + self.Write
            if self.debug_flag=='1': 
                log_print(msg)
        except ConfigParser.NoOptionError:
            msg = "Read or Write is not found under section General in config.ini."
            log_print(msg)
            
    def GetPort(self):
        try:
            tmp_str = self.config.get("Port","port")
            self.port  = tmp_str.strip()
            msg = 'self.port:' + self.port
            if self.debug_flag=='1': 
                log_print(msg)
        except ConfigParser.NoOptionError:
            msg = "port is not found under section Port in config.ini."
            log_print(msg)
            
    def GetMibip(self):
        try:
            tmp_str = self.config.get("MIB IP","IP")
            self.IP  = tmp_str.strip()
            msg = 'self.IP:' + self.IP
            if self.debug_flag=='1': 
                log_print(msg)
        except ConfigParser.NoOptionError:
            msg = "IP is not found under section MIB IP in config.ini."
            
            log_print(msg)
    
    def GetNetsnmpbinpath(self):
        try:
            tmp_str = self.config.get("NET SNMP BIN","binpath")
            self.netsnmpbinpath  = tmp_str.strip()
            msg = 'self.binpath:' + self.netsnmpbinpath
            if self.debug_flag=='1': 
                log_print(msg)
        except ConfigParser.NoOptionError:
            msg = "binpath is not found under section NET SNMP BIN in config.ini."
            log_print(msg)
            
    def GetMibPath(self):
        try:
            tmp_str = self.config.get("NET SNMP MIBS PATH","mibpath")
            self.mibpath  = tmp_str.strip()
            msg = 'self.mibpath:' + self.mibpath
            if self.debug_flag=='1': 
                log_print(msg)
            #self.SetWindowsMibEnv()
        except ConfigParser.NoOptionError:
            msg = "mibpath is not found under section NET SNMP MIBS PATH in config.ini."
            log_print(msg)
            
    def GetMIB_DATA(self):
        try:
            tmp_str = self.config.get("MIB DATA","file")
            self.filename  = tmp_str.strip()
            msg = 'self.filename:' + self.filename
            if self.debug_flag=='1': 
                log_print(msg)
            tmp_str = self.config.get("MIB DATA","sheetname")
            self.sheetName  = tmp_str.strip()
            msg = 'self.sheetname:' + self.sheetName
            if self.debug_flag=='1': 
                log_print(msg)
        except ConfigParser.NoOptionError:
            msg = "file or sheetname is not found under section MIB DATA in config.ini."
            log_print(msg)
            
    def OpenexcelFile(self):
        obj_book = 0 
        file_exist(self.filename)
        try:
            obj_book = xlrd.open_workbook(self.filename)
            return obj_book
        except Exception,e:
            log_print(e)
            log_print('open the excel failed!')
            return obj_book
    
    def Excel_sheetName(self):
        obj_table = 0
        obj_book = 0 
        obj_book = self.OpenexcelFile()
        if obj_book == 0 :
            msg='Not find the excel:' + self.filename
            self.error = msg
            return obj_book
        for sheetname in obj_book.sheet_names():
            if self.sheetName == sheetname :
                obj_table = obj_book.sheet_by_name(sheetname)
                break
        return obj_table
    
    def Read_excel_data(self):
        obj_table = self.Excel_sheetName()
        self.Dic_parame ={}
        if obj_table == 0 :
            msg = 'find the excel: ' +self.filename +' but not find sheet name:' + self.sheetName
            if self.debug_flag=='1': 
                log_print(msg)
            self.error = msg
            return self.Dic_parame
        for row in range(obj_table.nrows):
            values =  []
            for  col in range(obj_table.ncols):
                values.append(obj_table.cell(row,col).value)
            tmp_list = []
            tmp_num =0
            key = ' '
            for x in values:
                if tmp_num==0:
                    key = x.strip()
                else:
                    tmp_list.append(x.strip())
                tmp_num = tmp_num + 1 
            
            self.Dic_parame[key] = tmp_list   
        return self.Dic_parame
        
    def Restartnetsnmpagent(self,find_str = '服务已经启动成功'):
        command = 'net stop "net-snmp agent"'
        if self.debug_flag=='1': 
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1': 
            log_print(info)
        
        time.sleep(10)
        command = 'net start "net-snmp agent"'
        if self.debug_flag=='1': 
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1': 
            log_print(info)
        time.sleep(10)
        
        
    def GetAllOID(self):
        path = get_run_path()
        file = path + '\\tmp_date\\tmp_miboid.txt'
        if file_exist(file):
            os.remove(file)
        try:
            command = self.netsnmpbinpath +'\\snmptranslate -To -m ALL >' + file 
            log_print(command)
            os.popen(command).read()
            
            file_object = open(file,"r")
            textlist = file_object.readlines()
            file_object.close()
            #log_print('This is Get All oid list:')
            self.oid_list = []
            for x in textlist:
                if len(x.split('.')[-1])==1 and  x.split('.')[-1] =='0':
                    continue
                self.oid_list.append(x.strip())
                #log_print(x.strip())
            
            
        except Exception,e:
            log_print('Get all oid is error:')
            log_print(e)
            
        
    def Readconfig(self):
        self.GetconfigFile()
        self.Getprotocol()
        self.GetGeneral()
        self.GetPort()
        self.GetMibip()
        self.GetMIB_DATA()
        self.GetMibPath()
        self.GetNetsnmpbinpath()
        self.Read_excel_data()
        '''
        if self.Restartnetsnmpagent()==False:
            return False
        '''
    def SetWindowsMibEnv(self):
        command = 'set  MIBDIRS='  + self.mibpath
        if self.debug_flag=='1': 
            log_print(command)
        os.popen(command).read()
        command = 'set MIBS=ALL'
        if self.debug_flag=='1': 
            log_print(command)
        
    def Get_Allsnmpoid_descrip(self):
        self.dic_alloid={}
        for x in self.oid_list:
            command = self.netsnmpbinpath +'\\snmptranslate -Td -OS ' + x
            info = os.popen(command).read()
            self.dic_alloid[x] = info
            msg = '*********** This oid:' + x + ' description ***********\n' + info
            if self.debug_flag=='1': 
                log_print(msg)
    
    def Auto_TestOid_Get_descrip_single_get(self,oid):
        self.Readconfig()
        self.GetAllOID()
        oid ='.' + oid
        #self.Get_Partsnmpoid_descrip(oid)
        msg = ''
        self.dic_partoid_leaf = {}
        self.dic_partoid ={}
        for x in self.oid_list:
            if x.startswith(oid)==True:
                if len(oid)!= len(x) :
                    if x[len(oid)] != '.':
                        continue
                #print '*********************'
                command = self.netsnmpbinpath +'\\snmptranslate -Td -OS ' + x
                info = os.popen(command).read()
                self.dic_partoid[x] = info
                msg = '*********** This oid:' + x + ' description ***********\n' + info
                if self.debug_flag=='1': 
                    log_print(msg)
                    
                if self.opsnmpdic_result.has_key(x)==False:
                    self.opsnmpdic_result[x] = {'GET':0,'GETNEXT':0,'SET':0,'WALK':0,'GETBULK':0,
                                                  'GET_ERROR':[],'GETNEXT_ERROR':[],'SET_ERROR':[],'GETBULK_ERROR':[],'WALK_ERROR':[]}
                tmp_list = self.Read_MAX_ACCESS(info,x)
                if len(tmp_list)!=0 :
                    self.dic_partoid_leaf[x] = tmp_list
                    if tmp_list[1]=='entry':
                        #oid_leaf = key 
                        self.Snmpop_Getinstall_single(x,tmp_list)
                    elif tmp_list[1] =='leaf':
                        #oid_leaf = key 
                        self.Snmpop_Get_single(x)
                    else:
                        msg = 'this is not entry or leaf  oid:' + x
                        self.opsnmpdic_result[x]['GET'] = 4
                else:
                    msg = 'this is not entry or leaf  oid:' + x
                    if self.debug_flag=='1':
                        log_print(msg)
                    self.opsnmpdic_result[x]['GET'] = 4
        
        self.debug_flag='1'
        
        if self.debug_flag=='1':
            log_print('************* all oid description **************')
            log_print(self.dic_partoid_leaf)
            for key,value in  self.dic_partoid_leaf.items():
                msg = '   key: ' + key + '   value:'+ '        '.join(value)
                log_print(msg)
        if self.debug_flag=='1':
            log_print('************* oid Test result **************')
            log_print(self.opsnmpdic_result)
            for key,value in  self.opsnmpdic_result.items():
                #print 'key:',key ,' value:',value
                str_GET_ERROR = ''
                str_SET_ERROR = ''
                str_GETNEXT_ERROR = ''
                str_WALK_ERROR = ''
                str_GETBULK_ERROR = ''
                if len(value['GET_ERROR'])==0:
                    str_GET_ERROR = 'None_error'
                else:
                    str_GET_ERROR = ' ,'.join(value['GET_ERROR'])
                if len(value['SET_ERROR'])==0:
                    str_SET_ERROR = 'None_error'
                else:
                    str_SET_ERROR = ' ,'.join(value['SET_ERROR'])
                if len(value['GETNEXT_ERROR'])==0:
                    str_GETNEXT_ERROR = 'None_error'
                else:
                    str_GETNEXT_ERROR = ' ,'.join(value['GETNEXT_ERROR'])
                if len(value['WALK_ERROR'])==0:
                    str_WALK_ERROR = 'None_error'
                else:
                    str_WALK_ERROR = ' ,'.join(value['WALK_ERROR'])
                if len(value['GETBULK_ERROR'])==0:
                    str_GETBULK_ERROR = 'None_error'
                else:
                    str_GETBULK_ERROR = ' ,'.join(value['GETBULK_ERROR'])
                msg = ('OID: ' + key 
                + ' GET:' + str(value['GET']) +' GET_ERROR:'+str_GET_ERROR
                + ' SET:' + str(value['SET']) + ' SET_ERROR:'+ str_SET_ERROR
                + ' GETNEXT:' + str(value['GETNEXT']) +' GETNEXT_ERROR:'+ str_GETNEXT_ERROR
                + ' GETBULK:' + str(value['GETBULK']) + ' GETBULK_ERROR:'+ str_GETBULK_ERROR
                + ' WALK:' + str(value['WALK']) + ' WALK_ERROR:'+ str_WALK_ERROR
                )
                log_print(msg)
        
    def Get_Partsnmpoid_descrip(self,oid):
        #print ' Get_Partsnmpoid_descrip fuction'
        self.dic_partoid_leaf = {}
        self.dic_partoid ={}
        for x in self.oid_list:
            if x.startswith(oid)==True:
                if len(oid)!= len(x) :
                    if x[len(oid)] != '.':
                        continue
                #print '*********************'
                command = self.netsnmpbinpath +'\\snmptranslate -Td -OS ' + x
                info = os.popen(command).read()
                self.dic_partoid[x] = info
                msg = '*********** This oid:' + x + ' description ***********\n' + info
                if self.debug_flag=='1': 
                    log_print(msg)
                
                tmp_list = self.Read_MAX_ACCESS(info,x)
                #print '11111111111111111'
                if len(tmp_list)!=0 :
                    self.dic_partoid_leaf[x] = tmp_list
                
                    
                    
        '''            
        if self.debug_flag=='1': 
            log_print( 'self.dic_partoid_leaf:')
            log_print(self.dic_partoid_leaf)
            #log_print('self.dic_partoid:')
            #log_print(self.dic_partoid)
        '''
    
    def snmp_getop(self):
        log_print('11')
        
    def Findstr(self,info,find_str):
        regex = re.compile(find_str)
        re_result=regex.findall(info)
        '''
        if self.debug_flag=='1':
            log_print(re_result)
        '''
        if re_result:
            return True
        else:
            return False
        
    def Findstr_multi_either(self,*args):
        tmp_num = 0
        find_str = ''
        info = ''
        if len(args)<2:
            return []
        for arg in args:
            if tmp_num == 0:
                info = arg
            elif tmp_num ==1:
                find_str = arg
            else:
                find_str = find_str + '|'+ arg 
            tmp_num = tmp_num +1 
        regex = re.compile(find_str)
        re_result=regex.findall(info)
        return    re_result
    
    def Findstr_multi(self,info,find_str):
        regex = re.compile(find_str)
        re_result=regex.findall(info)
        if self.debug_flag=='1':
            log_print(re_result)
        if re_result:
            return True
        else:
            return False
        
    def Read_MAX_ACCESS(self,oid_descrip,oid):
        #print ' Read_MAX_ACCESS fuction'
        #print '222222222222222222222'
        dic_pand = {'not-accessible':1,'None':1}
        re_str =[]
        if len(oid_descrip)==0:
            return re_str
        if self.Findstr(oid_descrip,'MAX-ACCESS')==False:
            return re_str
        #log_print(oid_descrip.split('\n'))
        tmp_str1 ='None'
        tmp_str2 ='None'
        for x in oid_descrip.split('\n'):
            #print 'oid x:',x
            if tmp_str1!='None' and tmp_str2!='None':
                break
            if tmp_str1=='None':
                if self.Findstr(x,'MAX-ACCESS')==True:
                    tmp_str1 = x.split('MAX-ACCESS\t')[-1]
            if tmp_str2=='None':
                if self.Findstr(x,'::=')==True:
                    if self.Findstr(x,'Table.+Entry')==True:
                        tmp_str2 ='entry'
                    else:
                        tmp_str2 ='leaf'
                
                    
        #print 'tmp_str1,tmp_str2:',tmp_str1,tmp_str2
        if dic_pand.has_key(tmp_str1)==True:
            return re_str
        
        #self.TestValueType(oid)
        oid_type,oidvalue_range = self.GetoidvalueType(oid)
        if self.debug_flag=='1':
            log_print(self.list_type)
        #self.GetoidvalueRange(oid)
        re_str.append(tmp_str1)
        re_str.append(tmp_str2)
        re_str.append(oid_type)
        re_str.append(oidvalue_range)
        #print 're_str:',re_str
        return re_str
        
            
    def TestValueType(self,oid):
        command = self.netsnmpbinpath +'\\snmptranslate -Td -Tp ' + oid
        if self.debug_flag=='1':
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1':
            log_print(info)
        for x in info.split('\n'):
            if self.Findstr(x,'\+--')==True:
                if len(x.split(' '))>=3:
                    oidtype =  x.split(' ')[2]
                    if oidtype not in self.list_type:
                        self.list_type.append(oidtype)
                elif len(x.split(' '))==1:
                    oidtype =x.split('+--')[-1]
                    if oidtype not in self.list_type:
                        self.list_type.append(oidtype)
                break
        
        
    def GetoidvalueType(self,oid):
        #dic_type={'STRING':0,'INTEGER':1}
        dic_type_range={'String':'Size', 'ObjID':'None', 'TimeTicks':'None', 'INTEGER':'Range', 'Integer32':'None', 'EnumVal':'Values',
                        'Gauge':'None', 'Counter':'None', 'NetAddr':'None', 'IpAddr':'None', 'Unsigned':'Range','Counter64':'None',
                        'BitString':'None', 'Opaque':'None','OCTET STRING':'None'}
        command = self.netsnmpbinpath +'\\snmptranslate -Td -Tp ' + oid
        if self.debug_flag=='1':
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1':
            log_print('******* oid value from the mib data:*******')
            log_print(info)
        tmp_list = []
        oidtype ='None'
        range_value='None'
        for x in info.split('\n'):
            if self.Findstr(x,'\+--')==True:
                if len(x.split(' '))>=3:
                    oidtype =  x.split(' ')[2]
                elif len(x.split(' '))==1:
                    oidtype =x.split('+--')[-1]
            elif self.Findstr(x,'OCTET STRING')==True:
                oidtype = 'OCTET STRING'
            if oidtype!='None':
                #print 'GetoidvalueType oidtype:',oidtype
                if dic_type_range.has_key(oidtype)==True:
                    tmp_findstr  = dic_type_range[oidtype]
                    if self.Findstr(x,tmp_findstr)==True:
                        range_value = x.split(':')[-1]
                
        return oidtype,range_value
    
    def GetoidvalueRange(self,oid,oidtype):
        dic_type_range={'String':'Size', 'ObjID':'', 'TimeTicks':'', 'INTEGER':'', 'Integer32':'', 'EnumVal':'', 'Gauge':'', 
                        'Counter':'', 'NetAddr':'', 'IpAddr':'', 'Unsigned':'', 'Counter64':'', 'BitString':'', 'Opaque':'',
                        'OCTET STRING':''}
        
        
    def Compare_value(self,info,oid):
        re_value = False
        min_flag = False
        max_flag = False
        tmp_value = info.split('=')[-1]
        value = tmp_value.split(': ')[-1].strip('\n').strip('\t')
        valuetype  = self.dic_partoid_leaf[oid][2]
        valuerange = self.dic_partoid_leaf[oid][3]
        if valuerange=='None':
            valuerange = self.GetTyperange(valuetype)
        if valuerange !='None':
            if valuetype=='String':
                if len(value)>= string.atoi(valuerange.split('..')[0]):
                    min_flag = True
                    if len(value)<= string.atoi(valuerange.split('..')[-1]) :
                        max_flag = True 
            elif valuetype=='INTEGER':
                #print '1111value:',value
                value = ''.join(re.findall('\d|-',value))
                #print '1111value:',value
                if string.atoi(value)> string.atoi(valuerange.split('..')[0]):
                    min_flag = True
                if string.atoi(value)< string.atoi(valuerange.split('..')[-1]) :
                    max_flag = True
            elif valuetype=='EnumVal':
                if valuerange.find(value.strip().strip('\n'))>-1:
                    min_flag =True 
                    max_flag = True
                    
                '''
                split_str = re.findall('\.\.|,',valuerange)[0]
                if len(split_str) == 0:
                    if valuerange.find(value.strip().strip('\n'))>-1:
                        min_flag =True 
                        max_flag = True
                        break
                else:
                    for x in valuerange.split(split_str):
                        #print 'x:',x,'value',value
                        if x.strip().find(value.strip().strip('\n'))>-1:
                            min_flag =True 
                            max_flag = True
                            break
                '''
        
        if min_flag==True and max_flag == True:
            re_value = True
            msg = 'Get value: ' + value + ' is in '  + 'valuerange ' + valuerange
        else:
            re_value = False
            msg = 'Get value: ' + value + ' is not in '  + 'valuerange ' + valuerange
        if self.debug_flag=='1':
            log_print(msg)
        return re_value
    
    def STRRandom(self,len_num):
        Rand_Type_Value = ''
        num_len  = len(string.ascii_letters) + len(string.digits)
        total_num = 0 
        if len_num>=len(string.ascii_letters) + len(string.digits):
            total_num = len_num /num_len
            for x in range(total_num):
                tmp_str = ''.join(random.sample(string.ascii_letters+string.digits, num_len))
                Rand_Type_Value = tmp_str + Rand_Type_Value
            tmp_str = ''.join(random.sample(string.ascii_letters+string.digits, len_num -total_num*num_len)) 
            Rand_Type_Value = tmp_str + Rand_Type_Value
        else:
            Rand_Type_Value = ''.join(random.sample(string.ascii_letters+string.digits, num_len))
        return Rand_Type_Value
                
    def Random_Value(self,Type,rangelen):
        Rand_Type_Value = None
        min = string.atoi(rangelen.split('..')[0])
        max = string.atoi(rangelen.split('..')[-1])
        if Type=='String':
            len_num = random.randint(min,max)
            Rand_Type_Value = self.STRRandom(len_num)
            #''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
        elif Type=='INTEGER':
            Rand_Type_Value = string(random.randint(min,max))
        #print 'Rand_Type_Value:',Rand_Type_Value
        return Rand_Type_Value
        
    def Snmpop_set(self,oid):
        dic_type_oid ={'String':'s','ObjID':'o', 'TimeTicks':'None', 'INTEGER':'i', 'Integer32':'i', 'EnumVal':'None', 
                       'Gauge':'None', 'Counter':'None', 'NetAddr':'None', 'IpAddr':'a', 'Unsigned':'None', 'Counter64':'None', 
                       'BitString':'b', 'Opaque':'None'}
        self.Get_Partsnmpoid_descrip(oid)
        Rand_Type_Value = None
        for key,value in self.dic_partoid_leaf.items():
            if self.opsnmpdic_result.has_key(key)==False:
                self.opsnmpdic_result[key] = {'GET':0,'GETNEXT':0,'SET':0,'WALK':0,'GETBULK':0,
                                              'GET_ERROR':[],'GETNEXT_ERROR':[],'SET_ERROR':[],'GETBULK_ERROR':[],'WALK_ERROR':[]}
            if value[0] =='read-write' or value[0] =='read-create':
                Rand_Type_Value = self.Random_Value(value[2],value[3])
                command = self.netsnmpbinpath +'\\snmpset -v ' + self.protocol + ' -c ' + self.Write + ' ' + self.IP + ' ' + key + ' '+ dic_type_oid[value[2]]+' ' + Rand_Type_Value
                if self.debug_flag=='1':
                    log_print(command)
                info = os.popen(command).read()
                if self.debug_flag=='1':
                    log_print(info)
                info=info.strip('\n').strip()
            else:
                info = 'This oid:'+ key+' is not leaf or max-access  read-write or read-create cannot set '
                if self.debug_flag=='1':
                    log_print(info)
                info=info.strip('\n').strip()
            findstr1 = Rand_Type_Value
            findstr2 = 'Timeout:'
            findstr3 = 'No Such Object available'
            findstr4 = 'not leaf or max-access  read-write or read-create cannot set'
            if Rand_Type_Value!=None and  self.Findstr(info,findstr1)==True:
                result = 6
            elif self.Findstr(info,findstr2)==True or len(info.strip('\n').strip())==0:
                result = 1
            elif self.Findstr(info,findstr3)==True:
                result = 3
            elif self.Findstr(info,findstr4)==True:
                result = 7
            else:
                result = 2
            
            self.opsnmpdic_result[key]['SET'] = result
            if self.debug_flag=='1':
                log_print(self.opsnmpdic_result)
    #def Ranglen
                
    def Deal_Getvalue(self,value,type):
        re_vul =value
        if type =='INTEGER':
            re_vul =''.join(re.findall('\d',value))
        return re_vul
        
            
            
            
    def Getinstall_Judge(self,info,oid,oid_value=[]):
        str_find1 = 'Timeout:'
        str_find2 ='= No'
        str_find3 = 'Wrong Type'
        dic_type_range={'String':1, 'ObjID':2, 'TimeTicks':3, 'INTEGER':4, 'Integer32':4, 'EnumVal':5, 'Gauge':6, 
                        'Counter':6, 'NetAddr':7, 'IpAddr':7, 'Unsigned':6, 'Counter64':8, 'BitString':1, 'Opaque':9,
                        'OCTET STRING':1}
        if self.Findstr(info,str_find1)==True or len(info.strip('\n').strip())==0:
                self.opsnmpdic_result[oid]['GET'] = 1
        elif self.Findstr(info,str_find2)==True:
                self.opsnmpdic_result[oid]['GET'] = 3
        elif self.Findstr(info,str_find3)==True:
                self.opsnmpdic_result[oid]['GET'] = 9
                self.opsnmpdic_result[oid]['GET_ERROR'].append(info)
        else:
            list_info = info.split('\n')
            for x in list_info:
                if len(x.strip().strip('\n'))==0:
                    continue
                min_Flag = False
                max_Flag = True
                type = oid_value[2]
                range_value = oid_value[3]
                Get_value = x.split(': ')[-1].strip()
                Get_value = self.Deal_Getvalue(Get_value,type)
                if range_value =='None':
                    range_value = self.GetTyperange(type)
                min = range_value.split('..')[0].strip()
                max = range_value.split('..')[-1].strip()
                if dic_type_range.has_key(type)==True:
                    if dic_type_range[type]==1:
                        if len(Get_value)>=string.atoi(min):
                            min_Flag = True
                        if  len(Get_value)<=string.atoi(max):
                            max_Flag = True
                        if  min_Flag==True and max_Flag == True:
                            if self.opsnmpdic_result[oid]['GET'] ==0:
                                self.opsnmpdic_result[oid]['GET'] = 6
                        else:
                            self.opsnmpdic_result[oid]['GET'] = 2
                            msg = x + ' error:' +self.oid_op_error[2]
                            self.opsnmpdic_result[oid]['GET_ERROR'].append(msg)
                    elif dic_type_range[type]==2:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==3:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==4:
                        if string.atoi(Get_value)>=string.atoi(min):
                            min_Flag = True
                        if  string.atoi(Get_value)<=string.atoi(max):
                            max_Flag = True
                        if  min_Flag==True and max_Flag == True:
                            if self.opsnmpdic_result[oid]['GET'] ==0:
                                self.opsnmpdic_result[oid]['GET'] = 6
                        else:
                            self.opsnmpdic_result[oid]['GET'] = 2
                            msg = x + ' error:' +self.oid_op_error[2]
                            self.opsnmpdic_result[oid]['GET_ERROR'].append(msg)
                    elif dic_type_range[type]==5:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==6:
                        if string.atoi(Get_value)>=string.atoi(min):
                            min_Flag = True
                        if  string.atoi(Get_value)<=string.atoi(max):
                            max_Flag = True
                        if  min_Flag==True and max_Flag == True:
                            if self.opsnmpdic_result[oid]['GET'] ==0:
                                self.opsnmpdic_result[oid]['GET'] = 6
                        else:
                            self.opsnmpdic_result[oid]['GET'] = 2
                            msg = x + ' error:' +self.oid_op_error[2]
                            self.opsnmpdic_result[oid]['GET_ERROR'].append(msg)
                    elif dic_type_range[type]==7:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==8:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==9:
                        self.opsnmpdic_result[oid]['GET'] = 6
                    elif dic_type_range[type]==10:
                        self.opsnmpdic_result[oid]['GET'] = 6
                else:
                    self.opsnmpdic_result[oid]['GET'] = 8
                
            #print 'info:',info
            #print 'oid_value:',oid_value
    def Auto_TestOid_Set(self,oid):
        self.Readconfig()
        self.GetAllOID()
        oid ='.' + oid
        self.Snmpop_set(oid)
        
    def Auto_TestOid_Get(self,oid):
        self.Readconfig()
        self.GetAllOID()
        oid ='.' + oid
        self.Get_Partsnmpoid_descrip(oid)
        msg = ''
        for key,value in self.dic_partoid_leaf.items():
             print 'key:',key , 'value:',value
             if self.opsnmpdic_result.has_key(key)==False:
                self.opsnmpdic_result[key] = {'GET':0,'GETNEXT':0,'SET':0,'WALK':0,'GETBULK':0,
                                              'GET_ERROR':[],'GETNEXT_ERROR':[],'SET_ERROR':[],'GETBULK_ERROR':[],'WALK_ERROR':[]}
             if value[1] =='entry':
                #oid_leaf = key 
                self.Snmpop_Getinstall_single(key,value)
             elif value[1] =='leaf':
                #oid_leaf = key 
                self.Snmpop_Get_single(key)
             else:
                msg = 'this is not entry or leaf  oid:' + key
                if self.debug_flag=='1':
                    log_print(msg)
                self.opsnmpdic_result[key]['GET'] = 4
                continue
        self.debug_flag='1'
        
        if self.debug_flag=='1':
            log_print('************* all oid description **************')
            log_print(self.dic_partoid_leaf)
            for key,value in  self.dic_partoid_leaf.items():
                msg = '   key: ' + key + '   value:'+ value
                log_print(msg)
        if self.debug_flag=='1':
            log_print('************* oid Test result **************')
            log_print(self.opsnmpdic_result)
            for key,value in  self.opsnmpdic_result.items():
                msg = '   key: ' + key + '   value:'+ value
                log_print(msg)
        
        
            
    def Snmpop_Get_single(self,key):
        oid_leaf = key +'.0'
        command = self.netsnmpbinpath +'\\snmpget -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + oid_leaf
        if self.debug_flag=='1':
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1':
            log_print(info)
        str_find1 = 'Timeout:'
        str_find2 ='No '
        if self.Findstr(info,str_find1)==True or len(info.strip('\n').strip())==0:
            self.opsnmpdic_result[key]['GET'] = 1
        elif self.Findstr(info,str_find2)==True:
            self.opsnmpdic_result[key]['GET'] = 3
        else:
            result = self.Compare_value(info,key)
            if result == True:
                self.opsnmpdic_result[key]['GET'] = 6
            else:
                self.opsnmpdic_result[key]['GET'] = 2
    
    def Snmpop_Getinstall_single(self,key,value): 
        oid_leaf = key
        command = self.netsnmpbinpath +'\\snmpwalk -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + oid_leaf
        if self.debug_flag=='1':
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1':
            log_print(info)
        if self.debug_flag=='1':
            log_print(info)
        self.Getinstall_Judge(info,key,value)
                
    def Snmpop_Get(self,oid):
        self.Get_Partsnmpoid_descrip(oid)
        for key,value in self.dic_partoid_leaf.items():
            self.opsnmpdic_result[key] = {'GET':0,'GETNEXT':0,'SET':0,'WALK':0,'GETBULK':0,
                                          'GET_ERROR':[],'GETNEXT_ERROR':[],'SET_ERROR':[],'GETBULK_ERROR':[],'WALK_ERROR':[]}
            if value[1] =='leaf':
                oid_leaf = key +'.0'
                
            else:
                msg = 'this is not leaf oid:' + key
                if self.debug_flag=='1':
                    log_print(msg)
                self.opsnmpdic_result[key]['GET'] = 4
                continue
            command = self.netsnmpbinpath +'\\snmpget -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + oid_leaf
            if self.debug_flag=='1':
                log_print(command)
            info = os.popen(command).read()
            if self.debug_flag=='1':
                log_print(info)
            str_find1 = 'Timeout:'
            str_find2 ='No Such Object available'
            if self.Findstr(info,str_find1)==True or len(info.strip('\n').strip())==0:
                self.opsnmpdic_result[key]['GET'] = 1
            elif self.Findstr(info,str_find2)==True:
                self.opsnmpdic_result[key]['GET'] = 3
            else:
                result = self.Compare_value(info,key)
                if result == True:
                    self.opsnmpdic_result[key]['GET'] = 6
                else:
                    self.opsnmpdic_result[key]['GET'] = 2
        if self.debug_flag=='1':
            log_print(self.opsnmpdic_result)
            
    def Snmpop_Getinstall(self,oid):
        self.Get_Partsnmpoid_descrip(oid)
        msg = ''
        for key,value in self.dic_partoid_leaf.items():
            if self.opsnmpdic_result.has_key(key)==False:
                self.opsnmpdic_result[key] = {'GET':0,'GETNEXT':0,'SET':0,'WALK':0,'GETBULK':0,
                                              'GET_ERROR':[],'GETNEXT_ERROR':[],'SET_ERROR':[],'GETBULK_ERROR':[],'WALK_ERROR':[]}
            if value[1] =='entry':
                oid_leaf = key 
            else:
                msg = 'this is not entry oid:' + key
                if self.debug_flag=='1':
                    log_print(msg)
                self.opsnmpdic_result[key]['GET'] = 4
                continue
            
            command = self.netsnmpbinpath +'\\snmpwalk -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + oid_leaf
            if self.debug_flag=='1':
                log_print(command)
            info = os.popen(command).read()
            if self.debug_flag=='1':
                log_print(info)
            self.Getinstall_Judge(info,key,value)
        if self.debug_flag=='1':
            log_print(self.opsnmpdic_result)
                
    def Snmpop_Walk(self,oid):
        self.Get_Partsnmpoid_descrip(oid)
        for key,value in self.dic_partoid_leaf.items():
            command = self.netsnmpbinpath +'\\snmpwalk -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + key
            if self.debug_flag=='1':
                log_print(command)
            info = os.popen(command).read()
            if self.debug_flag=='1':
                log_print(info)
        
    def Snmpop_GetBulk(self,oid):
        command = self.netsnmpbinpath +'\\snmpbulkwalk -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + oid
        if self.debug_flag=='1':
            log_print(command)
        info = os.popen(command).read()
        if self.debug_flag=='1':
            log_print(info)
        
    def Snmpop_GetNext(self,oid):
        self.Get_Partsnmpoid_descrip(oid)
        for key,value in self.dic_partoid_leaf.items():
            command = self.netsnmpbinpath +'\\snmpgetnext -v ' + self.protocol + ' -c ' + self.Read + ' ' + self.IP + ' ' + key
            if self.debug_flag=='1':
                log_print(command)
            info = os.popen(command).read()
            if self.debug_flag=='1':
                log_print(info)
    
    def Read_GetNextoid_value(self,oid):
        for x in self.oid_list:
            pass
    
    
        
    def walk_multi(self,ip,time_walk,pid_total,oid):
        #pid_list = []
        #p_list =[]
        while True:
            command = 'snmpwalk -v 2c -c public ' + ip   + ' ' + oid
            info = os.popen('tasklist | findstr "snmpwalk"').read()
            log_print(len(re.findall('snmpwalk',info)))
            
            if len(re.findall('snmpwalk',info))< string.atoi(pid_total):
                try:
                    tn1 = telnet_class.myTelnet(ip,'23',"admin","admin",'1')
                    tn1.open()
                    tn1.mycommand("admin",":",'10')
                    tn1.mycommand("admin",":",'2')
                    tn1.mycommand("enable",">",'2')
                    tn1.mycommand("debug","#",'2')
                    tn1.mycommand("shell","#",'2')
        
                    print '***************'
                    print 'olt getmemshow result:', tn1.olt_getmemshow('110 90')
                    print '***************'
                    
                    tn1.shellcommand("exit","#",'2')
                    
                    tn1.mycommand("logout","#",'2')
                    tn1.close()
                except Exception ,e:
                    pass
                try:
                    p = subprocess.Popen(command,shell=True)
                    #p_list .append(subprocess.Popen.pid(p))
                    #pid_list.append(p)
                    #log_print(pid_total)
                    #print '*******************'
                    #log_print(p_list)
                    #print '*******************'
                except Exception ,e:
                    log_print(e)
                    pass
            time.sleep(time_walk)
            '''
            else:
                tmp_num =0
                for x in pid_list:
                    try:
                        if subprocess.Popen.poll(x)==0:
                            del pid_list[tmp_num]
                            del p_list[tmp_num]
                            break
                        tmp_num = tmp_num   + 1 
                    except  Exception ,e:
                        log_print(e)
                        #print 'here 2'
                        del pid_list[:]
                        pid_list=[]
                        del p_list[:]
                        p_list=[]
                        pass
                #time.sleep(string.atoi(time_walk))
                #tmp_num1 = 0 
             '''
    
        
if __name__ == "__main__":
    
    oid =raw_input("please input oid:")
    ip = raw_input("please input olt ip:")
    time_walk = raw_input("please input walk sleep:")
    pid_total  = raw_input("please input pid total:")
    test_snmp = SnmpAuto()
    while True:
        info = os.popen('tasklist | findstr "snmpwalk"').read()
        print 'find walk',len(re.findall('snmpwalk',info))
        if len(re.findall('snmpwalk',info))<string.atoi(pid_total):
            try:
                test_snmp.walk_multi(ip,time_walk,pid_total,oid)
            except Exception ,e:
                log_print(e)
                pass
        else:
            log_print('Find snmpwalk pid')
        time.sleep(string.atoi(time_walk))
        
            
    '''
    pid_list = []
    p_list =[]
    while True:
        #command = 'snmpwalk -v 2c -c public  192.168.22.248 1'
        test_snmp = SnmpAuto()
        command = 'snmpwalk -v 2c -c public ' + ip   + ' ' + oid
        print len
        if len(pid_list)< string.atoi(pid_total):
            try:
                p = subprocess.Popen(command,shell=True)
                #info = p.stdout.readlines()
                #log_print(info)
            except Exception ,e:
                log_print(e)
                del pid_list[:]
                pid_list=[]
                del p_list[:]
                p_list=[]
                os.popen('taskkill /F /im  snmpwalk.exe').read()
                continue
            p_list .append(p.pid)
            pid_list.append(p)
            log_print(pid_total)
            log_print(p_list)
        else:
            tmp_num =0
            info = os.popen('tasklist | findstr "snmpwalk"').read()
            if info.find('snmpwalk')<0:
                del pid_list[:]
                pid_list=[]
                del p_list[:]
                p_list=[]
            for x in pid_list:
                try:
                    if subprocess.Popen.poll(x)==0:
                        del pid_list[tmp_num]
                        del p_list[tmp_num]
                        break
                    
                    tmp_num = tmp_num   + 1 
                except Exception ,e:
                    log_print(e)
                    del pid_list[:]
                    pid_list=[]
                    del p_list[:]
                    p_list=[]
                    os.popen('taskkill /F /im  snmpwalk.exe').read()
                    continue
            time.sleep(string.atoi(time_walk))
        
        log_print(pid_list)
        
    '''
    #test_snmp.Auto_TestOid_Get('1.3.6.1.2.1.1')
    #test_snmp.Auto_TestOid_Get('1.3.6.1.4.1.7064.1800.2')
    #test_snmp.Auto_TestOid_Get_descrip_single_get('1.3.6.1.4.1.7064.1800.2')
    #test_snmp.Auto_TestOid_Get_descrip_single_get('1.3.6.1.4.1.7064.1800.2.2.1.6.9.1.1.4')
    #test_snmp.Auto_TestOid_Get_descrip_single_get('1.3.6.1.4.1.7064.1800.2.2.1.3.1.8')
    #test_snmp1 =SnmpAuto()
    #test_snmp1.Auto_TestOid_Set('1.3.6.1.4.1.7064.1800.2')
    #test_snmp.Readconfig()
    #test_snmp.GetAllOID()
    #test_snmp.SetWindowsMibEnv()
    #test_snmp.Get_Allsnmpoid_descrip()
    #test_snmp.Get_Partsnmpoid_descrip('iso.org')
    #test_snmp.Get_Partsnmpoid_descrip('iso.org.dod.internet.private.enterprises.nscrtvRoot.nscrtvEponEocTree.eponTree.eponLinkedEoCManagementObjects.eocDevInfoTable.eocDevInfoEntry')
    #test_snmp.Get_Partsnmpoid_descrip('iso.org.dod.internet.private.enterprises.ePeng')
    #test_snmp.Get_Partsnmpoid_descrip('1.3.6.1.4.1.17409.2.3.11.1.1')
    
    #test_snmp.Get_Partsnmpoid_descrip('1.3.6.1.4.1.1949.2.3.2.2.8.1')
   
    #test_snmp.Get_Partsnmpoid_descrip('1.3.6.1.4.1.1949.2.3.2.2.10.1.1')
   
    #test_snmp.Get_Partsnmpoid_descrip('.1.3.6.1.6.3.16.1.4.1.7')
    #test_snmp.Snmpop_Get('.1.3.6.1.2.1.1')
    #test_snmp.Snmpop_set('.1.3.6.1.2.1.1')
    #test_snmp.Get_Partsnmpoid_descrip('.1')
    #test_snmp.Snmpop_Getinstall('.1.3.6.1.2.1.2.2.1.11')
    #test_snmp.Snmpop_Getinstall('.1.3.6.1.2.1.2')
    #test_snmp.Snmpop_Getinstall('.1.3.6.1.4.1.1949')
    #test_snmp.Snmpop_Getinstall('.1.3.6.1.4.1.1949.1.3.10.200.6.2.2.1.5.3.1.1')
    
