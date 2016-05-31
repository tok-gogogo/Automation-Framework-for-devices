#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        STC_CLS.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2013/11/18
# RCS-ID:      $Id: STC_CLS.py $,USE FOR CONTROL testcenter
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------


from global_parame import *
import Tkinter 
import os
import sys
import time
import string
import types
import re

from wtResult import clsWtResult
from public import *
import WtLog

KEY_TIME_FORMAT = "%Y%m%d_%H%M%S"
ENABLE_CAPTURE = 1
str_sign = '>=|<=|>|<|=='
dic_sign = {'==':0,'>':1,'<':2,'>=':3,'<=':4}

def build_cmd(*args):
    cmd = ''
    for arg in args:
        cmd = cmd + arg + ' '
    log_print (cmd)
    return cmd


class Stc(object):
    def __init__(self):
        self.tclsh =Tkinter.Tcl()
        #self.tclsh=Tcl()
        self.error =None
        self.errorFlag = True
        self.resultFlag = False
        self.waittime = 100
        print self.tclsh.eval("package require SpirentTestCenter")
        print 'SpirentTestCenter system version:',self.tclsh.eval('stc::get system1 -Version')
        
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu'
        path_parent = Getfindpath(path1,findstr)
        autoconfigFile = path_parent + '\\auto_conf\\version.ini'
        autoversion_str = read_ini(autoconfigFile,'infoprint','testcenter')
        if autoversion_str.startswith('on')==True:
            ENABLE_CAPTURE = 1
        else:
            ENABLE_CAPTURE = 0
        
        autoversion_str = read_ini(autoconfigFile,'EnableCapture','testcenter')
        if autoversion_str.startswith('on')==True:
            self.infoprintflag = True
        else:
            self.infoprintflag = False
            
        
    def stc_get_resultFlag(self):
        return self.resultFlag
    def stc_init(self, *args):
        cmd =build_cmd('stc::init', *args)
        return self.tclsh.eval(cmd)
        
    def stc_disconnect(self,*args):
        cmd =build_cmd('stc::disconnect', *args)
        return self.tclsh.eval(cmd)
        
    def stc_connect(self,*args):
        cmd =build_cmd('stc::connect', *args)
        return self.tclsh.eval('stc::connect')
        
    def stc_create(self,*args):
        cmd =build_cmd('stc::create', *args)
        return self.tclsh.eval(cmd)
         
    def stc_delete(self,*args):
        cmd =build_cmd('stc::delete', *args)
        return self.tclsh.eval(cmd)
    
    def stc_config(self,*args):
        cmd =build_cmd('stc::config', *args)
        return self.tclsh.eval(cmd)
        
    def stc_get(self, *args):
        cmd = build_cmd('stc::get', *args)
        return self.tclsh.eval(cmd)
        
    def stc_perform(self,*args):
        cmd =build_cmd('stc::perform', *args)
        return self.tclsh.eval(cmd)
        
    def stc_reserve(self,*args):
        cmd =build_cmd('stc::reserve', *args)
        return self.tclsh.eval(cmd)
          
    def stc_release(self,*args):
        cmd =build_cmd('stc::release', *args)
        return self.tclsh.eval(cmd)
        
    def stc_subscribe(self,*args):
        cmd = build_cmd('stc::subscribe',*args)
        return self.tclsh.eval(cmd)
    
    def stc_unsubscribe(self,*args):
        cmd =build_cmd('stc::unsubscribe', *args)
        return self.tclsh.eval(cmd)
        
    def stc_help(self, *args):
        cmd = build_cmd('stc::help',*args)
        return self.tclsh.eval(cmd)
    
    def stc_apply(self, *args):
        cmd = build_cmd('stc::apply',*args)
        return self.tclsh.eval(cmd)
    
    def stc_eval(self,*args):
        if self.errorFlag==False:
            return self.errorFlag
        try:
            tmp_str = 'stc::connect  ' + self.ChassisIp
            self.tclsh.eval(tmp_str)
            tmp_str = 'stc::reserve  ' + self.ChassisIp+'/'+self.iTxSlot+'/'+self.iTxPort+ '  ' + self.ChassisIp+'/'+self.iRxSlot+'/'+self.iRxPort
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
    
    def stc_eval_multi(self,*args):
        if self.errorFlag==False:
            return self.errorFlag
        try:
            tmp_str = 'stc::connect  ' + self.ChassisIp
            self.tclsh.eval(tmp_str)
            tmp_len = 0
            tmp_str = 'stc::reserve  '
            for x in self.list_port_add:
                tmp_str = tmp_str + ' ' + self.ChassisIp + '/'+x
            log_print(tmp_str)
            self.tclsh.eval(tmp_str)
            
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
    
    def stc_read_global(self,filename ='E:\\Simu_server\\global\\global_param.xls',sheetname='global'):
        path1 = os.path.abspath(sys.argv[0])
        findstr = 'Simu'
        tmp_global_file ='\\global\\global_param.xls'
        path_parent = Getfindpath(path1,findstr)
        global_file = path_parent + tmp_global_file
        #read_global_param(global_file,sheetname)
        testexcel = readexcel(global_file,sheetname)
        self.global_p = testexcel.Excel_read()
        log_print('***********read global ****************')
        msg = self.global_p
        log_print(msg)
        log_print('***********read global ****************')
        
    def stc_global_keyreplay(self,dic_param):
        self.stc_read_global()
        dic = {}
        dic_list= dic_param.items()
        for x in dic_list:
            tmp_list = x[1].split('%%')
            tmp_str =''
            tmp_t = 0
            for y in tmp_list:
                if tmp_t % 2 ==0:
                    tmp_str = tmp_str + y
                else:
                    if self.global_p.has_key(y) ==True:
                        tmp_str = tmp_str + self.global_p[y]
                    else:
                        msg = 'the global file excel not find the global_parma:' + y
                        self.errorFlag =False
                        return None
                tmp_t = tmp_t + 1
            dic[x[0]]=tmp_str
            #print 'dic:',dic            
                    
        return dic
    def stc_initpare(self,filename='E:\\Simu_server\\auto_conf\\stream_param.xls',sheetname = 'stream'):
        self.list_port_add =[]
        try:
            initstream = readexcel(filename,sheetname)
            keyvalue_t = initstream.Excel_read()
            msg = '***************** excel  stc stream read data *****************' 
            log_print(msg)
            msg = keyvalue_t 
            log_print(msg)
            msg = '***************** excel  stc stream read data *****************' 
            dic = self.stc_global_keyreplay(keyvalue_t)
            if dic ==None:
                return  self.errorFlag   
            keyvalue = dic
            #print 'Excel_read:',keyvalue
            msg = '***************** excel replay read data *****************' 
            log_print(msg)
            msg = keyvalue 
            log_print(msg)
            msg = '***************** excel replay read data *****************' 
            log_print(msg)
        except Exception ,exc_str:
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            return self.errorFlag
        
        self.ChassisIp = keyvalue['ChassisIp']
        self.iTxSlot = keyvalue['iTxSlot']
        self.iTxPort = keyvalue['iTxPort']
        self.iRxSlot = keyvalue['iRxSlot']
        self.iRxPort = keyvalue['iRxPort']
        self.srcMac = keyvalue['srcMac']
        self.dstMac = keyvalue['dstMac']
        self.ModifierMode = keyvalue['ModifierMode']
        self.Mask = keyvalue['Mask']
        self.StepValue = keyvalue['StepValue']
        self.Data = keyvalue['Data']
        self.RecycleCount = keyvalue['RecycleCount']
        self.DataType = keyvalue['DataType']
        self.EnableStream =keyvalue['EnableStream']
        self.Offset = keyvalue['Offset']
        self.OffsetReference = keyvalue['OffsetReference']
        self.insertSig = keyvalue['insertSig']
        
        self.frameLengthMode = keyvalue['frameLengthMode']
        self.maxFrameLength = keyvalue['maxFrameLength']
        self.FixedFrameLength = keyvalue['FixedFrameLength']
        self.DurationMode = keyvalue['DurationMode']
        self.BurstSize = keyvalue['BurstSize']
        self.Duration = keyvalue['Duration']
        self.LoadMode = keyvalue['LoadMode']
        self.FixedLoad = keyvalue['FixedLoad']
        self.LoadUnit = keyvalue['LoadUnit']
        
        self.SchedulingMode = keyvalue['SchedulingMode']
        self.waittime = string.atoi(keyvalue['waittime'])
        self.RepeatCount = keyvalue['RepeatCount']
        self.FileName =keyvalue['FileName']
        #print 'keyvalue[Vlan_id]:',keyvalue['Vlan_id']
        self.Vlan_id= keyvalue['Vlan_id'].split(',')
        self.Vlan_cfi =keyvalue['Vlan_cfi']
        self.Vlan_pri =keyvalue['Vlan_pri']
        self.etherType=[]
        if keyvalue.has_key('etherType'):
            self.etherType = keyvalue['etherType'].split(',')
        
        self.Filter_config_Use = keyvalue['Filter_config_Use']
        self.FilterOnStreamId = keyvalue['FilterOnStreamId']
        
        self.Filter_srcMac = keyvalue['Filter_srcMac']
        self.Filter_dstMac = keyvalue['Filter_dstMac']
        self.Filter_vlanID = keyvalue['Filter_vlanID']
        #self.Filter_list_Familiar = keyvalue['Filter_list_Familiar'].split(',')
        
        self.Filter_Summary = ' {' + keyvalue['Filter_Summary'] + '} '
        self.Filter_FrameConfig = ' {' + keyvalue['Filter_FrameConfig'] + '} '
        
        self.ParamGeneratorPort =keyvalue['ParamGeneratorPort'].split(',')
        self.ParamAnalyzerPort = keyvalue['ParamAnalyzerPort'].split(',')   
        
        self.compare_mode = keyvalue['compare_mode']
        self.compare_pass_type = keyvalue['compare_pass_type']
        self.ParamGeneratorPortvalue = keyvalue['ParamGeneratorPortvalue']
        self.ParamAnalyzerPortvalue = keyvalue['ParamAnalyzerPortvalue']
        self.ParamGeneratorPort_compare_AnalyzerPort =keyvalue['ParamGeneratorPort_compare_AnalyzerPort']
        self.Generator_con_type = keyvalue['Generator_con_type']
        self.Generator_con_type_load = keyvalue['Generator_con_type_load']
        
        
            
        return self.errorFlag
        
    
    def tmp_list(self,list_tmp = []):
        list_re=[]
        if len(list_tmp)>0:
            for x in list_tmp:
                tmp_str = '\" ' + x  + '\" '
                list_re.append()
        return list_re
                
    def stc_print_flag_error(self,exc_str):
        log_print(exc_str)
        self.error = exc_str
        self.errorFlag =False
        
    def stc_create_pro(self,name=''):
        #print '##### stc_create_pro fuction #####'
        if self.errorFlag == False:
            return self.errorFlag
        strTime = time.strftime(KEY_TIME_FORMAT)
        #print "Creating project ..."
        msg = 'Creating project ...' 
        log_print(msg)
        try:
            self.hProject=self.stc_create('project')
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
        
        #return hProject
    
    def stc_create_tx_rx_port(self,oth_param='-useDefaultHost False'):
        #print '##### stc_create_tx_port fuction #####'
        #print "Creating tx ports ..."
        msg = 'Creating tx ports ...' 
        log_print(msg)
        tmp_str = '//'+self.ChassisIp+'/'+self.iTxSlot+'/'+self.iTxPort
        if self.errorFlag == False:
            return self.errorFlag
        try:
            self.hPortTx_Rx = self.stc_create('port','-under ',self.hProject,'-location ',tmp_str, oth_param)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
    
    def stc_create_tx_port(self,oth_param='-useDefaultHost False'):
        #print '##### stc_create_tx_port fuction #####'
        #print "Creating tx ports ..."
        msg = 'Creating tx ports ...' 
        log_print(msg)
        tmp_str = '//'+self.ChassisIp+'/'+self.iTxSlot+'/'+self.iTxPort
        if self.errorFlag == False:
            return self.errorFlag
        try:
            self.hPortTx = self.stc_create('port','-under ',self.hProject,'-location ',tmp_str, oth_param)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
        
        
    def stc_create_rx_tx_port(self,oth_param='-useDefaultHost False'):
        #print '##### stc_create_rx_port fuction #####'
        #print "Creating rx ports ..."
        msg = 'Creating rx ports ...' 
        log_print(msg)
        tmp_str = '//'+self.ChassisIp+'/'+self.iRxSlot+'/'+self.iRxPort
        if self.errorFlag == False:
            return self.errorFlag
        try:
            self.hPortRx_Tx = self.stc_create('port','-under ',self.hProject,'-location ',tmp_str, oth_param)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
    
    def stc_create_rx_port(self,oth_param='-useDefaultHost False'):
        #print '##### stc_create_rx_port fuction #####'
        #print "Creating rx ports ..."
        msg = 'Creating rx ports ...' 
        log_print(msg)
        tmp_str = '//'+self.ChassisIp+'/'+self.iRxSlot+'/'+self.iRxPort
        if self.errorFlag == False:
            return self.errorFlag
        try:
            self.hPortRx = self.stc_create('port','-under ',self.hProject,'-location ',tmp_str, oth_param)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
        return self.errorFlag
    
    
    def vlan_create_stream(self):
        print '##### vlan_create_stream fuction #####'
        #print 'self.Vlan_id:',self.Vlan_id 
        msg = 'self.Vlan_id:' 
        log_print(msg)
        msg = self.Vlan_id 
        log_print(msg)
        if len(self.Vlan_id)==2:
            pass
        else:
            if self.Vlan_id[0].find('NULL')<0:
                try:
                    tmp_str = 'vlans -under '
                    # Add a Vlan container object.
                    #print 'add a Vlan container object'
                    msg = 'add a Vlan container object'
                    log_print(msg)
                    self.hVlanContainer = self.stc_create(tmp_str,self.hEthernet)
                    #print 'add a Vlan header'
                    msg = 'add a Vlan header'
                    log_print(msg)
                    tmp_str = 'Vlan -under '
                    self.stc_create(tmp_str,self.hVlanContainer,'-pri',self.Vlan_pri,'-cfi',self.Vlan_cfi,'-id',self.Vlan_id[0] )
                    
                except Exception ,exc_str:
                    self.stc_print_flag_error(exc_str)
                    return self.errorFlag
        return self.errorFlag
                    
            
    def stc_realtime_result(self):
        #"Subscribe to realtime results"
        if self.errorFlag == False:
            return self.errorFlag
        #print "#####Subscribe to realtime results#####"
        msg = '#####Subscribe to realtime results#####'
        log_print(msg)
        try:   
            tmpstr1 =  ' -configType Analyzer -resultParent ' 
            tmpstr2 = ' -resultType FilteredStreamResults -filenamePrefix "FilteredStreamResults" -interval 1'
            self.hResultDataSetFiltered = self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPortRx,tmpstr2)
            #print 'hResultDataSetFiltered:',self.hResultDataSetFiltered
            msg = 'hResultDataSetFiltered:' + self.hResultDataSetFiltered
            log_print(msg)
            tmpstr1 =' -configType Generator -resultParent '
            tmpstr2 =' -resultType GeneratorPortResults -filenamePrefix "Generators" -interval 1'
            self.hResultsDataSetSend = self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPortTx,tmpstr2)
            #print 'self.hResultsDataSetSend:',self.hResultsDataSetSend
            msg = 'self.hResultsDataSetSend:' + self.hResultsDataSetSend
            log_print(msg)
            tmpstr1 = '-ConfigType Analyzer -resultParent '
            tmpstr2 = '-resulttype AnalyzerPortResults -filenameprefix "Analyzer_Port_Results" -interval 1'
            self.hResultsDataSetReceived = self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPortRx,tmpstr2)
            #print 'self.hResultsDataSetReceived:',self.hResultsDataSetReceived
            msg = 'self.hResultsDataSetReceived:' + self.hResultsDataSetReceived
            log_print(msg)
            #self.stc_apply()
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
        
    def stc_filter_temp_ethernetii(self):
        if self.errorFlag == False:
            return self.errorFlag
        try:
            tmp_str = 'ethernet:EthernetII -under'
            
            if self.Filter_srcMac.find('NULL')>-1 and self.Filter_dstMac.find('NULL')>-1:
                return self.errorFlag 
            elif self.Filter_srcMac.find('NULL')>-1:
                tmp_str_other = '-dstMac "' + self. Filter_dstMac +'"'
            elif self.Filter_dstMac.find('NULL')>-1:
                tmp_str_other = '-name af1_eth -srcMac "' +self.Filter_srcMac +'"'
            else:
                tmp_str_other = '-name af1_eth -srcMac "' +self.Filter_srcMac + '" -dstMac "' + self. Filter_dstMac +'"'
            self.stc_create(tmp_str,self.hAnalyzerFrameConfigFilter,tmp_str_other)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        #print 'hAnalyzerFrameConfigFilter:',self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
        msg = 'hAnalyzerFrameConfigFilter:'+self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
        log_print(msg)
        return self.errorFlag  
    
    
    def stc_filter_temp_use2(self):
        if self.errorFlag == False:
            return self.errorFlag
        try:
            tmpstr = ' -FrameConfig ' + self.Filter_FrameConfig +' -Summary ' + self.Filter_Summary
            self.stc_config(self.hAnalyzerFrameConfigFilter, tmpstr)
            #print 'hAnalyzerFrameConfigFilter:',self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
            msg = 'hAnalyzerFrameConfigFilter:'+self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
            log_print(msg)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
    
    def stc_filter_temp_vlan(self):
        if self.errorFlag == False:
            return self.errorFlag
        tmp_str = 'Vlan -under '
        try:
            if self.Filter_vlanID.find('NULL')>-1:
                return self.errorFlag 
            else:
                tmp_str_other = '-name af1_vlan -id "' + self.Filter_vlanID + '"'
            self.stc_create(tmp_str,self.hAnalyzerFrameConfigFilter,tmp_str_other)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        #print 'hAnalyzerFrameConfigFilter:',self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
        msg = 'hAnalyzerFrameConfigFilter:' + self.stc_get(self.hAnalyzerFrameConfigFilter,' -FrameConfig')
        log_print(msg)
        return self.errorFlag
    
    def stc_filter_config(self):
        #print '##### stc_filter_config fuction #####'
        if self.errorFlag == False:
            return self.errorFlag
        if self.Filter_config_Use == 0:
            return self.errorFlag
        #print "Configuring analyzer frame config filter ..."
        msg = 'Configuring analyzer frame config filter ...'
        log_print(msg)
        tmp_str = 'AnalyzerFrameConfigFilter -under '
        tmp_str_other ='-FrameConfig ""'
        
        self.hAnalyzerFrameConfigFilter=self.stc_create(tmp_str,self.hAnalyzer,tmp_str_other)
        
        if self.Filter_config_Use == '1':
            self.stc_filter_temp_ethernetii()
            self.stc_filter_temp_vlan()
        elif self.Filter_config_Use == '2':
            self.stc_filter_temp_use2()
        elif self.Filter_config_Use == '3':
            pass
        #self.stc_apply()
        return self.errorFlag
        
    def stc_create_stream(self,filename='',sheetname = 'stream'):
        #print '##### stc_create_stream fuction #####'
        if filename=='':
            path = os.path.abspath(sys.argv[0])
            findstr = 'Simu'
            path_parent = Getfindpath(path,findstr)
            filename = path_parent + '\\auto_conf\\stream_param.xls'
        self.stc_initpare(filename,sheetname)
       
        self.stc_create_pro()
        self.stc_create_tx_port()
        self.stc_create_rx_port()
        
        
        if self.errorFlag == False:
            return self.errorFlag
        try:
            #self.hPortTxCopperInterface = self.stc_create('EthernetCopper','-under ',self.hPortTx)
            
            #print "Configure physical interface..."
            msg = 'Configure physical interface...'
            log_print(msg)
            self.hPortTxCopperInterface = self.stc_create('EthernetCopper','-under ',self.hPortTx)
            self.stc_eval()
            #print 'Connecting ',self.ChassisIp,' ...'
            msg = 'Connecting ' + self.ChassisIp +' ...'
            log_print(msg)
            self.stc_eval()
            #print "Set up port mappings..."
            msg = 'Set up port mappings...'
            log_print(msg)
            #print 'SetupPortMappings: ',self.stc_perform('SetupPortMappings')
            tmp_str_tx = '\"' +'//'+self.ChassisIp+'/'+self.iTxSlot+'/'+self.iTxPort +'\"' 
            tmp_str_rx = '\"' + '//'+self.ChassisIp+'/'+self.iRxSlot+'/'+self.iRxPort + '\"'
            tmp_str = '\"'  + self.hPortTx + ' ' + self.hPortRx + '\"'
            self.stc_perform('attachPorts -portlist' , tmp_str)
            
            #print  "Apply configuration..."
            msg = 'Apply configuration...'
            log_print(msg)
            self.stc_apply()
            #print 'Retrieve the generator and analyzer objects'
            msg = 'Retrieve the generator and analyzer objects'
            log_print(msg)
            self.hGenerator =self.stc_get(self.hPortTx,'-children-Generator')
            #print 'self.hGenerator1:',self.hGenerator
            msg = 'self.hGenerator1:' + self.hGenerator
            log_print(msg)
            self.hAnalyzer = self.stc_get(self.hPortRx,'-children-Analyzer')
            #print 'self.hAnalyzer:',self.hAnalyzer
            msg = 'self.hAnalyzer:' + self.hAnalyzer
            log_print(msg)
            #print "Configuring stream block ..."
            msg = 'Configuring stream block ...'
            log_print(msg)
            tmp_str = '-insertSig ' +self.insertSig +  '  -frameConfig "" ' + '  -frameLengthMode ' + self.frameLengthMode + ' -maxFrameLength ' +self.maxFrameLength + ' -FixedFrameLength ' +self.FixedFrameLength
            self.hStreamBlock = self.stc_create('streamBlock -under',self.hPortTx,tmp_str)
            time.sleep(3)
            #print '............'
            #print "Adding headers..."
            msg = 'Adding headers...'
            log_print(msg)
            self.hEthernet = self.stc_create('ethernet:EthernetII -under',self.hStreamBlock,'-name sb1_eth',' -srcMac ',self.srcMac,'-dstMac ',self.dstMac)
            
            self.vlan_create_stream()
            
            #self.stc_create('ipv4:IPv4 -under ',self.hStreamBlock,' -name sb1_ip -sourceAddr 10.0.0.2 -destAddr 192.168.1.1')
            self.stc_apply()
            self.stc_filter_config()
            
            #print "Creating Modifier on Stream Block ..."
            msg = 'Creating Modifier on Stream Block ...'
            log_print(msg)
            Mask = '\"'+self.Mask+'\"'
            StepValue = '\"'+self.StepValue+'\"'
            Data = '\"'+self.Data +'\"'
            other_str = '-RecycleCount '+self.RecycleCount+' -RepeatCount '+self.RepeatCount+' -DataType '+self.DataType+' -EnableStream '+self.EnableStream+' -Offset '+self.Offset+' -OffsetReference \"'+self.OffsetReference+'\"'
            self.hRangeModifier = self.stc_create('RangeModifier -under ',self.hStreamBlock,'-ModifierMode ',self.ModifierMode,' -Mask',Mask,'-StepValue',StepValue,'-Data',Data,other_str)
            
            #print"\n\nStreamBlock information..."
            msg = '\n\nStreamBlock information...'
            log_print(msg)
            self.lstStreamBlockInfo = self.stc_perform('StreamBlockGetInfo -StreamBlock',self.hStreamBlock)
            #print 'lstStreamBlockInfo:',self.lstStreamBlockInfo
            msg = 'lstStreamBlockInfo:'+self.lstStreamBlockInfo
            log_print(msg)
            
            #print "Configuring Generator..."
            msg = 'Configuring Generator...'
            log_print(msg)
            self.hGeneratorConfig = self.stc_get(self.hGenerator,' -children-GeneratorConfig ')
           # print 'self.hGeneratorConfig1:',self.hGeneratorConfig
            msg = 'self.hGeneratorConfig1:' + self.hGeneratorConfig
            log_print(msg)
            
            #load Generator Configure
            if self.Generator_con_type.find('2')>-1:
                tmp_str = self.Generator_con_type_load
            else:
                tmp_str = '-DurationMode '+self.DurationMode+' -BurstSize '+self.BurstSize+' -Duration '+self.Duration+' -LoadMode '+self.LoadMode+' -FixedLoad '+self.FixedLoad+' -LoadUnit '+self.LoadUnit+' -SchedulingMode '+self.SchedulingMode
            self.stc_config(self.hGeneratorConfig,tmp_str)
            #print 'hGeneratorConfig2:',self.hGeneratorConfig
            msg = 'hGeneratorConfig2:'+self.hGeneratorConfig
            log_print(msg)
            
            #print 'Subscribe to results'
            msg = 'Subscribe to results' 
            log_print(msg)
            self.stc_realtime_result()
            
            
            #print "Configuring Analyzer..."
            msg = 'Configuring Analyzer...' 
            log_print(msg)
            tmp_str = '-children-AnalyzerConfig'
            #print 'self.hAnalyzer:',self.hAnalyzer
            msg = 'self.hAnalyzer:' + self.hAnalyzer
            log_print(msg)
            self.hAnalyzerConfig = self.stc_get(self.hAnalyzer,tmp_str)
           
            #print "Configure Capture"
            msg = 'Configure Capture'
            log_print(msg)
            if ENABLE_CAPTURE==1:
                #print '\nStarting Capture...'
                msg = '\nStarting Capture...'
                log_print(msg)
                tmp_str ='-children-capture'
                self.hCapture = self.stc_get(self.hPortRx,tmp_str)
                tmp_str = '-mode REGULAR_MODE -srcMode TX_RX_MODE'
                self.stc_config(self.hCapture,tmp_str)
                tmp_str = 'CaptureStart -captureProxyId'
                self.stc_perform(tmp_str,self.hCapture)
                
            #print 'Apply configuration'
            msg = 'Apply configuration'
            log_print(msg)
            self.stc_apply()
            #print "\nSave configuration as an XML file."
            msg = '\nSave configuration as an XML file.'
            log_print(msg)
            tmp_str = 'SaveAsXml'
            self.stc_perform(tmp_str)
            
        except Exception ,exc_str:
            #print 'Exception.....stc_create_stream'
            msg = 'Exception.....stc_create_stream'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        
        return self.errorFlag
        
    
    def stc_release_testcenter(self):
        #print '##### stc_release_testcenter fuction #####'
        if self.errorFlag == False:
            return self.errorFlag
        try:
            #print "Releasing ports .."
            msg = 'Releasing ports ..'
            log_print(msg)
            tmp_str = self.ChassisIp+'/'+ self.iTxSlot + '/'+self.iTxPort
            tmp_str1 = self.ChassisIp+'/'+ self.iRxSlot + '/'+self.iRxPort
            self.stc_release(tmp_str,tmp_str1)
            #print 'Disconnect from the chassis ...'
            msg = 'Disconnect from the chassis ...'
            log_print(msg)
            self.stc_disconnect(self.ChassisIp)
            # Delete configuration
            #print "Deleting project"
            msg = 'Deleting project'
            log_print(msg)
            self.stc_delete(self.hProject)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
        
    def stc_traffic_stream(self):
        #print '##### traffic_stream fuction #####'
        msg = '##### traffic_stream fuction #####'
        log_print(msg)
        if self.errorFlag == False:
            return self.errorFlag
        #print "Start Analyzer"
        msg = 'Start Analyzer'
        log_print(msg)
        try:
            tmp_str = 'AnalyzerStart -AnalyzerList'
            self.stc_perform(tmp_str,self.hAnalyzer)
            tmp_str = ' -state'
            #print 'Current analyzer state',self.stc_get(self.hAnalyzer,tmp_str)
            msg = 'Current analyzer state' + self.stc_get(self.hAnalyzer,tmp_str)
            log_print(msg)
            #print "Start Generator"
            msg = 'Start Generator'
            log_print(msg)
            tmp_str = 'GeneratorStart -GeneratorList'
            self.stc_perform(tmp_str,self.hGenerator)
            tmp_str = ' -state'
            #print 'Current generator state ',self.stc_get(self.hGenerator,tmp_str)
            msg = 'Current generator state '+self.stc_get(self.hGenerator,tmp_str)
            log_print(msg)
            #print 'wait ',self.waittime,' seconds'
            
            msg = 'wait '+ str(self.waittime)+' seconds'
            log_print(msg)
            time.sleep(self.waittime)
            #print 'Current analyzer state ',self.stc_get(self.hAnalyzer,tmp_str)
            msg = 'Current analyzer state '+self.stc_get(self.hAnalyzer,tmp_str)
            log_print(msg)
            #print 'Current generator state ',self.stc_get(self.hGenerator,tmp_str)
            msg = 'Current generator state '+self.stc_get(self.hGenerator,tmp_str)
            log_print(msg)
            #print 'stop analyzer'
            msg = 'stop analyzer'
            log_print(msg)
            tmp_str ='GeneratorStop -GeneratorList'
            self.stc_perform(tmp_str,self.hGenerator)
            
            
            #print 'Stop the analyzer.'
            msg = 'Stop the analyzer.'
            log_print(msg)
            tmp_str ='AnalyzerStop -AnalyzerList'
            self.stc_perform(tmp_str,self.hAnalyzer)
            
            tmp_str =' -children-GeneratorPortResults'
            self.hGeneratorResults = self.stc_get( self.hGenerator,tmp_str)
            tmp_str = '-children-AnalyzerPortResults'
            self.hAnalyzerResults = self.stc_get(self.hAnalyzer,tmp_str)
            
            #print 'wait 20S AnalyzerResult'
            msg = 'wait 20S AnalyzerResult'
            log_print(msg)
            time.sleep(20)
            #print "Frames Counts:"
            msg = 'Frames Counts:'
            log_print(msg)
            tmp_str = '-sigFrameCount'
            #print '\tSignature frames:',self.stc_get(self.hAnalyzerResults,tmp_str)
            msg = '\tSignature frames:' + self.stc_get(self.hAnalyzerResults,tmp_str)
            log_print(msg)
            tmp_str = '-totalFrameCount'
            #print '\tTotal frames',self.stc_get(self.hAnalyzerResults,tmp_str)
            msg = '\tTotal frames'+self.stc_get(self.hAnalyzerResults,tmp_str)
            log_print(msg)
            tmpstr = ' -GeneratorFrameCount'
            #print 'Send packets:', self.stc_get(self.hGeneratorResults,tmpstr)
            msg = 'Send packets:'+ self.stc_get(self.hGeneratorResults,tmpstr)
            log_print(msg)
            tmpstr = '-totalFrameCount'
            #print 'Received packets:', self.stc_get(self.hAnalyzerResults,tmpstr)
            msg = 'Received packets:'+self.stc_get(self.hAnalyzerResults,tmpstr)
            log_print(msg)
            for x in self.ParamGeneratorPort:
                self.stc_result_print(x,port_str='GeneratorPort')
            for x in self.ParamAnalyzerPort:
                 self.stc_result_print(x,port_str='AnalyzerPort')
            
            #print '################ this result case ################'
            msg = '################ this result case ################'
            log_print(msg)
            self.resultFlag =self.stc_result_compare()
            #print '################ this result case ################'
            msg = '################ this result case ################'
            log_print(msg)
            if ENABLE_CAPTURE==1:
                #print 'Retrieving Captured frames...'
                msg = 'Retrieving Captured frames...'
                log_print(msg)
                tmp_str = 'CaptureStop -captureProxyId' 
                self.stc_perform(tmp_str,self.hCapture)
                tmp_str = 'CaptureDataSave -captureProxyId'
                strTime = time.strftime(KEY_TIME_FORMAT)
                tmp_filename = self.FileName +'_'+strTime
                #print 'tmp_filename:',tmp_filename
                msg = 'tmp_filename:' + tmp_filename
                log_print(msg)
                tmp_str_other = '-FileName "'+tmp_filename+'.pcap" -FileNameFormat PCAP -IsScap FALSE'
                self.stc_perform(tmp_str,self.hCapture,tmp_str_other)
                tmp_str = '-PktCount'
                #print 'Captured frames:',self.stc_get(self.hCapture,tmp_str)
                msg = 'Captured frames:'+self.stc_get(self.hCapture,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
    
    def stc_result_compare_type_eq(self,handle,handvalue):
        print 'Comparing eq ...'
        print 'handle:',handle,'handvalue:',handvalue
        tmpstr = '-'+handvalue[0]
        value  = string.atoi(handvalue[1])
        tm_st = self.stc_get(handle,tmpstr)
        #print 'get  ',handle,' result value:',tm_st
        tmp_port_print =self.stc_get_datafromstr(handle)
        msg = 'get ' + handle + ' result value:' + tm_st +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg = handvalue[1]
        log_print(msg)
        print 'get_value:',tm_st, ' == ','value:',value
        if string.atoi(tm_st)== value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase pass,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_greater(self,handle,handvalue):
        print 'Comparing greater ...'
        print 'handle:',handle,'handvalue:',handvalue
        tmpstr = '-'+handvalue[0]
        value  = string.atoi(handvalue[1])
        tm_st = self.stc_get(handle,tmpstr)
        #print 'get  ',handle,' result value:',tm_st
        tmp_port_print =self.stc_get_datafromstr(handle)
        msg = 'get ' + handle + ' result value:' + tm_st +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg = handvalue[1]
        log_print(msg)
        tm_st = self.stc_get(handle,tmpstr)
        print 'get_value:',tm_st, ' > ','value:',value
        if string.atoi(tm_st)> value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase pass,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_small(self,handle,handvalue):
        print 'Comparing small ...'
        print 'handle:',handle,'handvalue:',handvalue
        tmpstr = '-'+handvalue[0]
        value  = string.atoi(handvalue[1])
        tm_st = self.stc_get(handle,tmpstr)
        #print 'get  ',handle,' result value:',tm_st
        tmp_port_print =self.stc_get_datafromstr(handle)
        msg = 'get ' + handle + ' result value:' + tm_st  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg = handvalue[1]
        log_print(msg)
        print 'get_value:',tm_st, ' < ','value:',value
        if string.atoi(tm_st)< value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase pass,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_greater_eq(self,handle,handvalue):
        print 'Comparing greater and eq ...'
        print 'handle:',handle,'handvalue:',handvalue
        tmpstr = '-'+handvalue[0]
        value  = string.atoi(handvalue[1])
        tm_st = self.stc_get(handle,tmpstr)
        #print 'get  ',handle,' result value:',tm_st
        tmp_port_print =self.stc_get_datafromstr(handle)
        msg = 'get ' + handle + ' result value:' + tm_st  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg = handvalue[1]
        log_print(msg)
        print 'get_value:',tm_st, ' >= ','value:',value
        if string.atoi(tm_st)>= value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase pass,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_small_eq(self,handle,handvalue):
        print 'Comparing small and eq ...'
        print 'handle:',handle,'handvalue:',handvalue
        tmpstr = '-'+handvalue[0]
        value  = string.atoi(handvalue[1])
        tm_st = self.stc_get(handle,tmpstr)
        #print 'get ',handle,' result value:',tm_st
        tmp_port_print =self.stc_get_datafromstr(handle)
        msg = 'get ' + handle + ' result value:' + tm_st  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg = handvalue[1]
        log_print(msg)
        print 'get_value:',tm_st, ' <= ','value:',value
        if string.atoi(tm_st)<= value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase pass,NG ***************'
            msg  = '*************** this testcase pass,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    
    
    def stc_result_compare_type_eq_port(self,handle_Generator_both,handle_Analyzer_both,handle_GcA,tmp_GcA):
        print 'Comparing Port eq ...'
        print 'handle_GcA:',handle_GcA,'tmp_GcA:',tmp_GcA
        tmpstr1 = '-'+handle_GcA
        tmpstr2 = '-'+tmp_GcA[0]
        value = string.atoi(tmp_GcA[1])
        #print '---------------value:',value
        tm_st1 = self.stc_get(handle_Analyzer_both,tmpstr1)
        tm_st2 = self.stc_get(handle_Generator_both,tmpstr2)
        
        #print 'get  AnalyzerResults result value:',tm_st1
        tmp_port_print =self.stc_get_datafromstr(handle_Analyzer_both)
        msg  = 'get  AnalyzerResults result value:' + tm_st1  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'get GeneratorResults result value:',tm_st2
        tmp_port_print =self.stc_get_datafromstr(handle_Generator_both)
        msg  = 'get GeneratorResults result value:' + tm_st2  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg  = 'compile value:' + tmp_GcA
        log_print(msg)
        
        #tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        print 'get_value:',tmp_value,' == ','value:',value
        if tmp_value == value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase fail,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_greater_port(self,handle_Generator_both,handle_Analyzer_both,handle_GcA,tmp_GcA):
        print 'Comparing Port greater ...'
        print 'handle_GcA:',handle_GcA,'tmp_GcA:',tmp_GcA
        tmpstr1 = '-'+handle_GcA
        tmpstr2 = '-'+tmp_GcA[0]
        value = string.atoi(tmp_GcA[1])
        #print '---------------value:',value
        tm_st1 = self.stc_get(handle_Analyzer_both,tmpstr1)
        tm_st2 = self.stc_get(handle_Generator_both,tmpstr2)
        
        
        #print 'get  AnalyzerResults result value:',tm_st1
        tmp_port_print =self.stc_get_datafromstr(handle_Analyzer_both)
        msg  = 'get  AnalyzerResults result value:' + tm_st1+' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'get GeneratorResults result value:',tm_st2
        tmp_port_print =self.stc_get_datafromstr(handle_Generator_both)
        msg  = 'get GeneratorResults result value:' + tm_st2+' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg  = 'compile value:' + tmp_GcA[1]
        log_print(msg)
        
        #tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        print 'get_value:',tmp_value,' > ','value:',value
        if tmp_value > value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase fail,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_small_port(self,handle_Generator_both,handle_Analyzer_both,handle_GcA,tmp_GcA):
        print 'Comparing Port small ...'
        print 'handle_GcA:',handle_GcA,'tmp_GcA:',tmp_GcA
        tmpstr1 = '-'+handle_GcA
        tmpstr2 = '-'+tmp_GcA[0]
        value = string.atoi(tmp_GcA[1])
        #print '---------------value:',value
        tm_st1 = self.stc_get(handle_Analyzer_both,tmpstr1)
        tm_st2 = self.stc_get(handle_Generator_both,tmpstr2)
        
        #print 'get  AnalyzerResults result value:',tm_st1
        tmp_port_print =self.stc_get_datafromstr(handle_Analyzer_both)
        msg  = 'get  AnalyzerResults result value:' + tm_st1+' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'get GeneratorResults result value:',tm_st2
        tmp_port_print =self.stc_get_datafromstr(handle_Generator_both)
        msg  = 'get GeneratorResults result value:' + tm_st2+' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg  = 'compile value:' + tmp_GcA[1]
        log_print(msg)
        
        #tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        print 'get_value:',tmp_value,' < ','value:',value
        if tmp_value < value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase fail,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_greater_eq_port(self,handle_Generator_both,handle_Analyzer_both,handle_GcA,tmp_GcA):
        print 'Comparing Port greater and eq ...'
        print 'handle_GcA:',handle_GcA,'tmp_GcA:',tmp_GcA
        tmpstr1 = '-'+handle_GcA
        tmpstr2 = '-'+tmp_GcA[0]
        value = string.atoi(tmp_GcA[1])
        #print '---------------value:',value
        tm_st1 = self.stc_get(handle_Analyzer_both,tmpstr1)
        tm_st2 = self.stc_get(handle_Generator_both,tmpstr2)
        
        #print 'get  AnalyzerResults result value:',tm_st1
        tmp_port_print =self.stc_get_datafromstr(handle_Analyzer_both)
        msg  = 'get  AnalyzerResults result value:' + tm_st1 +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'get GeneratorResults result value:',tm_st2
        tmp_port_print =self.stc_get_datafromstr(handle_Generator_both)
        msg  = 'get GeneratorResults result value:' + tm_st2 +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg  = 'compile value:' + tmp_GcA[1]
        log_print(msg)
        
        #tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        print 'get_value:',tmp_value,' >= ','value:',value
        if tmp_value >= value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase fail,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    
    def stc_result_compare_type_small_eq_port(self,handle_Generator_both,handle_Analyzer_both,handle_GcA,tmp_GcA):
        print 'Comparing Port small and eq ...'
        print 'handle_GcA:',handle_GcA,'tmp_GcA:',tmp_GcA
        tmpstr1 = '-'+ handle_GcA
        tmpstr2 = '-'+ tmp_GcA[0]
        value = string.atoi(tmp_GcA[1])
        #print '---------------value:',value
        tm_st1 = self.stc_get(handle_Analyzer_both,tmpstr1)
        tm_st2 = self.stc_get(handle_Generator_both,tmpstr2)
        
        #print 'get  AnalyzerResults result value:',tm_st1
        tmp_port_print =self.stc_get_datafromstr(handle_Analyzer_both)
        msg  = 'get  AnalyzerResults result value:' + tm_st1 +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'get GeneratorResults result value:',tm_st2
        tmp_port_print =self.stc_get_datafromstr(handle_Generator_both)
        msg  = 'get GeneratorResults result value:' + tm_st2 +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
        log_print(msg)
        #print 'compile value:',value
        msg  = 'compile value:' + tmp_GcA[1]
        log_print(msg)
        #tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        tmp_value = string.atoi(tm_st1)*10000/string.atoi(tm_st2)
        print 'get_value:',tmp_value,' <= ','value:',value
        if tmp_value <= value:
            #print '*************** this testcase pass,OK ***************'
            msg  = '*************** this testcase pass,OK ***************'
            log_print(msg)
            self.errorFlag = True
        else:
            #print '*************** this testcase fail,NG ***************'
            msg  = '*************** this testcase fail,NG ***************'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
    def stc_yy_compare(self,handle_Generator='',handle_Analyzer = '',handle_GcA = '',FilterStream_Result_value=''):
        print 'starting yy_compare ...'
        if  handle_Generator=='':
            handle_Generator= self.hGeneratorResults
        #if handle_Generator_both=='':
        #    handle_Generator_both =self.hGeneratorResults
        if handle_Analyzer =='':
            handle_Analyzer = self.hAnalyzerResults
        #if handle_Analyzer_both=='':
        #    handle_Analyzer_both = self.hAnalyzerResults
        if FilterStream_Result_value=='':
            FilterStream_Result_value = self.FilterStream_Result_t
        
        handle_Generator_value = self.ParamGeneratorPortvalue
        handle_Analyzer_value = self.ParamAnalyzerPortvalue
        #handle_GcA = self.ParamGeneratorPort_compare_AnalyzerPort
        
        if (self.compare_pass_type.find('0')>-1):         #Ϊģʽ 1�� ֻ�Ƚ�ParamGeneratorPortvalue��ֵ
            self.stc_yy_compareType0(handle_Generator,handle_Generator_value)

            
        elif(self.compare_pass_type.find('1')>-1):
            self.stc_yy_compareType1(handle_Analyzer,handle_Analyzer_value)

             
        elif (self.compare_pass_type.find('2')>-1):
            self.stc_yy_compareType2(handle_GcA)

             
        elif (self.compare_pass_type.find('3')>-1):
            if self.stc_yy_compareType0(handle_Generator,handle_Generator_value)== True:
                self.stc_yy_compareType1(handle_Analyzer,handle_Analyzer_value)

                         
        elif (self.compare_pass_type.find('4')>-1):
            if self.stc_yy_compareType0(handle_Generator,handle_Generator_value) == True:
                self.stc_yy_compareType2(handle_GcA)
                
        elif (self.compare_pass_type.find('5')>-1):
            if self.stc_yy_compareType0(handle_Analyzer,handle_Analyzer_value) == True:
                self.stc_yy_compareType2(handle_GcA)
        
        elif (self.compare_pass_type.find('6')>-1):
            if self.stc_yy_compareType0(handle_Analyzer,handle_Analyzer_value) == True:
                if self.stc_yy_compareType1(handle_Generator,handle_Generator_value) == True:
                    self.stc_yy_compareType2(handle_GcA)
                    
        elif (self.compare_pass_type.find('7')>-1):
            print 'comparing type 7 ...'
            self.stc_filter_value_compile()
        #print 'self.errorFlag:',self.errorFlag
        return self.errorFlag
        
    def stc_yy_compareType0(self,handle_Generator,handle_Generator_value):
        print 'begining compare type 0 ...'
        tmpresult = True
        for x in handle_Generator_value:     # #['SigFrameCount>0' , 'SigFrameCount<10']
            tmp = re.findall(str_sign,x)
            tmp_Generator_value = x.split(tmp[0])  #['SigFrameCount','0']
            if tmp[0] == '==':
                results = self.stc_result_compare_type_eq(handle_Generator , tmp_Generator_value)
            elif tmp[0] == '>':
                results = self.stc_result_compare_type_greater(handle_Generator , tmp_Generator_value)
            elif tmp[0] == '<':
                results = self.stc_result_compare_type_small(handle_Generator,tmp_Generator_value)
            elif tmp[0] == '>=':
                results = self.stc_result_compare_type_greater_eq(handle_Generator,tmp_Generator_value)
            elif tmp[0] == '<=':
                results = self.stc_result_compare_type_small_eq(handle_Generator,tmp_Generator_value)
            else:
                self.errorFlag = False
            if results == False:
                tmpresult = False
        self.errorFlag = tmpresult
        return self.errorFlag    
    
    def stc_yy_compareType1(self,handle_Analyzer,handle_Analyzer_value):
        print 'begining compare type 1 ...'
        tmpresult = True
        for x in handle_Analyzer_value:     # #['SigFrameCount>0' , 'SigFrameCount<10']
            tmp = re.findall(str_sign,x)
            tmp_Analyzer_value = x.split(tmp[0])  #['SigFrameCount','0']
            if tmp[0] == '==':
                results = self.stc_result_compare_type_eq(handle_Analyzer , tmp_Analyzer_value)
            elif tmp[0] == '>':
                results = self.stc_result_compare_type_greater(handle_Analyzer , tmp_Analyzer_value)
            elif tmp[0] == '<':
                results = self.stc_result_compare_type_small(handle_Analyzer,tmp_Analyzer_value)
            elif tmp[0] == '>=':
                results = self.stc_result_compare_type_greater_eq(handle_Analyzer,tmp_Analyzer_value)
            elif tmp[0] == '<=':
                results = self.stc_result_compare_type_small_eq(handle_Analyzer,tmp_Analyzer_value)
            else:
                self.errorFlag = False
            if results == False:
                tmpresult = False
        self.errorFlag = tmpresult
        return self.errorFlag   
                  
    def stc_yy_compareType2(self,handle):              ##['6/12:SigFrameCount ,6/11:GeneratorSigFrameCount>=100','6/12:SigFrameCount ,6/11:GeneratorSigFrameCount<=1000']
        print 'begining compare type 2 ...'
        '''
        print 'handle_Generator_both:\n'
        print 'handle_Analyzer_both:\n'
        print 'handle_GcA:\n'
        '''
        tmpresult = True
        for x in handle:          #x : '6/12:SigFrameCount ,6/11:GeneratorSigFrameCount>=100'
            tmp_value = x.split(',')                #  ['6/12:SigFrameCount','6/11:GeneratorSigFrameCount>=100']
            print 'x:',x
            tmp_Analyzer_port = self.stc_get_rx_hport(tmp_value[0].split(':')[0])
            self.hAnalyzerResults_both  = self.hAnalyzerResults_multi[tmp_Analyzer_port]
            tmp_Generator_port = self.stc_get_rx_hport(tmp_value[1].split(':')[0])
            self.hGeneratorResults_both = self.hGeneratorResults_multi[tmp_Generator_port]
            
            tmp = re.findall(str_sign,tmp_value[1].split(':')[1])
            tmp_GcA = tmp_value[1].split(':')[1].split(tmp[0])    #
            if tmp[0] == '==':
                results =self.stc_result_compare_type_eq_port(self.hGeneratorResults_both,self.hAnalyzerResults_both ,tmp_value[0].split(':')[1],tmp_GcA)
            elif tmp[0] == '>':
                results =self.stc_result_compare_type_greater_port(self.hGeneratorResults_both,self.hAnalyzerResults_both ,tmp_value[0].split(':')[1],tmp_GcA)
            elif tmp[0] == '<':
                results =self.stc_result_compare_type_small_port(self.hGeneratorResults_both,self.hAnalyzerResults_both ,tmp_value[0].split(':')[1],tmp_GcA)
            elif tmp[0] == '>=':
                results =self.stc_result_compare_type_greater_eq_port(self.hGeneratorResults_both,self.hAnalyzerResults_both ,tmp_value[0].split(':')[1],tmp_GcA)
            elif tmp[0] == '<=':
                results =self.stc_result_compare_type_small_eq_port(self.hGeneratorResults_both,self.hAnalyzerResults_both ,tmp_value[0].split(':')[1],tmp_GcA)
            else:
                self.errorFlag = False
            if results == False:
                tmpresult = False
        self.errorFlag  = tmpresult
        return self.errorFlag 
            

    
    def stc_result_compare(self,handle_Generator='',handle_Generator_both ='',handle_Analyzer = '',handle_Analyzer_both = '',FilterStream_Result_value=''):
        if  handle_Generator=='':
            handle_Generator= self.hGeneratorResults
        if handle_Generator_both=='':
            handle_Generator_both =self.hGeneratorResults
        if handle_Analyzer =='':
            handle_Analyzer = self.hAnalyzerResults
        if handle_Analyzer_both=='':
            handle_Analyzer_both = self.hAnalyzerResults
        if FilterStream_Result_value=='':
            FilterStream_Result_value = self.FilterStream_Result_t
        
        handle_Generator_value = self.ParamGeneratorPortvalue
        handle_Analyzer_value = self.ParamAnalyzerPortvalue
        '''
        compare_mode value:0 ->  ==＄1�7
                           1 ->  > ＄1�7
                           2 ->  < ＄1�7
                           3 ->  >=＄1�7
                           4 ->  <=,
        compare_pass_type:
          0：比较GeneratorPortvalue
          1：比较AnalyzerPortvalue
          2：比较GeneratorPort_compare_AnalyzerPort
          3：比较GeneratorPortvalue与AnalyzerPortvalue
          4：比较GeneratorPortvalue与GeneratorPort_compare_AnalyzerPort
          5：比较AnalyzerPortvalue与GeneratorPort_compare_AnalyzerPort
          6：比较AnalyzerPortvalue，GeneratorPort_compare_AnalyzerPort GeneratorPortvalue
        '''
        if self.compare_mode.find('0')>-1:
            if self.compare_pass_type.find('0')>-1:
                self.stc_result_compare_type_eq(handle_Generator,handle_Generator_value)
            elif self.compare_pass_type.find('1')>-1:
                self.stc_result_compare_type_eq(handle_Analyzer,handle_Analyzer_value)
            elif self.compare_pass_type.find('2')>-1:
                self.stc_result_compare_type_eq_port(handle_Generator_both,handle_Analyzer_both)
            elif self.compare_pass_type.find('3')>-1:
                if self.stc_result_compare_type_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('4')>-1:
                if self.stc_result_compare_type_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('5')>-1:
                if self.stc_result_compare_type_eq(handle_Analyzer,handle_Analyzer_value)==True:
                    if self.stc_result_compare_type_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('6')>-1:
                if self.stc_result_compare_type_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_eq(handle_Analyzer,handle_Analyzer_value)==True:
                        if self.stc_result_compare_type_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                            self.errorFlag =False
                    else:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('7')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]   #SigFrameCount
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]   #>100
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
            elif self.compare_pass_type.find('8')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                if self.errorFlag:
                    if self.stc_result_compare_type_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                    
            else:
                #print 'ERROR:stc_result_print param error'
                msg  = 'ERROR:stc_result_print param error'
                log_print(msg)
                self.errorFlag = False
        
        elif self.compare_mode.find('1')>-1:
            if self.compare_pass_type.find('0')>-1:
                self.stc_result_compare_type_greater(handle_Generator,handle_Generator_value)
            elif self.compare_pass_type.find('1')>-1:
                self.stc_result_compare_type_greater(handle_Analyzer,handle_Analyzer_value)
            elif self.compare_pass_type.find('2')>-1:
                self.stc_result_compare_type_greater_port(handle_Generator_both,handle_Analyzer_both)
                return self.errorFlag
            elif self.compare_pass_type.find('3')>-1:
                if self.stc_result_compare_type_greater(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
                return self.errorFlag
            elif self.compare_pass_type.find('4')>-1:
                if self.stc_result_compare_type_greater(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('5')>-1:
                if self.stc_result_compare_type_greater(handle_Analyzer,handle_Analyzer_value)==True:
                    if self.stc_result_compare_type_greater_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('6')>-1:
                if self.stc_result_compare_type_greater(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater(handle_Analyzer,handle_Analyzer_value)==True:
                        if self.stc_result_compare_type_greater_port(handle_Generator_both,handle_Analyzer_both)==False:
                            self.errorFlag =False
                    else:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('7')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                
            elif self.compare_pass_type.find('8')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                if self.errorFlag:
                    if self.stc_result_compare_type_greater(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
            else:
                #print 'ERROR:stc_result_print param error'
                msg  = 'ERROR:stc_result_print param error'
                log_print(msg)
                self.errorFlag = False
            
        elif self.compare_mode.find('2')>-1:
            if self.compare_pass_type.find('0')>-1:
                self.stc_result_compare_type_small(handle_Generator,handle_Generator_value)
            elif self.compare_pass_type.find('1')>-1:
                self.stc_result_compare_type_small(handle_Analyzer,handle_Analyzer_value)
            elif self.compare_pass_type.find('2')>-1:
                self.stc_result_compare_type_small_port(handle_Generator_both,handle_Analyzer_both)
                return self.errorFlag
            elif self.compare_pass_type.find('3')>-1:
                if self.stc_result_compare_type_small(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
                return self.errorFlag
            elif self.compare_pass_type.find('4')>-1:
                if self.stc_result_compare_type_small(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('5')>-1:
                if self.stc_result_compare_type_small(handle_Analyzer,handle_Analyzer_value)==True:
                    if self.stc_result_compare_type_small_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('6')>-1:
                if self.stc_result_compare_type_small(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small(handle_Analyzer,handle_Analyzer_value)==True:
                        if self.stc_result_compare_type_small_port(handle_Generator_both,handle_Analyzer_both)==False:
                            self.errorFlag =False
                    else:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('7')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
            
            elif self.compare_pass_type.find('8')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                if self.errorFlag:
                    if self.stc_result_compare_type_small(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                        
            else:
                #print 'ERROR:stc_result_print param error'
                msg  = 'ERROR:stc_result_print param error'
                log_print(msg)
                self.errorFlag = False
        elif self.compare_mode.find('3')>-1:
            if self.compare_pass_type.find('0')>-1:
                self.stc_result_compare_type_greater_eq(handle_Generator,handle_Generator_value)
            elif self.compare_pass_type.find('1')>-1:
                self.stc_result_compare_type_greater_eq(handle_Analyzer,handle_Analyzer_value)
            elif self.compare_pass_type.find('2')>-1:
                self.stc_result_compare_type_greater_eq_port(handle_Generator_both,handle_Analyzer_both)
                return self.errorFlag
            elif self.compare_pass_type.find('3')>-1:
                if self.stc_result_compare_type_greater_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
                return self.errorFlag
            elif self.compare_pass_type.find('4')>-1:
                if self.stc_result_compare_type_greater_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('5')>-1:
                if self.stc_result_compare_type_greater_eq(handle_Analyzer,handle_Analyzer_value)==True:
                    if self.stc_result_compare_type_greater_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('6')>-1:
                if self.stc_result_compare_type_greater_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_greater_eq(handle_Analyzer,handle_Analyzer_value)==True:
                        if self.stc_result_compare_type_greater_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                            self.errorFlag =False
                    else:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('7')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
            
            elif self.compare_pass_type.find('8')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                if self.errorFlag:
                    if self.stc_result_compare_type_greater_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                        
            else:
                #print 'ERROR:stc_result_print param error'
                msg  = 'ERROR:stc_result_print param error'
                log_print(msg)
                self.errorFlag = False
        elif self.compare_mode.find('4')>-1:
            if self.compare_pass_type.find('0')>-1:
                self.stc_result_compare_type_small_eq(handle_Generator,handle_Generator_value)
            elif self.compare_pass_type.find('1')>-1:
                self.stc_result_compare_type_small_eq(handle_Analyzer,handle_Analyzer_value)
            elif self.compare_pass_type.find('2')>-1:
                self.stc_result_compare_type_small_eq_port(handle_Generator_both,handle_Analyzer_both)
                return self.errorFlag
            elif self.compare_pass_type.find('3')>-1:
                if self.stc_result_compare_type_small_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
                return self.errorFlag
            elif self.compare_pass_type.find('4')>-1:
                if self.stc_result_compare_type_small_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('5')>-1:
                if self.stc_result_compare_type_small_eq(handle_Analyzer,handle_Analyzer_value)==True:
                    if self.stc_result_compare_type_small_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('6')>-1:
                if self.stc_result_compare_type_small_eq(handle_Generator,handle_Generator_value)==True:
                    if self.stc_result_compare_type_small_eq(handle_Analyzer,handle_Analyzer_value)==True:
                        if self.stc_result_compare_type_small_eq_port(handle_Generator_both,handle_Analyzer_both)==False:
                            self.errorFlag =False
                    else:
                        self.errorFlag =False
                else:
                    self.errorFlag =False
            elif self.compare_pass_type.find('7')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
            
            elif self.compare_pass_type.find('8')>-1:
                rxPort = FilterStream_Result_value.split(':')[0]
                param_cmd = FilterStream_Result_value.split(':')[1].split(',')[0]
                com_value = FilterStream_Result_value.split(':')[1].split(',')[1]
                self.stc_filter_value_compile(rxPort,param_cmd,com_value,self.compare_mode)
                if self.errorFlag:
                    if self.stc_result_compare_type_small_eq(handle_Analyzer,handle_Analyzer_value)==False:
                        self.errorFlag =False
                        
            else:
                #print 'ERROR:stc_result_print param error'
                msg  = 'ERROR:stc_result_print param error'
                log_print(msg)
                self.errorFlag = False
                
        else:
            #print 'ERROR:stc_result_print param error'
            msg  = 'ERROR:stc_result_print param error'
            log_print(msg)
            self.errorFlag = False
        return self.errorFlag
        
    def stc_result_print(self,p_str,port_str='AnalyzerPort'):
        if port_str.find('GeneratorPort')>-1:
            tmpstr = ' -'+ p_str
            #print 'GeneratorPort packet,',p_str,':',self.stc_get(self.hGeneratorResults,tmpstr)
            msg  = 'GeneratorPort packet,'+ p_str +':'+self.stc_get(self.hGeneratorResults,tmpstr)
            log_print(msg)
        elif port_str.find('AnalyzerPort')>-1:
            tmpstr = ' -'+ p_str
            msg  = 'AnalyzerPort packet,' + p_str +':' +self.stc_get(self.hAnalyzerResults,tmpstr)
            log_print(msg)
            #print 'AnalyzerPort packet,',p_str,':',self.stc_get(self.hAnalyzerResults,tmpstr)
        else:
            log_print( 'ERROR:stc_result_print param error')
            self.errorFlag = False
        
        return self.errorFlag
        
    
    
    
    def stc_stream_test(self,filename='E:\\Simu_server\\auto_conf\\stream_param.xls',sheetname = 'stream',waifor='0'):
        if sheetname.upper().find('MULTI_')==0:
            self.stc_testcenter_multi_test(filename,sheetname,waifor)
            return self.stc_get_resultFlag()
        elif sheetname.upper().find('LOAD_')==0:
            self.stc_loadfile(filename,sheetname)
            return True

        try:
            self.stc_create_stream(filename,sheetname)
            self.stc_traffic_stream()
            self.stc_release_testcenter()
        except Exception ,exc_str:
            self.stc_print_flag_error(exc_str)
            self.resultFlag =False
        return self.stc_get_resultFlag()
    
    
    
    
    def stc_initpare_multi(self,filename='E:\\Simu_server\\auto_conf\\stream_param.xls',sheetname = 'multi_stream'):
        self.ipv4_sel =[]
        try:
            initstream = readexcel(filename,sheetname)
            keyvalue_t = initstream.Excel_read()
            msg = '***************** excel read data *****************' 
            log_print(msg)
            msg = keyvalue_t 
            log_print(msg)
            msg = '***************** excel read data *****************' 
            
            dic = self.stc_global_keyreplay(keyvalue_t)
            if dic ==None:
                return  self.errorFlag   
            keyvalue = dic
            
            msg = '***************** excel replay read data *****************' 
            log_print(msg)
            msg = keyvalue 
            log_print(msg)
            msg = '***************** excel replay read data *****************' 
            log_print(msg)
        except Exception ,exc_str:
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            return self.errorFlag
        try:
            #TESTCENT IP RXPORT TXPORT
            self.ChassisIp = keyvalue['ChassisIp']
            self.iTxSlot = keyvalue['iTxSlot']
            self.iRxSlot = keyvalue['iRxSlot']
            self.iTxPort = keyvalue['iTxPort'].split(',')
            self.iRxPort = keyvalue['iRxPort'].split(',')
            
            tmp_list = [x for x in self.iRxPort if x not in self.iTxPort]
            self.list_port_add = []
            self.list_port_add_rx=[]
            for x in self.iTxPort:
                self.list_port_add.append(x)
            for x in tmp_list:
                self.list_port_add.append(x)
            msg = '-----  Use Testcenter ports:  ---------'
            log_print(msg)
        
            log_print(self.list_port_add)
            
            #Add an EthernetII Protocol Data Unit (PDU)
            self.srcMac = keyvalue['srcMac'].split(',')
            self.dstMac = keyvalue['dstMac'].split(',')
	    self.etherType = []
	    if keyvalue.has_key('etherType'):
                self.etherType = keyvalue['etherType'].split(',')
            #add vlan configure
            self.Vlan_pri = keyvalue['Vlan_pri'].split(',')
            self.Vlan_cfi = keyvalue['Vlan_cfi'].split(',')
            self.Vlan_id = keyvalue['Vlan_id'].split(',')
            #Use modifier to generate multiple streams
            self.ModifierMode = keyvalue['ModifierMode'].split(',')
            self.Mask = keyvalue['Mask'].split(',')
            self.StepValue = keyvalue['StepValue'].split(',')
            self.Data = keyvalue['Data'].split(',')
            self.RecycleCount = keyvalue['RecycleCount'].split(',')
            self.RepeatCount = keyvalue['RepeatCount'].split(',')
            self.DataType = keyvalue['DataType'].split(',')
            self.EnableStream = keyvalue['EnableStream'].split(',')
            self.Offset = keyvalue['Offset'].split(',')
            self.OffsetReference = keyvalue['OffsetReference'].split(',')
            self.useDefaultHost = keyvalue['useDefaultHost'].split(',')
            #Create a stream block.
            self.frameLengthMode = keyvalue['frameLengthMode'].split(',')
            self.maxFrameLength = keyvalue['maxFrameLength'].split(',')
            self.FixedFrameLength = keyvalue['FixedFrameLength'].split(',')
            self.insertSig = keyvalue['insertSig'].split(',')
            
            #Configure generator.
            self.Generator_con_type = keyvalue['Generator_con_type'].split(',')
            self.Generator_con_type_load = keyvalue['Generator_con_type_load'].split(',')
            self.DurationMode = keyvalue['DurationMode'].split(',')
            self.BurstSize = keyvalue['BurstSize'].split(',')
            self.Duration = keyvalue['Duration'].split(',')
            self.LoadMode = keyvalue['LoadMode'].split(',')
            self.FixedLoad = keyvalue['FixedLoad'].split(',')
            self.FixedLoad = keyvalue['FixedLoad'].split(',')
            self.LoadUnit = keyvalue['LoadUnit'].split(',')
            self.SchedulingMode = keyvalue['SchedulingMode'].split(',')
            #wait traffic stream time
            
            self.waittime = string.atoi(keyvalue['waittime'])
            #Set_capture param
            self.FileName = keyvalue['FileName'].split(',')
            self.Filter_config_Use = keyvalue['Filter_config_Use'].split(',')
            self.FilterOnStreamId = keyvalue['FilterOnStreamId'].split(',')
            
            self.Filter_Summary_multi= keyvalue['Filter_Summary'].split('$')
            self.Filter_FrameConfig_multi = keyvalue['Filter_FrameConfig'].split('$')
            self.Filter_srcMac= keyvalue['Filter_srcMac'].split(',')
            self.Filter_dstMac = keyvalue['Filter_dstMac'].split(',')
            self.Filter_vlanID= keyvalue['Filter_vlanID'].split(',')
            #self.Filter_Port = keyvalue['Filter_vlanID'].split(',')
           
            self.FilterStream_Result_value = keyvalue['FilterStream_Result_value'].split('$')
            
            #RESULT打印信息输出（该值为过滤规则后的数据＄1�7
            self.ParamGeneratorPort = keyvalue['ParamGeneratorPort'].split(',')
            self.ParamAnalyzerPort = keyvalue['ParamAnalyzerPort'].split(',')
            
            
            #compare_parame（比较过滤规则后的数据结果）
            self.compare_mode_multi = keyvalue['compare_mode'].split(',')
            self.compare_pass_type_multi = keyvalue['compare_pass_type'].split(',')
            self.ParamGeneratorPortvalue_multi = keyvalue['ParamGeneratorPortvalue'].split('$')
            self.ParamAnalyzerPortvalue_multi = keyvalue['ParamAnalyzerPortvalue'].split('$')
            self.ParamGeneratorPort_compare_AnalyzerPort_multi = keyvalue['ParamGeneratorPort_compare_AnalyzerPort'].split('$')
            
            self.hGeneratorResults_both = None
            self.hAnalyzerResults_both = None
            
            self.Ipv4_srcIp = []
            self.Ipv4_dstIp = []
            self.ipv4_protocol = []
            
            self.ipv4_dscp = [] 
            if keyvalue.has_key('Ipv4_sel'):
                self.ipv4_sel =keyvalue['Ipv4_sel']
            if keyvalue.has_key('Ipv4_srcIp'):
                self.Ipv4_srcIp = keyvalue['Ipv4_srcIp'].split(',')
            if keyvalue.has_key('Ipv4_dstIp'):
                self.Ipv4_dstIp = keyvalue['Ipv4_dstIp'].split(',')
            if keyvalue.has_key('Ipv4_protocol'):
                self.ipv4_protocol = keyvalue['Ipv4_protocol'].split(',')
            if keyvalue.has_key('Ipv4_dscp'):
                self.ipv4_dscp = keyvalue['Ipv4_dscp'].split(',')
            
            
                
            
        except Exception ,exc_str:
            msg = 'init param Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            return self.errorFlag       
        return
    
    
    
    def stc_CreateProject_multi(self):
        #print '##### stc_create_pro fuction #####'
        if self.errorFlag == False:
            return self.errorFlag
        strTime = time.strftime(KEY_TIME_FORMAT)
        msg = 'Creating project ...' 
        log_print(msg)
        try:
            self.hProject=self.stc_create('project')
        except Exception ,exc_str:
            msg = 'create project error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return 
    
    def stc_create_port_multi(self,oth_param='-useDefaultHost False'):
        
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Creating ports ...' 
        log_print(msg)
        self.hPort_multi =[]
        #find the port in self.iRxPort but not in  self.iTxPort
        
        try:
            for x in self.list_port_add:
                tmp_str = '//'+self.ChassisIp +'/'+x
                self.hPort_multi.append(self.stc_create('port','-under ',self.hProject,'-location ',tmp_str, oth_param)) 
                time.sleep(3)
                msg= '----self.hPort_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hPort_multi
                log_print(msg)
                msg= '----self.hPort_multi port:' + x + '  -----'
                log_print(msg)
        except Exception ,exc_str:
            msg = 'create port error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_create_physical_interface(self,oth_param='-useDefaultHost False'):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configure physical interface...'
        log_print(msg) 
        self.hPortTxCopperInterface_multi =[]
        try:
            for x in self.hPort_multi:
                self.hPortTxCopperInterface_multi.append(self.stc_create('EthernetCopper','-under ',x))
                msg= '----self.hPortTxCopperInterface_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hPortTxCopperInterface_multi
                log_print(msg)
                msg= '----self.hPort_multi port:' + x + '  -----'
                log_print(msg)
            self.stc_eval_multi()
            msg = 'Connecting ' + self.ChassisIp +' ...'
            log_print(msg)
            self.stc_eval_multi()
            msg = 'Set up port mappings...'
            log_print(msg)
            if len(self.hPort_multi)>0:
                tmp_str = '"'
                for x in self.hPort_multi:
                    tmp_str = tmp_str + ' ' + x
                tmp_str = tmp_str + ' "'
                self.stc_perform('attachPorts -portlist' , tmp_str)
            else:
                self.errorFlag = False
                return self.errorFlag 
            
        except Exception ,exc_str:
            msg = 'create physical_interface port error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    
        
    def stc_create_port_generator_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'get generator interface...'
        log_print(msg)
        self.hGenerator_multi = []  
        try:
            if len(self.hPort_multi)>0:
                for x in self.hPort_multi:
                    self.hGenerator_multi.append(self.stc_get( x,'-children-Generator'))
            else:
                self.errorFlag = False
                return self.errorFlag
        except Exception ,exc_str:
            msg = 'generator get  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_create_port_Analyzer_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'get Analyzer interface...'
        log_print(msg)
        self.hAnalyzer_multi = []
        try:
            if len(self.hPort_multi)>0:
                print 'len(self.hPort_multi)',len(self.hPort_multi)
                for x in self.hPort_multi:
                    self.hAnalyzer_multi.append(self.stc_get( x,'-children-Analyzer'))
                    #time.sleep(3)
            else:
                self.errorFlag = False
                return self.errorFlag
        except Exception ,exc_str:
            msg = 'Analyzer get  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_create_ipv4diffserv_multi(self):
        log_print('*********** create_ipv4diffserv fuction ***********')
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configuring ipv4diffserv  block ...'
        log_print(msg) 
        self.diffserv_multi = []
        self.tos_multi = []
        tmp_str = ''
        
        try:
            for x in range(len(self.ipv4_multi)):
                
                if self.ipv4_multi[x]=='':
                    self.diffserv_multi.append('')
                else:
                    tmp  = ' tosdiffserv -under ' + self.ipv4_multi[x] 
                    self.diffserv_multi.append(self.stc_create(tmp))
                
                log_print( '**********#######diffserv_multi#######**********')
                log_print(self.diffserv_multi)
                log_print( '*********#######diffserv_multi#######***********')
                
        except Exception ,exc_str:
            msg = 'create ipv4tosdiffserv  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        try:
            for x in range(len(self.diffserv_multi)):
                tmp_dscp = ''
                tmp_dscp_high = '0'
                tmp_dscp_low = '0'
                if self.diffserv_multi[x]=='':
                    self.tos_multi.append('')
                else:
                    tmp =  ' diffServ -under ' +  self.diffserv_multi[x] + ' '
                    self.tos_multi.append(self.stc_create(tmp))
                log_print( '*********#######tos#######***********')
                log_print(self.tos_multi)
                log_print( '*********#######tos#######***********')
                if len(self.ipv4_dscp) ==0 :
                    pass
                elif x>len(self.ipv4_dscp )-1:
                    tmp_dscp = self.ipv4_dscp[-1]
                else:
                    tmp_dscp = self.ipv4_dscp[x]
                if tmp_dscp!='NULL':
                    print 'tmp_dscp:',tmp_dscp
                    tmp_bin2 = DectoBin2(tmp_dscp)
                    print 'tmp_bin2:',tmp_bin2
                    if len(tmp_bin2)>3:
                        t_b = tmp_bin2[-3:]
                        tmp_dscp_low = Bin2toDec(tmp_bin2[-3:])
                        t_b = tmp_bin2[:-3]
                        tmp_dscp_high = Bin2toDec(tmp_bin2[:-3])
                    else:
                        t_b = tmp_bin2
                        tmp_dscp_low = Bin2toDec(tmp_bin2)
                    tmp = ' '     + self.tos_multi[x] + ' -dscpLow ' + tmp_dscp_low + ' -dscpHigh ' + tmp_dscp_high
                    self.stc_config(tmp)      
        except Exception ,exc_str:
            msg = 'create diffserv  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
        
    def stc_create_ipv4_multi(self):
        log_print( '*********** create_ipv4 fuction ***********')
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configuring ip  block ...'
        log_print(msg)
        if len(self.ipv4_sel)==0:
            return
        self.ipv4_multi = [] 
       
        try:
            for x in range(len(self.hPort_multi)):
                tmp_ipsel =''
                tmp_ipdst=''
                tmp_ipsrc=''
                tmp_ippro=''
                tmp_ipdscp=''
                if x>len(self.ipv4_sel)-1:
                    tmp_ipsel =self.ipv4_sel[-1]
                else:
                    tmp_ipsel =self.ipv4_sel[x]
                if tmp_ipsel =='False':
                    self.ipv4_multi.append('')
                else:
                    tmp_str = ' ipv4:IPv4 -under  '
                    #print 'self.hStreamBlock_multi:',self.hStreamBlock_multi[x],' x:',x
                    #print 'self.Ipv4_srcIp:',self.Ipv4_srcIp
                    #print 'self.Ipv4_dstIp:',self.Ipv4_dstIp
                    #print 'self.ipv4_dscp:',self.ipv4_dscp
                    #print 'self.ipv4_protocol:',self.ipv4_protocol
                    #print 'self.ipv4_sel:',self.ipv4_sel
                    tmp_str = tmp_str + self.hStreamBlock_multi[x] + ' -name sb1_ip '
                    if len(self.Ipv4_srcIp) ==0:
                        tmp_ipsrc='NULL'
                    elif x>len(self.Ipv4_srcIp)-1:
                        tmp_ipsrc=self.Ipv4_srcIp[-1]
                    else:
                        tmp_ipsrc=self.Ipv4_srcIp[x]
                    if tmp_ipsrc!='NULL':
                        tmp_str = tmp_str + ' -sourceAddr ' + tmp_ipsrc + ' '
                    if len(self.Ipv4_dstIp) ==0:
                        tmp_ipdst='NULL'
                    elif x>len(self.Ipv4_dstIp)-1:
                        tmp_ipdst = self.Ipv4_dstIp[-1]
                    else:
                        tmp_ipdst = self.Ipv4_dstIp[x]
                    if tmp_ipdst!='NULL':
                        tmp_str = tmp_str + ' -destAddr ' + tmp_ipdst + ' '
                    if len(self.ipv4_protocol) ==0:
                        tmp_ippro='NULL'
                    elif x>len(self.ipv4_protocol)-1:
                        tmp_ippro = self.ipv4_protocol[-1]
                    else:
                        tmp_ippro = self.ipv4_protocol[x]
                    if tmp_ippro!='NULL':
                        tmp_str = tmp_str + ' -protocol ' + tmp_ippro + ' '
                    if tmp_str=='':
                        self.ipv4_multi.append('')
                    else:
                        self.ipv4_multi.append(self.stc_create(tmp_str))
                    
        except Exception ,exc_str:
            msg = 'create ipv4 multi  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
            
    def stc_create_stream_block_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configuring stream block ...'
        log_print(msg)
        self.hStreamBlock_multi = []
        try:
            for x in range(len(self.hPort_multi)):
                tmp_str = '  -frameConfig ""  -insertSig '
                if x>=len(self.insertSig):
                    tmp_str = tmp_str +' ' + self.insertSig[-1]
                else:
                    tmp_str = tmp_str +' ' +self.insertSig[x]
                if x>=len(self.frameLengthMode):
                    tmp_str = tmp_str +' -frameLengthMode ' + self.frameLengthMode[-1]
                else:
                    tmp_str = tmp_str +' -frameLengthMode ' +self.frameLengthMode[x]
                if x>=len(self.maxFrameLength):
                    tmp_str = tmp_str +' -maxFrameLength ' + self.maxFrameLength[-1]
                else:
                    tmp_str = tmp_str +' -maxFrameLength ' +self.maxFrameLength[x]
                if x>=len(self.FixedFrameLength):
                    tmp_str = tmp_str +' -FixedFrameLength ' + self.FixedFrameLength[-1]
                else:
                    tmp_str = tmp_str +' -FixedFrameLength ' +self.FixedFrameLength[x]
                self.hStreamBlock_multi.append( self.stc_create('streamBlock -under ',self.hPort_multi[x],tmp_str))
               
                #self.stc_apply()
        except Exception ,exc_str:
            msg = 'create stream block_multi  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        print 'Configuring stream block ... :self.hStreamBlock_multi:',self.hStreamBlock_multi
        return self.errorFlag
        

    def stc_create_ethernet_head_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Adding EthernetII headers... ...'
        log_print(msg)
        self.hEthernet_multi = []
        try:
            for x in range(len(self.hPort_multi)):
                tmp_str = 'ethernet:EthernetII -under' + ' ' + self.hStreamBlock_multi[x] + ' ' + '-name sb1_eth'
                if x >= len(self.srcMac):
                    tmp_str = tmp_str + '  -srcMac ' + self.srcMac[-1]
                else:
                    tmp_str = tmp_str + '  -srcMac ' + self.srcMac[x]
                if x >=len(self.dstMac):
                    tmp_str = tmp_str + '  -dstMac ' + self.dstMac[-1]
                else:
                    tmp_str = tmp_str + '  -dstMac ' + self.dstMac[x]
                
                if len(self.etherType)>0:
                    if x>=len(self.etherType):
                        if self.etherType[-1].upper()!= 'NULL':
                            tmp_str = tmp_str + '  -etherType ' + self.etherType[-1]
                    else:
                        if self.etherType[x].upper()!= 'NULL':
                            tmp_str = tmp_str + '  -etherType ' + self.etherType[x]
                        
                self.hEthernet_multi.append(self.stc_create(tmp_str))
    
        except Exception ,exc_str:
            msg = 'Adding EthernetII headers  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_create_vlan_multi_multitag(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Adding vlan... ...'
        log_print(msg)
        self.hVlanContainer_multi = [ ]
        try:
            for x in range(len(self.hPort_multi)):
                tmp_str = ''
                tmp_vlan = ''
                if x >= len(self.Vlan_id):
                    tmp_vlan = self.Vlan_id[-1]
                else:
                    tmp_vlan = self.Vlan_id[x]
                if tmp_vlan.find('NULL')<0:
                    self.hVlanContainer_multi.append(self.stc_create( 'vlans -under ',self.hEthernet_multi[x]))
                    for y in  tmp_vlan.split('/'):
                        tmp_str  = '  -id ' +  y
                        if x >=len(self.Vlan_pri):
                            tmp_str = tmp_str + '  -pri ' + self.Vlan_pri[-1]
                        else:
                            tmp_str = tmp_str + '  -pri ' + self.Vlan_pri[x]
                        if x >=len(self.Vlan_cfi):
                            tmp_str = tmp_str + '  -cfi ' + self.Vlan_cfi[-1]
                        else:
                            tmp_str = tmp_str + '  -cfi ' + self.Vlan_cfi[x] 
                        self.stc_create('Vlan -under ',self.hVlanContainer_multi[x],tmp_str)
                else:
                    self.hVlanContainer_multi.append('NULL')
                        
                        
        except Exception ,exc_str:
            msg = 'Adding  vlan...  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    
    def stc_create_vlan_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Adding vlan... ...'
        log_print(msg)
        self.hVlanContainer_multi = [ ]
        try:
            for x in range(len(self.hPort_multi)):
                tmp_str = ''
                if x >= len(self.Vlan_id):
                    tmp_str = '  -id ' + self.Vlan_id[-1]
                else:
                    tmp_str = '  -id ' + self.Vlan_id[x]
                
                if tmp_str.find('NULL')<0:
                    self.hVlanContainer_multi.append(self.stc_create( 'vlans -under ',self.hEthernet_multi[x]))
                    if x >=len(self.Vlan_pri):
                        tmp_str = tmp_str + '  -pri ' + self.Vlan_pri[-1]
                    else:
                        tmp_str = tmp_str + '  -pri ' + self.Vlan_pri[x]
                    if x >=len(self.Vlan_cfi):
                        tmp_str = tmp_str + '  -cfi ' + self.Vlan_cfi[-1]
                    else:
                        tmp_str = tmp_str + '  -cfi ' + self.Vlan_cfi[x] 
                    self.stc_create('Vlan -under ',self.hVlanContainer_multi[x],tmp_str)
                else:
                    self.hVlanContainer_multi.append('NULL')
        except Exception ,exc_str:
            msg = 'Adding  vlan...  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
                      
    def stc_filter_config_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Adding filter...'
        log_print(msg)
        tmp_str_port = ' '
        self.hAnalyzerFrameConfigFilter_multi = [] 
        try:
            print 'self.hAnalyzer_multi',len(self.hAnalyzer_multi)
            for x in range(len(self.hPort_multi)):
                msg = 'Configuring analyzer frame config filter ...'
                log_print(msg)
                tmp_str = 'AnalyzerFrameConfigFilter -under '
                tmp_str_other ='-FrameConfig ""'
                print '******** add filter self.hAnalyzer_multi[x]:',self.hAnalyzer_multi[x]
                self.hAnalyzerFrameConfigFilter_multi.append(self.stc_create(tmp_str,self.hAnalyzer_multi[x],tmp_str_other))
                #print 'self.hAnalyzer_multi:',self.hAnalyzerFrameConfigFilter_multi
                print '******** add filter  hAnalyzerFrameConfigFilter_multi:',self.hAnalyzerFrameConfigFilter_multi
                if x >= len(self.Filter_config_Use):
                    tmp_str = self.Filter_config_Use[-1]
                else:
                    tmp_str = self.Filter_config_Use[x]
                if tmp_str=='2':
                    self.stc_filter_temp_use2_multi()
                
        except Exception ,exc_str:
            msg = 'stc_filter_config_multi error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_filter_GetStream(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'stc_filter_GetStream...'
        log_print(msg)
        self.hfiltedresult_multi=[]
        try:
            for x in self.hAnalyzer_multi:
                print 'self.hAnalyzer_multi:',x
                print '************hfiltedresult_multi************'
                self.hfiltedresult_multi.append(self.stc_get(x,'-children-FilteredStreamResults'))
                print '************hfiltedresult_multi************'
                print 'self.hfiltedresult_multi:',self.hfiltedresult_multi
        except Exception ,exc_str:
            msg = 'stc_filter_GetStream error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
            
        
    def stc_filter_value_compile(self):
        
        msg = 'stc_filter_value_compile...'
        log_print(msg)
        tmp_FilterStream_Result = self.FilterStream_Result_t.split(':')
        rxPort = tmp_FilterStream_Result[0]
        tmp_num = self.stc_get_rx_hport(rxPort)
        print '******** hfiltedresult_multi*******',self.hfiltedresult_multi
        print 'tmp_num:',tmp_num
        tmp_value = tmp_FilterStream_Result[1].split('&&')    #['SigFrameCount>0' ,  'GeneratorSigFrameCount>0']
        print 'tmp_value:', tmp_value
        print 'self.hfiltedresult_multi:',self.hfiltedresult_multi
        for x in tmp_value:
            tmp = re.findall(str_sign , x)  #['>']
            value = x.split(tmp[0])     #['sigframecount', '23456']
            tmp_str = '-' + value[0]
            get_value='0'
            try:
                get_value = self.stc_get(self.hfiltedresult_multi[tmp_num],tmp_str)
                print 'get_value:', get_value,'rxPort:',rxPort,'value:',value
            except Exception ,exc_str:
                msg = 'not get value' + rxPort
                log_print(msg)
                dic_1 ={'==':1,'>=':1,'<=':1}
                if string.atoi(value[1])==0:
                    if dic_1.has_key(tmp[0])==True:
                        return True
                pass
            if tmp[0] == '==':
                if (string.atoi(get_value) == string.atoi(value[1])):
                    self.errorFlag = True
                else:
                    self.errorFlag = False
            elif tmp[0] == '>':
                if (string.atoi(get_value) > string.atoi(value[1])):
                    self.errorFlag = True
                else:
                    self.errorFlag = False
            elif tmp[0] == '<':
                if (string.atoi(get_value) < string.atoi(value[1])):
                    self.errorFlag = True
                else:
                    self.errorFlag = False
            elif tmp[0] == '>=':
                if (string.atoi(get_value) >= string.atoi(value[1])):
                    self.errorFlag = True
                else:
                    self.errorFlag = False
            elif tmp[0] == '<=':
                if (string.atoi(get_value) <= string.atoi(value[1])):
                    self.errorFlag = True
                else:
                    self.errorFlag = False
            if self.errorFlag ==True:
                msg  = '*************** this stc_filter_value_compile pass,OK ***************'
                log_print(msg)
                msg = 'get ' + self.hfiltedresult_multi[tmp_num] + ' result value:' + get_value +' Data from Port:' + rxPort
                log_print(msg)
                msg  = '*************** this stc_filter_value_compile pass,OK ***************'
                log_print(msg)
            else:
                msg  = '*************** this stc_filter_value_compile pass,NG ***************'
                log_print(msg)
                msg = 'get ' + self.hfiltedresult_multi[tmp_num] + ' result value:' + get_value +' Data from Port:' + rxPort
                log_print(msg)
                msg  = '*************** this stc_filter_value_compile pass,NG ***************'
                log_print(msg)
        return self.errorFlag
        
    '''        
            print 'comp_type :',comp_type,' rxport:',rxPort
            tmp_num = self.stc_get_rx_hport(rxPort)
            tmp_str = '-'+param_cmd
            get_value='0'
            print '******** hfiltedresult_multi*******',self.hfiltedresult_multi
            print 'tmp_num:',tmp_num
            try:
                get_value = self.stc_get(self.hfiltedresult_multi[tmp_num],tmp_str)
            except Exception ,exc_str:
                msg = 'not get value' + rxPort
                log_print(msg)
                pass
            #print 'except continue'
                
            #print 'get_value:',get_value
            if comp_type=='0':
                value = string.atoi(get_value)
                if(value ==string.atoi(comp_type)):
                    self.errorFlag = True
                else:
                    self.errorFlag =False
            
            elif comp_type=='1':
                value = string.atoi(get_value)
                if(value > string.atoi(comp_type)):
                    self.errorFlag =True
                else:
                    self.errorFlag =False
            elif comp_type=='2':
                value = string.atoi(get_value)
                if(value <string.atoi(comp_type)):
                    self.errorFlag =True
                else:
                    self.errorFlag =False
            elif comp_type=='3':
                value = string.atoi(get_value)
                if(value >=string.atoi(comp_type)):
                    self.errorFlag =True
                else:
                    self.errorFlag =False
            elif comp_type=='4':
                value = string.atoi(get_value)
                if(value >=string.atoi(comp_type)):
                    self.errorFlag =True
                else:
                    self.errorFlag =False
            elif comp_type=='5':
                value = string.atoi(get_value)
                if(value <=string.atoi(comp_type)):
                    self.errorFlag =True
                else:
                    self.errorFlag =False
            if self.errorFlag ==True:
                msg  = '*************** this stc_filter_value_compile pass,OK ***************'
                log_print(msg)
                msg = 'get ' + param_cmd + ' result value:' + get_value +' Data from Port:' + rxPort
                log_print(msg)
                msg  = '*************** this stc_filter_value_compile pass,OK ***************'
                log_print(msg)
            else:
                msg  = '*************** this stc_filter_value_compile pass,NG ***************'
                log_print(msg)
                msg = 'get ' + param_cmd + ' result value:' + get_value +' Data from Port:' + rxPort
                log_print(msg)
                msg  = '*************** this stc_filter_value_compile pass,NG ***************'
                log_print(msg)
            return self.errorFlag 
    '''        
    def stc_filter_temp_use2_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg='stc_filter_temp_use2_multi create'
        log_print(msg)
        #hAnalyzerFrameConfigFilter_multi = []
        try:
            print 'hAnalyzerFrameConfigFilter_multi ',self.hAnalyzerFrameConfigFilter_multi
            for x in range(len(self.hAnalyzerFrameConfigFilter_multi)):
                if x>= len(self.Filter_FrameConfig_multi):
                    self.Filter_FrameConfig = '{ ' + self.Filter_FrameConfig_multi[-1] + ' }'
                else:
                    self.Filter_FrameConfig = '{ ' + self.Filter_FrameConfig_multi[x] + ' }'
                if x>=len(self.Filter_Summary_multi):
                    self.Filter_Summary = '{ ' + self.Filter_Summary_multi[-1] + ' }'
                else:
                    self.Filter_Summary = '{ ' + self.Filter_Summary_multi[x] + ' }'
                    
                tmpstr =''
                if self.Filter_Summary.find('NULL')>-1:
                    tmpstr = ' -FrameConfig ' + self.Filter_FrameConfig 
                else:
                    tmpstr = ' -FrameConfig ' + self.Filter_FrameConfig +' -Summary ' + self.Filter_Summary
                #self.stc_config(self.hAnalyzerFrameConfigFilter_multi[x], tmpstr)
                print 'self.hAnalyzerFrameConfigFilter_multi[x]',self.hAnalyzerFrameConfigFilter_multi[x]
                self.stc_config(self.hAnalyzerFrameConfigFilter_multi[x], tmpstr)
                self.stc_apply()
                
        except Exception ,exc_str:
            msg = 'stc_filter_temp_use2_multi error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
        
    def stc_modify_stream_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Creating Modifier on Stream Block ...'
        log_print(msg)
        self.hRangeModifier_multi = []
        self.lstStreamBlockInfo_multi = [] 
        try:
            for x in range(len(self.hPort_multi)):
                tmp_str = 'RangeModifier -under ' + self.hStreamBlock_multi[x] + ' -ModifierMode '
                if x >=len(self.ModifierMode):
                    tmp_str =tmp_str +' '+self.ModifierMode[-1]
                else:
                    tmp_str =tmp_str +' '+self.ModifierMode[x]
                if x >=len(self.Mask):
                    tmp_str =tmp_str +' -Mask "'+self.Mask[-1]+'"'
                else:
                    tmp_str =tmp_str +' -Mask "'+self.Mask[x]+'"'
                if x >=len(self.StepValue):
                    tmp_str =tmp_str +' -StepValue "'+self.StepValue[-1]+'"'
                else:
                    tmp_str =tmp_str +' -StepValue "'+self.StepValue[x]+'"'
                if x >=len(self.Data):
                    tmp_str =tmp_str +' -Data "'+self.Data[-1]+'"'
                else:
                    tmp_str =tmp_str +' -Data "'+self.Data[x]+'"'
                if x >=len(self.RecycleCount):
                    tmp_str =tmp_str +' -RecycleCount '+self.RecycleCount[-1]
                else:
                    tmp_str =tmp_str +' -RecycleCount '+self.RecycleCount[x]
                if x >=len(self.DataType):
                    tmp_str =tmp_str +' -DataType '+self.DataType[-1]
                else:
                    tmp_str =tmp_str +' -DataType '+self.DataType[x]
                if x >=len(self.EnableStream):
                    tmp_str =tmp_str +' -EnableStream '+self.EnableStream[-1]
                else:
                    tmp_str =tmp_str +' -EnableStream '+self.EnableStream[x]
                if x >=len(self.Offset):
                    tmp_str =tmp_str +' -Offset '+self.Offset[-1]
                else:
                    tmp_str =tmp_str +' -Offset '+self.Offset[x]
                if x >=len(self.OffsetReference):
                    tmp_str =tmp_str +' -OffsetReference "'+self.OffsetReference[-1] +'"'
                else:
                    tmp_str =tmp_str +' -OffsetReference "'+self.OffsetReference[x] +'"'
                
                print '####################'
                self.hRangeModifier_multi.append(self.stc_create(tmp_str))
                print '####################'
                #self.stc_apply()
                
                msg = '\n\nStreamBlock information ' + self.iTxPort[x]+ '.........'
                log_print(msg)
                print 'self.hStreamBlock_multi',self.hStreamBlock_multi[x]
                self.lstStreamBlockInfo_multi.append(self.stc_perform('StreamBlockGetInfo -StreamBlock',self.hStreamBlock_multi[x]))
                log_print(self.lstStreamBlockInfo_multi[x])
        
        except Exception ,exc_str:
            msg = 'Creating Modifier on Stream Block error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        print 'Creating Modifier on Stream Block lstStreamBlockInfo_multi:',self.lstStreamBlockInfo_multi
        return self.errorFlag
                
    def stc_Config_Generator_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configuring Generator...'
        log_print(msg)
        self.hGeneratorConfig_multi = []
        try:
            for x in range(len(self.iTxPort)):
                
                self.hGeneratorConfig_multi.append(self.stc_get(self.hGenerator_multi[x],' -children-GeneratorConfig '))
                tmp_str_other = ' '
                if x>=len(self.Generator_con_type):
                    tmp_str_other=self.Generator_con_type[-1]
                else:
                    tmp_str_other=self.Generator_con_type[x]
                if tmp_str_other.find('2')>-1:
                    if x>= len(self.Generator_con_type_load):
                        tmp_str = self.Generator_con_type_load[-1]
                    else:
                        tmp_str = self.Generator_con_type_load[x]
                else:
                    
                    print '11111111111133333333333331111111111111'
                    if x>= len(self.DurationMode ):
                        tmp_str = ' -DurationMode ' + self.DurationMode[-1]
                    else:
                        tmp_str =  ' -DurationMode ' + self.DurationMode[x]
                    
                    if x>= len(self.BurstSize ):
                        tmp_str = tmp_str + ' -BurstSize ' + self.BurstSize[-1]
                    else:
                        tmp_str =  tmp_str +' -BurstSize ' + self.BurstSize[x]
                    if x>= len(self.Duration ):
                        tmp_str =  tmp_str +' -Duration ' + self.Duration[-1]
                    else:
                        tmp_str =  tmp_str +' -Duration ' + self.Duration[x]
                    if x>= len(self.LoadMode ):
                        tmp_str =  tmp_str +' -LoadMode ' + self.LoadMode[-1]
                    else:
                        tmp_str =  tmp_str +' -LoadMode ' + self.LoadMode[x]
                    if x>= len(self.FixedLoad ):
                        tmp_str =  tmp_str +' -FixedLoad ' + self.FixedLoad[-1]
                    else:
                        tmp_str =  tmp_str +' -FixedLoad ' + self.FixedLoad[x]
                    if x>= len(self.LoadUnit ):
                        tmp_str =  tmp_str +' -LoadUnit ' + self.LoadUnit[-1]
                    else:
                        tmp_str =  tmp_str +' -LoadUnit ' + self.LoadUnit[x]
                    if x>= len(self.SchedulingMode ):
                        tmp_str =  tmp_str +' -SchedulingMode ' + self.SchedulingMode[-1]
                    else:
                        tmp_str =  tmp_str +' -SchedulingMode ' + self.SchedulingMode[x]
                self.stc_config(self.hGeneratorConfig_multi[x],tmp_str)
        except Exception ,exc_str:
            msg = 'Configuring Generator error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag      
                
        
    def stc_get_rx_hport(self,x):
        tmp = 0
        for i in self.list_port_add:
            if x.find(i)>-1:
                break
            else:
                tmp = tmp +1 
        return tmp
                
    def stc_Realtime_Result_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Subscribe to realtime results...'
        log_print(msg)
        self.hResultDataSetFiltered_multi=[]
        self.hResultsDataSetSend_multi = []
        self.hResultsDataSetReceived_multi = []
        try:
            for x in range(len(self.hPort_multi)):
                tmpstr1 =' -configType Generator -resultParent '
                tmpstr2 =' -resultType GeneratorPortResults -filenamePrefix "Generators" -interval 1'
                self.hResultsDataSetSend_multi.append(self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPort_multi[x],tmpstr2))
            for x in range(len(self.hPort_multi)):
                #tmp_port = self.iRxPort[x]
                '''
                if x >= len(self.iRxPort):
                    tmp_port = self.iRxPort[-1]
                else:
                    tmp_port = self.iRxPort[x]
                '''
                #tmp_num = self.stc_get_rx_hport(tmp_port)
                tmpstr1 =  ' -configType Analyzer -resultParent '
                tmpstr2 = ' -resultType FilteredStreamResults -filenamePrefix "FilteredStreamResults" -interval 1'
                #self.hResultDataSetFiltered_multi.append(self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPort_multi[tmp_num],tmpstr2))
                self.hResultDataSetFiltered_multi.append(self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPort_multi[x],tmpstr2))
                
                tmpstr1 = '-ConfigType Analyzer -resultParent '
                tmpstr2 = '-resulttype AnalyzerPortResults -filenameprefix "Analyzer_Port_Results" -interval 1'
                #self.hResultsDataSetReceived_multi.append(self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPort_multi[tmp_num],tmpstr2))
                self.hResultsDataSetReceived_multi.append(self.stc_subscribe(' -Parent ',self.hProject,tmpstr1,self.hPort_multi[x],tmpstr2))
                
                #self.stc_apply()
        except Exception ,exc_str:
            msg = 'Subscribe to realtime results error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag   
                
                
    def  stc_Configuring_Analyzer_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Configuring Analyzer...'
        log_print(msg)
        self.hAnalyzerConfig_multi = []
        try:
            for x in range(len(self.list_port_add)):
                #tmp_port = self.iRxPort[x]
                #tmp_num = self.stc_get_rx_hport(tmp_port)
                tmp_str = '-children-AnalyzerConfig'
                #self.hAnalyzerConfig_multi.append(self.stc_get(self.hAnalyzer_multi[tmp_num],tmp_str))
                self.hAnalyzerConfig_multi.append(self.stc_get(self.hAnalyzer_multi[x],tmp_str))
                msg= '----self.hAnalyzerConfig_multi port:' + self.list_port_add[x] + '  -----'
                log_print(msg)
                msg = self.hAnalyzerConfig_multi
                log_print(msg)
                msg= '----self.hAnalyzerConfig_multi port:' + self.list_port_add[x] + '  -----'
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Configuring Analyzer  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag    
    
    def  stc_Configure_Capture_multi(self):
        
        msg = 'Configure Capture...'
        log_print(msg)
        self.hCapture_multi = []
        try:
            for x in range(len(self.list_port_add)):
                #tmp_port = self.iRxPort[x]
                #tmp_num = self.stc_get_rx_hport(tmp_port)
                tmp_str ='-children-capture'
                #self.hCapture_multi.append(self.stc_get(self.hPort_multi[tmp_num],tmp_str))
                self.hCapture_multi.append(self.stc_get(self.hPort_multi[x],tmp_str))
                
                msg= '----self.hCapture_multi port:' + self.list_port_add[x] + '  -----'
                log_print(msg)
                msg = self.hCapture_multi
                log_print(msg)
                msg= '----self.hCapture_multi port:' + self.list_port_add[x] + '  -----'
                log_print(msg)
                
                tmp_str = '-mode REGULAR_MODE -srcMode TX_RX_MODE'
                self.stc_config(self.hCapture_multi[x],tmp_str)
                tmp_str = 'CaptureStart -captureProxyId'
                self.stc_perform(tmp_str,self.hCapture_multi[x])
        except Exception ,exc_str:
            msg = 'Configure Capture  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        try:
            msg = '\nSave configuration as an XML file.'
            log_print(msg)
            tmp_str = 'SaveAsXml'
            self.stc_perform(tmp_str)
        except Exception ,exc_str:
            msg = 'SaveAsXml  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        return self.errorFlag
    
    def stc_traffic_stream_multi_waitfor(self):
        msg = '##### traffic_stream fuction #####'
        log_print(msg)
        if self.errorFlag == False:
            return self.errorFlag
        #print "Start Analyzer"
        self.hGeneratorResults_multi=[]
        self.hAnalyzerResults_multi = []
        try:
            msg = 'Start Analyzer'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str = 'AnalyzerStart -AnalyzerList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                msg = 'Current analyzer state' + self.stc_get(x,tmp_str)
                log_print(msg)
            msg = 'Start Generator'
            log_print(msg)
            for x in self.hGenerator_multi:
                tmp_str = 'GeneratorStart -GeneratorList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                #print 'Current generator state ',self.stc_get(self.hGenerator,tmp_str)
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Start Analyzer or  Start Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        '''
        msg = 'wait '+ str(self.waittime)+' seconds'
        log_print(msg)
        time.sleep(self.waittime)
        '''
        try:
            for x in self.hAnalyzer_multi:
                msg = 'Current analyzer state '+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGenerator_multi:
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Current Analyzer state or  Current Generator state error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        try:
            msg = 'stop Generator'
            log_print(msg)
            tmp_num1 =0
            tmp_port_str =''
            for x in  self.hGenerator_multi:
                if tmp_num1==0:
                    tmp_port_str ='" '+ tmp_port_str + ' ' + x
                else:
                    tmp_port_str =tmp_port_str + ' ' + x 
                tmp_num1 = tmp_num1 + 1 
            tmp_port_str = tmp_port_str +  ' ' + '"'
            tmp_str ='GeneratorWaitForStop -GeneratorList'
            self.stc_perform(tmp_str,tmp_port_str)
            msg = 'Stop the analyzer.'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str ='AnalyzerStop -AnalyzerList'
                self.stc_perform(tmp_str,x)
        except Exception ,exc_str:
            msg = 'Stop Analyzer or  Stop Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        try:
            for x in self.hGenerator_multi:
                tmp_str =' -children-GeneratorPortResults'
                self.hGeneratorResults_multi.append( self.stc_get( x,tmp_str))
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hGeneratorResults_multi
                log_print(msg)
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
            for x in self.hAnalyzer_multi:
                tmp_str = '-children-AnalyzerPortResults'
                self.hAnalyzerResults_multi.append(self.stc_get(x,tmp_str))
                msg= '----self.hAnalyzerResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hAnalyzerResults_multi
                log_print(msg)
                msg= '----self.hStreamBlock_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
        except Exception ,exc_str:
            msg = ' Analyzer port result or  Generator port result error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
        msg = 'wait 10S AnalyzerResult'
        log_print(msg)
        time.sleep(10)
        
        try:
            for x in self.hAnalyzerResults_multi:
                tmp_str = '-sigFrameCount'
                #print '\tSignature frames:',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tSignature frames:' + self.stc_get(x,tmp_str)
                log_print(msg)
                tmp_str = '-totalFrameCount'
                #print '\tTotal frames',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tTotal frames'+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGeneratorResults_multi:
                tmpstr = ' -GeneratorFrameCount'
                #print 'Send packets:', self.stc_get(self.hGeneratorResults,tmpstr)
                msg = 'Send packets:'+ self.stc_get(x,tmpstr)
                log_print(msg)
        
        except Exception ,exc_str:
            msg = ' get port frames error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
    def stc_traffic_stream_multi(self):
        msg = '##### traffic_stream fuction #####'
        log_print(msg)
        if self.errorFlag == False:
            return self.errorFlag
        #print "Start Analyzer"
        self.hGeneratorResults_multi=[]
        self.hAnalyzerResults_multi = []
        try:
            msg = 'Start Analyzer'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str = 'AnalyzerStart -AnalyzerList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                msg = 'Current analyzer state' + self.stc_get(x,tmp_str)
                log_print(msg)
            msg = 'Start Generator'
            log_print(msg)
            for x in self.hGenerator_multi:
                tmp_str = 'GeneratorStart -GeneratorList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                #print 'Current generator state ',self.stc_get(self.hGenerator,tmp_str)
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Start Analyzer or  Start Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        msg = 'wait '+ str(self.waittime)+' seconds'
        log_print(msg)
        time.sleep(self.waittime)
        
        try:
            for x in self.hAnalyzer_multi:
                msg = 'Current analyzer state '+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGenerator_multi:
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Current Analyzer state or  Current Generator state error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        try:
            msg = 'stop Generator'
            log_print(msg)
            for x in  self.hGenerator_multi:
                tmp_str ='GeneratorStop -GeneratorList'
                self.stc_perform(tmp_str,x)
            msg = 'Stop the analyzer.'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str ='AnalyzerStop -AnalyzerList'
                self.stc_perform(tmp_str,x)
        except Exception ,exc_str:
            msg = 'Stop Analyzer or  Stop Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        try:
            for x in self.hGenerator_multi:
                tmp_str =' -children-GeneratorPortResults'
                self.hGeneratorResults_multi.append( self.stc_get( x,tmp_str))
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hGeneratorResults_multi
                log_print(msg)
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
            for x in self.hAnalyzer_multi:
                tmp_str = '-children-AnalyzerPortResults'
                self.hAnalyzerResults_multi.append(self.stc_get(x,tmp_str))
                msg= '----self.hAnalyzerResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hAnalyzerResults_multi
                log_print(msg)
                msg= '----self.hStreamBlock_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
        except Exception ,exc_str:
            msg = ' Analyzer port result or  Generator port result error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
        msg = 'wait 20S AnalyzerResult'
        log_print(msg)
        time.sleep(20)
        
        try:
            for x in self.hAnalyzerResults_multi:
                tmp_str = '-sigFrameCount'
                #print '\tSignature frames:',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tSignature frames:' + self.stc_get(x,tmp_str)
                log_print(msg)
                tmp_str = '-totalFrameCount'
                #print '\tTotal frames',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tTotal frames'+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGeneratorResults_multi:
                tmpstr = ' -GeneratorFrameCount'
                #print 'Send packets:', self.stc_get(self.hGeneratorResults,tmpstr)
                msg = 'Send packets:'+ self.stc_get(x,tmpstr)
                log_print(msg)
        
        except Exception ,exc_str:
            msg = ' get port frames error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        
    def stc_result_print_multi(self,p_str,handle,port_str='AnalyzerPort'):
        
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'stc result print... '
        print 'handle:',handle
        log_print(msg)
        
        try:
            tmp_list = p_str.split('/')
            if port_str.find('GeneratorPort')>-1:
                for x in tmp_list:
                    tmpstr = ' -'+x.strip()
                    tmp_port_print =self.stc_get_datafromstr(handle)
                    msg  = 'GeneratorPort packet,handle:'+ handle+' -'+x +':'+self.stc_get(handle,tmpstr)  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
                    log_print(msg)
            elif port_str.find('AnalyzerPort')>-1:
                for x in tmp_list:
                    tmpstr = ' -'+x.strip()
                    tmp_port_print =self.stc_get_datafromstr(handle)
                    msg  = 'AnalyzerPort packet,'+ handle+'-'+x +':'+self.stc_get(handle,tmpstr)  +' Data from Port:' + self.list_port_add[string.atoi(tmp_port_print)-1]
                    log_print(msg)
            else:
                log_print( 'ERROR:stc_result_print param error')
                self.errorFlag = False
        except Exception ,exc_str:
            msg = ' stc result_print_multi error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
    
    def stc_stop_Captured_frames_multi(self):
        
        msg = 'Retrieving Captured frames...'
        log_print(msg)
        try:
            if ENABLE_CAPTURE==1:
                for x in self.hCapture_multi:
                    tmp_str = 'CaptureStop -captureProxyId' 
                    self.stc_perform(tmp_str,x)
                    tmp_str = 'CaptureDataSave -captureProxyId'
                    strTime = time.strftime(KEY_TIME_FORMAT)
                    tmp_cap_name = ''
                    if x>=len(self.FileName):
                        tmp_cap_name = self.FileName[-1]
                    else:
                        tmp_cap_name = self.FileName[x]
                    tmp_filename = tmp_cap_name +'_'+strTime +'_'+ x
                    msg = 'tmp_filename:' + tmp_filename 
                    log_print(msg)
                    tmp_str_other = '-FileName "'+tmp_filename+'.pcap" -FileNameFormat PCAP -IsScap FALSE'
                    self.stc_perform(tmp_str,x,tmp_str_other)
                    tmp_str = '-PktCount'
                    msg = 'Captured frames:'+self.stc_get(x,tmp_str)
                    log_print(msg)
                    
        except Exception ,exc_str:
            msg = ' stc stop Captured frames error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False 
        
    def stc_result_compare_multi(self):
        
        '''
        compare_mode value:0 ->  ==＄1�7
                           1 ->  > ＄1�7
                           2 ->  < ＄1�7
                           3 ->  >=＄1�7
                           4 ->  <=,
        compare_pass_type:
          0：比较GeneratorPortvalue
          1：比较AnalyzerPortvalue
          2：比较GeneratorPort_compare_AnalyzerPort
          3：比较GeneratorPortvalue与AnalyzerPortvalue
          4：比较GeneratorPortvalue与GeneratorPort_compare_AnalyzerPort
          5：比较AnalyzerPortvalue与GeneratorPort_compare_AnalyzerPort
          6：比较AnalyzerPortvalue，GeneratorPort_compare_AnalyzerPort GeneratorPortvalue
          7: 比较FilterStream_Result_value 
        '''
        if self.errorFlag == False:
            return self.errorFlag
        Bool_result =True
        
        for x in range(len(self.iTxPort)):
            self.ParamGeneratorPortvalue = []
            self.ParamAnalyzerPortvalue = []
            self.ParamGeneratorPort_compare_AnalyzerPort = ['']
                        
            if x>=len(self.compare_pass_type_multi):
                self.compare_pass_type  = self.compare_pass_type_multi[-1]
            else:
                self.compare_pass_type  = self.compare_pass_type_multi[x]
            
            if x>=len(self.ParamGeneratorPortvalue_multi):
                #tmp_num = self.stc_get_rx_hport(self.ParamGeneratorPortvalue_multi[-1].split(':')[0])
                #msg = 'ParamGeneratorPortvalue_multi:' + self.ParamGeneratorPortvalue_multi[-1].split(':')[0]  + 'list_port_add:'+ self.list_port_add[tmp_num]
                #log_print(msg) 
                #self.hGeneratorResults = self.hGeneratorResults_multi[tmp_num]
                #self.ParamGeneratorPortvalue  = self.ParamGeneratorPortvalue_multi[-1].split(':')[1]
                tmp = self.ParamGeneratorPortvalue_multi[-1].split(':')   #['6/12','SigFrameCount>0&&SigFrameCount<10']
                tmp_num = self.stc_get_rx_hport(tmp[0])          
                self.hGeneratorResults = self.hGeneratorResults_multi[tmp_num]
                #self.ParamGeneratorPortvalue[0] = 
                #for i in tmp:
                self.ParamGeneratorPortvalue = tmp[1].split('&&')   #['SigFrameCount>0' , 'SigFrameCount<10']
            else:
                #tmp_num = self.stc_get_rx_hport(self.ParamGeneratorPortvalue_multi[x].split(':')[0])
                #msg = 'ParamGeneratorPortvalue_multi:' + self.ParamGeneratorPortvalue_multi[x].split(':')[0]  + 'list_port_add:'+ self.list_port_add[tmp_num]
                #log_print(msg)
                #self.hGeneratorResults = self.hGeneratorResults_multi[tmp_num]
                #self.ParamGeneratorPortvalue  = self.ParamGeneratorPortvalue_multi[x].split(':')[1]
                tmp = self.ParamGeneratorPortvalue_multi[x].split(':')   #['6/12:SigFrameCount>0' , '6/12:SigFrameCount<10 $']
                tmp_num = self.stc_get_rx_hport(tmp[0])          
                self.hGeneratorResults = self.hGeneratorResults_multi[tmp_num]
                #for i in tmp:
                self.ParamGeneratorPortvalue = tmp[1].split('&&')
            if x>=len(self.ParamAnalyzerPortvalue_multi):
                #tmp_num = self.stc_get_rx_hport(self.ParamAnalyzerPortvalue_multi[-1].split(':')[0])
                #self.hAnalyzerResults = self.hAnalyzerResults_multi[tmp_num]
                #self.ParamAnalyzerPortvalue  = self.ParamAnalyzerPortvalue_multi[-1].split(':')[1]
                tmp = self.ParamAnalyzerPortvalue_multi[-1].split(':')
                tmp_num = self.stc_get_rx_hport(tmp[0])
                self.hAnalyzerResults = self.hAnalyzerResults_multi[tmp_num]
                #for i in tmp:
                self.ParamAnalyzerPortvalue = tmp[1].split('&&')
            else:
                #tmp_num = self.stc_get_rx_hport(self.ParamAnalyzerPortvalue_multi[x].split(':')[0])
                #self.hAnalyzerResults = self.hAnalyzerResults_multi[tmp_num]
                #self.ParamAnalyzerPortvalue  = self.ParamAnalyzerPortvalue_multi[x].split(':')[1]
                tmp = self.ParamAnalyzerPortvalue_multi[x].split(':')
                tmp_num = self.stc_get_rx_hport(tmp[0])
                self.hAnalyzerResults = self.hAnalyzerResults_multi[tmp_num]
                #for i in tmp:
                self.ParamAnalyzerPortvalue = tmp[1].split('&&')
    
            if x>=len(self.ParamGeneratorPort_compare_AnalyzerPort_multi):
                tmp_list = self.ParamGeneratorPort_compare_AnalyzerPort_multi[-1].split('&&')  #['6/12:SigFrameCount ,6/11:GeneratorSigFrameCount>=100','6/12:SigFrameCount ,6/11:GeneratorSigFrameCount<=1000']
                #print  'self.tmp_list:',tmp_list
                #tmp_Analyzer_port = self.stc_get_rx_hport(tmp_list[0].split(',')[0].split(':')[0])
                #self.hAnalyzerResults_both  = self.hAnalyzerResults_multi[tmp_Analyzer_port]
                
                #tmp_Generator_port = self.stc_get_rx_hport(tmp_list[1].split(':')[0])
                #self.hGeneratorResults_both = self.hGeneratorResults_multi[tmp_Generator_port]
                #['6/11:GeneratorSigFrameCount>=100' , '6/11:GeneratorSigFrameCount<=1000']
                #tmp_Generator_port = self.stc_get_rx_hport(tmp_list[0].split(',')[1].split(':')[0])
                #self.hGeneratorResults_both = self.hGeneratorResults_multi[tmp_Generator_port]
                #self.ParamGeneratorPort_compare_AnalyzerPort[0] = tmp_list[0].split(':')[1]
                #for i in tmp:
                #    self.ParamGeneratorPort_compare_AnalyzerPort.append(i.split(':')[1])
                #self.ParamGeneratorPort_compare_AnalyzerPort = tmp_list[0].split(':')[1]  + ',' + tmp_list[1].split(':')[1] + ',' + tmp_list[2]
                #print  'self.ParamGeneratorPort_compare_AnalyzerPort:',self.ParamGeneratorPort_compare_AnalyzerPort
            else:
                tmp_list = self.ParamGeneratorPort_compare_AnalyzerPort_multi[x].split('&&')
                #tmp_Analyzer_port = self.stc_get_rx_hport(tmp_list[0].split(':')[0])
                #self.hAnalyzerResults_both  = self.hAnalyzerResults_multi[tmp_Analyzer_port]
                #tmp_Generator_port = self.stc_get_rx_hport(tmp_list[1].split(':')[0])
                #self.hGeneratorResults_both = self.hGeneratorResults_multi[tmp_Generator_port]
                #tmp = tmp_list[1].split('&&')           #['6/11:GeneratorSigFrameCount>=100' , '6/11:GeneratorSigFrameCount<=1000']
                #tmp_Generator_port = self.stc_get_rx_hport(tmp[0].split('&&')[0])
                #self.hGeneratorResults_both = self.hGeneratorResults_multi[tmp_Generator_port]
                #self.ParamGeneratorPort_compare_AnalyzerPort[0] = tmp_list[0].split(':')[1]
                #for i in tmp:
                #    self.ParamGeneratorPort_compare_AnalyzerPort.append(i.split(':')[1])
                #print self.ParamGeneratorPort_compare_AnalyzerPort,'/////////////////'
                #self.ParamGeneratorPort_compare_AnalyzerPort = tmp_list[0].split(':')[1]  + ',' + tmp_list[1].split(':')[1] + ',' + tmp_list[2]
            
            print 'len(self.FilterStream_Result_value): ',len(self.FilterStream_Result_value)
            if x >= len(self.FilterStream_Result_value):
                self.FilterStream_Result_t = self.FilterStream_Result_value[-1]
            else:
                self.FilterStream_Result_t = self.FilterStream_Result_value[x]
                #print  'self.ParamGeneratorPort_compare_AnalyzerPort:',self.ParamGeneratorPort_compare_AnalyzerPort
            if(Bool_result):
                Bool_result = self.stc_yy_compare(self.hGeneratorResults,self.hAnalyzerResults,tmp_list)
                #print 'Boll_result:',Bool_result, '-----------------------------------------'
                #Bool_result = self.stc_yy_compare(self.hGeneratorResults,self.hGeneratorResults_both,self.hAnalyzerResults,self.hAnalyzerResults_both)
            else:
                self.stc_yy_compare(self.hGeneratorResults,self.hAnalyzerResults,tmp_list)
        #print 'Boll_result:',Bool_result, '-----------------------------------------'
        return Bool_result
        
            
    
  
    def stc_release_testcenter_multi(self):
        try:
            msg = 'Releasing ports ..'
            log_print(msg)
            tmp_str=''
            for x in self.list_port_add:
                tmp_str = tmp_str + ' ' + self.ChassisIp + '/'+ x
            self.stc_release(tmp_str)
            msg = 'Disconnect from the chassis ...'
            log_print(msg)
            self.stc_disconnect(self.ChassisIp)
            msg = 'Deleting project'
            log_print(msg)
            self.stc_delete(self.hProject)
        except Exception ,exc_str:
            log_print('stc_release_testcenter_multi error')
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
          
    '''      
    def stc_read_file_write(self,file_name,len):
        file_object1 = open(file_name,'r')
        tmp_str =''
        for linea in file_object1:
            if linea==' ':
                continue
            else:
                tmp_str = linea.strip()
    '''     
        
    def stc_get_datafromstr(self,x):
        str_t ='0123456789'
        str_r =[ i for i in x if i in str_t ]
        s=('').join(str_r)
        tmp_num = 0
        for x in self.hPort_multi:
            tmp_num =tmp_num +1
            str_l =[i for i in x if i in str_t]
            tmp_s  = ('').join(str_l)
            if cmp(tmp_s,s)==0:
                break
        s = str(tmp_num)
        return s
        
    def stc_Learning_multi(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'Start Learning...'
        log_print(msg)
        self.stream_list_multi =[]
        try:
            for x in self.hPort_multi:
                #self.stream_list_multi.append(self.stc_get(x,"-children-streamblock"))
                self.stc_perform('L2LearningStart -L2LearningOption TX_ONLY -HandleList ', self.stc_get(x,"-children-streamblock"))
                time.sleep(2)
                self.stc_perform('L2LearningStop -HandleList ', self.stc_get(x,"-children-streamblock"))
                time.sleep(1)
        except Exception ,exc_str:
            log_print('stc_Learning_multi error')
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
            
    def stc_ClearResults(self):
        if self.errorFlag == False:
            return self.errorFlag
        msg = 'ResultClearAllTraffic ...'
        log_print(msg)
        try:
            self.stc_perform('ResultClearAllTraffic')
            time.sleep(1)
        except Exception ,exc_str:
            log_print('ResultClearAllTraffic error')
            self.stc_print_flag_error(exc_str)
            return self.errorFlag
        return self.errorFlag
        
        
    def stc_infoprint(self,list_hwd):
        for y in list_hwd:
            info = self.stc_get ( y)
            for x in info.split('-'):
                if len(x.strip())==0:
                    continue
                x ='          -' + x
                log_print(x)
             
    
    def stc_testcenter_multi_test(self,filename='E:\\Simu_server\\auto_conf\\stream_param.xls',sheetname = 'multi_stream',waitfor ='0'):
        self.list_port_add =[]
        try:
            self.stc_initpare_multi(filename,sheetname)
            self.stc_CreateProject_multi()
            self.stc_create_port_multi()
            self.stc_create_physical_interface()
            self.stc_create_port_generator_multi()
            self.stc_create_port_Analyzer_multi()
            self.stc_create_stream_block_multi()
            self.stc_create_ethernet_head_multi()
            if len(self.ipv4_sel)>0:
                self.stc_create_ipv4_multi()
                self.stc_create_ipv4diffserv_multi()
            self.stc_create_vlan_multi_multitag()
            self.stc_filter_config_multi()
            self.stc_apply()
            self.stc_modify_stream_multi()
            self.stc_Config_Generator_multi()
            
            if self.infoprintflag ==True:
                log_print('*************Port infomation:*************')
                self.stc_infoprint(self.hPort_multi)
                log_print('*************Port infomation:*************')
            
                log_print('*************PortTxCopperInterface infomation:*************')
                self.stc_infoprint(self.hPortTxCopperInterface_multi)
                log_print('*************PortTxCopperInterface infomation:*************')
            
                log_print('*************PortTxCopperInterface infomation:*************')
                self.stc_infoprint(self.hPortTxCopperInterface_multi)
                log_print('*************PortTxCopperInterface infomation:*************')
            
                log_print('*************filter infomation:*************')
                self.stc_infoprint(self.hAnalyzerFrameConfigFilter_multi)
                log_print('*************filter infomation:*************')
            
                log_print('*************Stream infomation:*************')
                self.stc_infoprint(self.hStreamBlock_multi)
                log_print('*************Stream infomation:*************')
                
            self.stc_Realtime_Result_multi()
            self.stc_Configuring_Analyzer_multi()
            
            self.stc_Learning_multi()
            self.stc_ClearResults()
            self.stc_Configure_Capture_multi()
            
            self.stc_apply()
            if waitfor =='1':
                self.stc_traffic_stream_multi_waitfor()
            else:
                self.stc_traffic_stream_multi()
            
            self.stc_filter_GetStream()
            
            for x in range(len(self.hGeneratorResults_multi)):
                if x>=len(self.ParamGeneratorPort):
                    self.stc_result_print_multi(self.ParamGeneratorPort[-1],self.hGeneratorResults_multi[x],port_str='GeneratorPort')
                else:
                    self.stc_result_print_multi(self.ParamGeneratorPort[x],self.hGeneratorResults_multi[x],port_str='GeneratorPort')
            for x in range (len(self.hAnalyzerResults_multi)):
                if x>= len(self.ParamAnalyzerPort):
                    self.stc_result_print_multi(self.ParamAnalyzerPort[-1],self.hAnalyzerResults_multi[x],port_str='AnalyzerPort')
                else:
                    self.stc_result_print_multi(self.ParamAnalyzerPort[x],self.hAnalyzerResults_multi[x],port_str='AnalyzerPort')
            
            
            msg = '################ this result of multi case ################'
            log_print(msg)
            
            self.resultFlag =self.stc_result_compare_multi()
            msg = '################ this result of multi  ################'
            log_print(msg)
            #print 'iiiiiiiiiiiiiiiiiiiiiiii'
            #print 'self.resultFlag:',self.resultFlag
            #print 'iiiiiiiiiiiiiiiiiiiiiiii'
            self.stc_stop_Captured_frames_multi()
            self.stc_release_testcenter_multi()
            
            
        except Exception ,exc_str:
            msg = 'stc_testcenter_multi_test error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.stc_release_testcenter_multi()
            self.errorFlag=False
            self.resultFlag = False
        return self.stc_get_resultFlag()
    
    def stc_loadfile_init(self,filename,sheetname):
        try:
            self.list_port_add = []
            self.load_port= []
            initstream = readexcel(filename,sheetname)
            keyvalue_t = initstream.Excel_read()
            msg = '***************** excel read data *****************' 
            log_print(msg)
            msg = keyvalue_t 
            log_print(msg)
            msg = '***************** excel read data *****************' 
            dic = self.stc_global_keyreplay(keyvalue_t)
            if dic ==None:
                return  self.errorFlag   
            keyvalue = dic
            if keyvalue.has_key('ChassisIp'):
                self.ChassisIp = keyvalue['ChassisIp']
            if keyvalue.has_key('Port'):
                #self.load_Port = keyvalue['Port']
                self.list_port_add = keyvalue['Port'].strip(' ').split(',')
            if keyvalue.has_key('ParamGeneratorPortvalue'):
                self.load_ParamGeneratorPortvalue = keyvalue['ParamGeneratorPortvalue']
            if keyvalue.has_key('file_template'):
                self.load_file_template = keyvalue['file_template']
            if keyvalue.has_key('Compare_Type'):
                self.load_Compare_Type = keyvalue['Compare_Type']
            if keyvalue.has_key('ParamAnalyzerPortvalue'):
                self.load_ParamAnalyzerPortvalue = keyvalue['ParamAnalyzerPortvalue']
            if keyvalue.has_key('PGenerator_radio_Analyzer'):
                self.load_PGenerator_radio_Analyzer = keyvalue['PGenerator_radio_Analyzer']
            if keyvalue.has_key('FilterStream_Result'):
                self.load_FilterStream_Result = keyvalue['FilterStream_Result']
            
        except Exception ,exc_str:
            msg = 'stc_loadfile  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            return self.errorFlag  
        
    
    
    def stc_load_physicalport(self,portlist=[]):
        if len(portlist)==0:
            portlist = self.load_port
        try:
            for x in portlist:
                tmp = ' EthernetCopper -under ' + x
                self.stc_create(tmp)
        except Exception ,exc_str:
            msg = 'stc_load_physical port  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            
    def stc_load_set_portlist(self):
        tmp = 0
        tmp_str =''
        for x in self.load_port:
            if tmp ==0:
                tmp_str = '" ' + x + ' '
            elif tmp==len(self.load_port)-1:
                tmp_str  = tmp_str + ' ' + x + ' "'
            else:
                tmp_str = tmp_str + ' ' + x + ' '
            tmp = tmp + 1
        return tmp_str 
    '''
    def stc_load_get_file(self,filename):
        
        return self.tclsh.eval()
    '''
    def stc_load_setfile_all(self):
        try:
            tmp_str = ' L2TestLoadTemplate -FileName ' +  self.load_file_template.strip(' ').split(',')[-1]
            self.stc_perform(tmp_str)
            tmp_str = ' L2TestLoadTemplate -LoadDefault TRUE '
            self.stc_perform(tmp_str)
        except Exception ,exc_str:
            msg = 'stc_load_setfile_all port  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            
     
    def stc_load_getparam(self,strname_find,handle):
        str_return = 'NULL'
        try:
            if handle=='NULL':
                str_return = 'NULL'
            else:
                tmp_str = self.stc_get(handle,'-children')
                list_children = tmp_str.split(' ')
                print 'strname_find:',strname_find
                print 'list_children:',list_children
                for x in list_children:
                    if x.find(strname_find)>-1:
                        str_return = x
                        break
                    else:
                        str_return = 'NULL'
        except Exception ,exc_str:
            msg = 'stc_load_getparam from handle:' +handle +' children  Error :' + strname_find   
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
        return str_return
    
    def stc_load_get_system_p(self):
        self.load_generator_list = self.stc_load_get_handle_list(findstr='generator')
        self.load_analyzer_list = self.stc_load_get_handle_list(findstr='analyzer')
        
    def stc_load_traffic_stream(self):
        msg = '##### stc_load_traffic_stream fuction #####'
        log_print(msg)
        if self.errorFlag == False:
            return self.errorFlag
        #print "Start Analyzer"
        self.hGeneratorResults_multi=[]
        self.hAnalyzerResults_multi = []
        try:
            msg = 'Start Analyzer'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str = 'AnalyzerStart -AnalyzerList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                msg = 'Current analyzer state' + self.stc_get(x,tmp_str)
                log_print(msg)
            msg = 'Start Generator'
            log_print(msg)
            for x in self.hGenerator_multi:
                tmp_str = 'GeneratorStart -GeneratorList'
                self.stc_perform(tmp_str,x)
                tmp_str = ' -state'
                #print 'Current generator state ',self.stc_get(self.hGenerator,tmp_str)
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Start Analyzer or  Start Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        msg = 'wait '+ str(self.waittime)+' seconds'
        log_print(msg)
        time.sleep(self.waittime)
        
        try:
            for x in self.hAnalyzer_multi:
                msg = 'Current analyzer state '+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGenerator_multi:
                msg = 'Current generator state '+self.stc_get(x,tmp_str)
                log_print(msg)
        except Exception ,exc_str:
            msg = 'Current Analyzer state or  Current Generator state error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        try:
            msg = 'stop Generator'
            log_print(msg)
            for x in  self.hGenerator_multi:
                tmp_str ='GeneratorStop -GeneratorList'
                self.stc_perform(tmp_str,x)
            msg = 'Stop the analyzer.'
            log_print(msg)
            for x in self.hAnalyzer_multi:
                tmp_str ='AnalyzerStop -AnalyzerList'
                self.stc_perform(tmp_str,x)
        except Exception ,exc_str:
            msg = 'Stop Analyzer or  Stop Generator  error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
        
        try:
            for x in self.hGenerator_multi:
                tmp_str =' -children-GeneratorPortResults'
                self.hGeneratorResults_multi.append( self.stc_get( x,tmp_str))
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hGeneratorResults_multi
                log_print(msg)
                msg= '----self.hGeneratorResults_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
            for x in self.hAnalyzer_multi:
                tmp_str = '-children-AnalyzerPortResults'
                self.hAnalyzerResults_multi.append(self.stc_get(x,tmp_str))
                msg= '----self.hAnalyzerResults_multi port:' + x + '  -----'
                log_print(msg)
                msg = self.hAnalyzerResults_multi
                log_print(msg)
                msg= '----self.hStreamBlock_multi port:' + x + '  -----'
                log_print(msg)
                #time.sleep(5)
        except Exception ,exc_str:
            msg = ' Analyzer port result or  Generator port result error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
        msg = 'wait 20S AnalyzerResult'
        log_print(msg)
        time.sleep(20)
        
        try:
            for x in self.hAnalyzerResults_multi:
                tmp_str = '-sigFrameCount'
                #print '\tSignature frames:',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tSignature frames:' + self.stc_get(x,tmp_str)
                log_print(msg)
                tmp_str = '-totalFrameCount'
                #print '\tTotal frames',self.stc_get(self.hAnalyzerResults,tmp_str)
                msg = '\tTotal frames'+self.stc_get(x,tmp_str)
                log_print(msg)
            for x in self.hGeneratorResults_multi:
                tmpstr = ' -GeneratorFrameCount'
                #print 'Send packets:', self.stc_get(self.hGeneratorResults,tmpstr)
                msg = 'Send packets:'+ self.stc_get(x,tmpstr)
                log_print(msg)
        
        except Exception ,exc_str:
            msg = ' get port frames error'
            log_print(msg)
            self.stc_print_flag_error(exc_str)
            self.errorFlag=False
            
        
    def stc_load_test_run(self):
        self.stc_load_get_system_p()
        log_print(self.load_analyzer_list)
        log_print(self.load_generator_list)
        self.hAnalyzer_multi = self.load_analyzer_list
        self.hGenerator_multi = self.load_generator_list
        self.hPort_multi = self.load_port
        #self.stc_Configure_Capture_multi()
        self.stc_load_traffic_stream()
        time.sleep(120)
        
    def stc_load_get_handle_list(self,handlist=[],findstr=''):
        re_list = []
        if len(handlist)==0:
            handlist = self.load_port
        for x in handlist:
            tmp_str= self.stc_load_getparam(findstr,x)
            re_list.append(tmp_str)
        return re_list
            
    def stc_load_setfile_differ(self):
        try:
            tmp_num = 0
            tmp_total = len(self.load_file_template.strip(' ').split(','))
            for x  in self.load_port:
                if  tmp_total== 0:
                    log_print('There are no config files')
                    self.errorFlag =False
                    break
                elif tmp_total <=tmp_num:
                    tmp_str = ' L2TestLoadTemplate -Port "'+' '+self.load_port[tmp_num] +'" -FileName '  +  self.load_file_template.strip(' ').split(',')[tmp_num]
                else:
                    tmp_str = ' L2TestLoadTemplate -Port "'+' '+self.load_port[tmp_num] +'" -FileName '  +  self.load_file_template.strip(' ').split(',')[-1]
                self.stc_perform(tmp_str)
                tmp_str = ' L2TestLoadTemplate -Port "'+' '+self.load_port[tmp_num] +' " -LoadDefault TRUE '
                self.stc_perform(tmp_str)
                tmp_num = tmp_num +1
            self.load_file_template.strip(' ').split(',')
        except Exception ,exc_str:
            msg = 'stc_load_create port  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
    def stc_load_creatport(self):
        try:
            for x in self.list_port_add:
                tmp_str = ' port -under  project1 -location //' + self.ChassisIp + '/'+x
                self.load_port.append(self.stc_create(tmp_str))
        except Exception ,exc_str:
            msg = 'stc_load_create port  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
            
    def stc_load_attachport(self):
        try:
            self.stc_eval_multi()
            tmp_str = ' attachPorts -portlist ' +  self.stc_load_set_portlist()
            self.stc_perform(tmp_str)
        except Exception ,exc_str:
            msg = 'stc_load_attach port  Error'
            log_print(msg)
            log_print(exc_str)
            self.error = exc_str
            self.errorFlag =False
        #return self.load_port
    
    def stc_load_realse(self):
        self.stc_perform(' chassisDisconnectAll')
        self.stc_delete(' project1')

        
    def stc_loadfile(self,filename,sheetname):
        self.stc_CreateProject_multi()
        self.stc_loadfile_init(filename,sheetname)
        self.stc_load_creatport()
        self.stc_load_physicalport()
        self.stc_load_attachport()
        self.stc_load_setfile_all()
        self.stc_load_test_run()
        
        #self.stc_load_setfile_differ()
        self.stc_load_realse()
        return True
    
    
if __name__ == "__main__":
    t_stc=Stc()
    #t_stc.stc_stream_test('E:\\Simu_server\\auto_conf\\stream_param.xls','load_xml')
    #t_stc.stc_testcenter_multi_test()
    t_stc.stc_testcenter_multi_test(filename='E:\\Simu_server\\auto_conf\\stream_param.xls',sheetname = 'multi_4094_both')
    '''
    #args = 'system1','-Version'
    
    log_print('The result:')
    log_print(t_stc.stc_get_resultFlag())
    '''
    
   
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
