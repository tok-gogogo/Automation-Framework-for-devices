import os
import sys
import re

def find_new_port(filepath):
    fileopen = open(filepath)
    filelist = fileopen.read()
    fileopen.close()
    tmp_msg ='Location="//'+'.+'+'"'
    tmp_list = re.findall(tmp_msg,filelist)
    tmp_list = list(set(tmp_list))
    for x in tmp_list:
        print 'port:',x[9:]
    
    tmp_msg ='STREAMBLOCK ID='+'.'+'<STREAMBLOCK>'
    
    tmp_list = re.findall(tmp_msg.upper(),filelist.upper(),re.S)
    
    tmp_list = list(set(tmp_list))
    tmp_str =''
    tmp_list_name=[]
    for x in tmp_list:
        print '***********'
        print x
        print '***********'
        tmp_msg ='Name='+'.+'+'"' 
        tmp_list1 = []
        tmp_list1 = re.findall(tmp_msg.upper(),x)
        tmp_list_name.append( '$$'.join(tmp_list1))
    tmp_list_name = '$$'.join(tmp_list_name) .split('$$')
    for x in tmp_list_name:
        print 'StreamName:',x[5:]
    
    
def find_port(filepath,tmp_msg = 'Location="//192.168.22.253/'):
    print filepath
    line_count = 0
    port_list = []
    fileopen = open(filepath)
    port_line = {}
    filelist = fileopen.readlines()
    fileopen.close()
    for line in filelist:
        line_count =line_count + 1
        tmp_list = re.findall(tmp_msg,line)
        if (len(tmp_list)>0):
            tmp_count = 0
            tmp_port = line.strip().split(tmp_msg)[-1].strip('"')
            if len(port_list)==0:
                port_list.append(tmp_port)
                port_line[tmp_port] = line_count
            for port in port_list :
                tmp_count +=1
                if port == tmp_port:
                    break
                if tmp_count == len(port_list):
                    port_list.append(tmp_port)
                    port_line[tmp_port] = line_count
    print_msg(port_list,port_line)
    
def print_msg(list_msg,dic_msg):
    print '  ','port','   ','line'
    for port in list_msg:
        print '  ',port,  '   ',dic_msg[port]
    print '  ','total port number:',len(list_msg)
        

if __name__=='__main__':
    #print 'hello'
    FileName =raw_input("please input file:")
    find_new_port(FileName)
