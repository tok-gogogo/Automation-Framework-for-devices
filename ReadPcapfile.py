#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        ReadPcapfile.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2014/06/05
# RCS-ID:      ReadPcap file and cmp
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------

import struct
from public import *
import re
import os
import sys
import string
from wtResult import clsWtResult
from public import *
import WtLog

class Read_pcap():
    def __init__(self):
        self.pcapfile  = None
        self.string_data = None
        self.pcap_header = {}
        self.debug_pcap =True
        self.packet_num = 0
        self.packet_data = []
        self.pcap_packet_header = {}
        self.hex_pcap_data = []
        self.key_word_start = 0
        
        
    
    def read_debug(self,file,keyword,model='Pcap_Read'):
        
        autoversion_str = read_ini(file,keyword,model)
        if autoversion_str.startswith('on')==True:
            self.debug_pcap =True
        else:
            self.debug_pcap =False
            
    def ReadPcap(self,file_name):
        if file_exist(file_name)==False:
            return False
        fpcap = open(file_name,'rb')
        self.string_data = fpcap.read()
        self.pcap_header['magic_number'] = self.string_data[0:4]
        self.pcap_header['version_major'] = self.string_data[4:6]
        self.pcap_header['version_minor'] = self.string_data[6:8]
        self.pcap_header['thiszone'] = self.string_data[8:12]
        self.pcap_header['sigfigs'] = self.string_data[12:16]
        self.pcap_header['snaplen'] = self.string_data[16:20]
        self.pcap_header['linktype'] = self.string_data[20:24]
        
        if self.debug_pcap ==True:
            msg = 'Pcap file head:'
            log_print('msg')
            for key in ['magic_number','version_major','version_minor','thiszone',
                        'sigfigs','snaplen','linktype']:
                msg =  repr(self.pcap_header[key])
                msg =' '.join(msg.split('\\x'))
                msg = key+ "$     " + msg +'\n'
                log_print(msg)
                
        #pcap�ļ�����ݰ���� 
        step = 0
        self.packet_num = 0
        self.packet_data = []
        self.pcap_packet_header = {}
        i =24
        while(i<len(self.string_data)):
            #��ݰ�ͷ�����ֶ�
            self.pcap_packet_header['GMTtime'] = self.string_data[i:i+4]
            self.pcap_packet_header['MicroTime'] = self.string_data[i+4:i+8]
            self.pcap_packet_header['caplen'] = self.string_data[i+8:i+12]
            self.pcap_packet_header['len'] = self.string_data[i+12:i+16]
            #����˰�İ�len
            packet_len = struct.unpack('I',self.pcap_packet_header['len'])[0]
            #д��˰����
            self.packet_data.append(self.string_data[i+16:i+16+packet_len])
            i = i+ packet_len+16
            self.packet_num+=1
        return True
    
    def Get_hexdata(self,frame_data,num_tmp = 0):
        raw_data = []
        asc_data = []
        display_data = []
        temp = ''
        tmp_pcapdata_list=[]
        temp_pcap = ''
        for i in range(len(frame_data)):
            temp = ord(frame_data[i])
            temp = hex(temp)
            if len(temp)==3:
                temp = temp.replace('0x','0x0')
            temp = temp.replace('0x',' ')
            temp_pcap = temp.strip()
            tmp_pcapdata_list.append(temp_pcap)
            
        tmp_pcapdata = ':'.join(tmp_pcapdata_list)
        #print 'tmp_data:',tmp_pcapdata
        return tmp_pcapdata
        
    def display_hexdata(self,frame_data,num_tmp = 0):
        #row_num = ['0x0000','0x0010','0x0020','0x0030','0x0050','0x0060','0x0070']
        raw_data = []
        asc_data = []
        display_data = []
        temp = ''
        tmp_pcapdata_list=[]
        temp_pcap = ''
        for i in range(len(frame_data)):
            temp = ord(frame_data[i])
            temp = hex(temp)
            if len(temp)==3:
                temp = temp.replace('0x','0x0')
            temp = temp.replace('0x',' ')
            temp_pcap = temp.strip()
            raw_data.append(temp)
            tmp_pcapdata_list.append(temp_pcap)
            asc = int(temp,16)
            if(asc>=32 and asc<=126):
                asc_data.append(chr(asc))
            else:
                asc_data.append('.')
        
        tmp_pcapdata = ':'.join(tmp_pcapdata_list)
        while(len(raw_data)%16!=0):
            raw_data.append('   ')
            asc_data.append(' ')
        temp1 = ''
        temp2 = ''
        
        for j in range(len(raw_data)):
            if (j==0 or j%16!=0):
               temp1 = temp1+raw_data[j]
               temp2 = temp2+asc_data[j]
            elif j%16==0:
                temp1 = temp1 + ';' + temp2
                display_data.append(temp1) 
                temp1 = ''
                temp2 = ''
                temp1=temp1+raw_data[j]
    
        display_data.append(temp1)
        if self.debug_pcap == True:
            log_print('*********************** this is ' + str(num_tmp) +' pcap data 16 ***********************')
            for i in display_data:
                log_print(i)
            log_print('*********************** this is ' + str(num_tmp) +' pcap data all ***********************')
            log_print(tmp_pcapdata) 
            
        return tmp_pcapdata
            
    
    def cmp_list_filter(self,list_filter,pcapdata):
        for x in range(1,len(list_filter)):
            find_str = list_filter[x].split('==')[-1].strip()
            find_start = list_filter[x].split('==')[0].strip().split('[')[-1].split(':')[0].strip()
            start_num = pcapdata.find(find_str)
            if start_num > -1:
                if start_num*3 != string.atoi(find_start):
                    return False
            else:
                return False
            
                
        
    def Filter_String(self,str_filter):
        self.Filterstring = ''
        tmp_fiter_dic = {}
        tmp_filter_list = []
        filter_list = str_filter.strip().lower().split('and')
        
        if len(filter_list) ==0 :
            msg='not Filter ,error!!!!'
            log_print(msg)
            return False
        
        for x in filter_list:
            find_str = x.split('==')[-1].strip()
            find_start = string.atoi(x.split('==')[0].strip().split('[')[-1].split(':')[0].strip())
            find_total = string.atoi(x.split('==')[0].strip().split('[')[-1].split(':')[-1].split(']')[0].strip())
            #tmp_filter_list.append({find_start:[find_start,find_total,find_str]})
            value = [find_start,find_total,find_str]
            #print 'value',value
            tmp_fiter_dic[find_start] = value
            #print 'tmp_fiter_dic:',tmp_fiter_dic
        tmp1 = 0
        tmp2 = 0
        tmp3 = 0 
        #print 'tmp_fiter_dic.keys():',tmp_fiter_dic.keys()
        keys_list = tmp_fiter_dic.keys()
        keys_list.sort()
        #print 'keys_list:',keys_list
        for x in keys_list:
            tmp_num = (tmp_fiter_dic[x][0]- tmp1)*3
            if tmp2==0:
                self.key_word_start = tmp_num
            tmp2+=1
            if tmp_num == 0:
                self.Filterstring =self.Filterstring + tmp_fiter_dic[x][2]
            else:
                if tmp2 >1:
                    self.Filterstring =self.Filterstring + '[\S]{' + str(tmp_num-tmp3*3+1) + '}'+tmp_fiter_dic[x][2]
                else:
                    self.Filterstring =self.Filterstring + '[\S]{' + str(tmp_num-tmp3*3) + '}'+tmp_fiter_dic[x][2]
            tmp1 = tmp_fiter_dic[x][0]
            tmp3 = tmp_fiter_dic[x][1]
        if self.debug_pcap == True:
            log_print('filter programe:'+self.Filterstring) 
        return True
            
            
        
        
    def cmp_data(self,str_filter,file_name,cmp_num = '0'):
        #print '..... fuction cmp_data....'
        find_Flag =False 
        if self.Filter_String(str_filter) ==False:
            return -1
        total_num = 0
        if len(self.Filterstring) ==0 :
            msg='Filter string,error!!!!'
            log_print(msg)
            return -1
        for x in self.hex_pcap_data:
            x = x.lower()
            if self.debug_pcap == True:
                if len(re.findall(self.Filterstring,x))>0:
                    log_print('find packet:' + x)
                    log_print(repr(re.findall(self.Filterstring,x)))
            it = re.finditer(self.Filterstring,x)
            for match in it:
                start_num = match.start()
                if start_num== 0:
                    total_num +=1
                    break
        
        return total_num
        '''
        if total_num >0:
            find_Flag = True
        tmp_msg = ''
        if cmp_num !='0':
            if string.atoi(cmp_num) != total_num:
                find_Flag  =False
                tmp_msg =' not you want  ' + cmp_num + ' packages'
        
        if find_Flag == False:
            log_print(str_filter + ' error  find: '+str(total_num)+' packages in the file:' + file_name +' '+ tmp_msg)
            return False
        else:
            log_print(str_filter + '  find: ' + str(total_num)  + ' packages in the file:' + file_name )
            return  True
        return True
        '''
            
    def cmp_data_run(self,file_name,str_filter,cmp_num='0'):
            #print '..... fuction cmp_data_run....'
            file  = find_parentpath()
            file = file +'\\auto_conf\\version.ini'
            self.read_debug(file,'debug','Pcap_Read') 
            if self.ReadPcap(file_name) ==False:
                return -1
            num_pcap = 0
            self.hex_pcap_data = []
            if self.debug_pcap == True:
                for i in self.packet_data:
                    num_pcap+=1
                    tmp_data = self.display_hexdata(i,num_pcap)
                    self.hex_pcap_data.append(tmp_data)
                num_pcap = self.cmp_data(str_filter,file_name,cmp_num)
            else:
                for i in self.packet_data:
                    num_pcap+=1
                    tmp_data = self.Get_hexdata(i,num_pcap)
                    self.hex_pcap_data.append(tmp_data)
                num_pcap = self.cmp_data(str_filter,file_name,cmp_num)
            return num_pcap
            '''
            if self.cmp_data(str_filter,file_name,cmp_num) ==False:
                return False
            return True
            '''
            

if __name__ == "__main__":
    print 'start time:',time.time()
    test = Read_pcap()
    
    file_name  = 'E:\\Simu_server\\result\\20140726__104328_port_5_8.pcap'
    #str_filter = 'frame[0:5]==ff:ff:ff:ff:ff  and frame[14:2]==45:00 and  frame[6:2]==00:24'
    #str_filter = 'frame[14:2]==45:00'
    #str_filter = 'frame[12:2]==08:06'
    str_filter = ' frame[14:2]==c3:ea and frame[18:2]==c0:66 and frame[0:2]==00:10 '
    startTime = time.time()
    print 'startTime:',startTime
    result = test.cmp_data_run(file_name,str_filter)
    print 'result1:',result,'time use:',time.time()-startTime
    
    '''
    file_name  = 'E:\\test_case_auto\\1.pcap'
    str_filter = 'frame[14:2]==60:c8 and frame[0:2]==00:10 and frame[20:2]==00:6a and frame[30:4]==c0:a8:00:02 and frame[112:2]==4f:dc'
    result = test.cmp_data_run(file_name,str_filter)
    print 'result2:',result
    '''