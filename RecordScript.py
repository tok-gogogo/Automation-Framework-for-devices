#-*- coding: UTF-8 -*- 
#-----------------------------------------------------------------------------
# Name:        RecordScript.py
# Purpose:     Record telnet script for CERSRT
#
# Author:      gongke
#
# Created:     2014/07/10
# RCS-ID:      $Id: RecordScript.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import pythoncom
import pyHook
from public import *
g_list = ['            mycommand$        ']
g_Recoder_Flag = False
g_sys_Debug = False
g_sys_timeget ='1'
g_telnet_ip=''
g_Stop_First_Flag = True 
g_file_object =None
g_file_path = None
g_tmp_stop_Flag = False
g_Tab_add_space = True
g_find_show_cmd =False
g_MultiFind  = False
g_Mouse_Pos =False

def Get_SystemParam():
    global g_Recoder_Flag 
    global g_sys_Debug
    global g_sys_timeget
    global g_Tab_add_space
    global g_find_show_cmd
    global g_MultiFind 
    global g_Mouse_Pos 
    
    tmp_conf_file = find_parentpath()+'\\auto_conf\\version.ini'
    
    try:
        if read_ini(tmp_conf_file,'debug','Record_debug').strip().upper()=='ON':
            g_sys_Debug = True
    except Exception,e:
            log_print(e)
            pass
    try:
        if read_ini(tmp_conf_file,'Mouse_Pos','Record_debug').strip().upper()=='ON':
            g_Mouse_Pos = True
    except Exception,e:
            log_print(e)
            pass
        
    try:
        if read_ini(tmp_conf_file,'MultiFind','Record_debug').strip().upper()=='ON':
            g_MultiFind = True
    except Exception,e:
            log_print(e)
            pass
    try:
        if read_ini(tmp_conf_file,'Tab_add_space','Record_debug').strip().upper()=='ON':
            g_Tab_add_space = True
    except Exception,e:
            log_print(e)
            pass
        
    try:
        if read_ini(tmp_conf_file,'Relace_Show','Record_debug').strip().upper()=='ON':
            g_find_show_cmd = True
    except Exception,e:
            log_print(e)
            pass
        
        
    try:
        g_sys_timeget = read_ini(tmp_conf_file,'default_time','Record_debug').strip()
        if g_sys_timeget ==None:
            g_sys_timeget ='1'
    except Exception,e:
            log_print(e)
            pass
        
def onMouseEvent(event):
    # ��������¼�
    global g_Recoder_Flag 
    global g_sys_Debug
    global g_sys_timeget
    global g_file_object
    global g_Mouse_Pos
    if g_sys_Debug ==True:
        print "MessageName:", event.MessageName
        print "Message:", event.Message
        print "Time:", event.Time
        print "Window:", event.Window
        print "WindowName:", event.WindowName
        print "Position:", event.Position
        print "Wheel:", event.Wheel
        print "Injected:", event.Injected
        print "---"
    else:
        if g_Mouse_Pos:
            print "Position:", event.Position
        # ���� True �Ա㽫�¼����������������
        # ע�⣬���������� False ��������¼�����ȫ������
        # Ҳ����˵�����꿴�����Ὡ���Ƕ����ƺ�ʧȥ��Ӧ��
    return True
    
def onKeyboardEvent(event):
    global g_Recoder_Flag 
    global g_sys_Debug
    global g_sys_timeget
    global g_file_object
    global g_telnet_ip
    global g_file_path
    global g_list
    global g_Stop_First_Flag
    global g_tmp_stop_Flag
    global g_Tab_add_space 
    
    name = g_telnet_ip + ' - SecureCRT'
    tmp_name = event.WindowName
    tmp_KeyId = event.KeyID
    tmp_asscii = event.Ascii
    if g_sys_Debug == True:
        # ���������¼�
        print "MessageName:", event.MessageName
        print "Message:", event.Message
        print "Time:", event.Time
        print "Window:", event.Window
        print "WindowName:", tmp_name
        print "Ascii:", tmp_asscii, chr(tmp_asscii)
        print "Key:", event.Key
        print "KeyID:", tmp_KeyId
        print "ScanCode:", event.ScanCode
        print "Extended:", event.Extended
        print "Injected:", event.Injected
        print "Alt", event.Alt
        print "Transition", event.Transition
        print "---"
        # ͬ����¼����������ķ���ֵ
    if tmp_KeyId==119:
        #F8 �˳�¼�����
        if g_file_object!=None:
            #g_file_object.writelines('            close$        ')
            g_file_object.close()
        sys.exit(0)
        
    if tmp_name.find(name)>-1:
        if tmp_KeyId == 120:
            #F9 ��ʼ����
            if g_Recoder_Flag ==False:
                g_Recoder_Flag=True
                print 'Record telnet module  start...: '
                g_file_object = open(g_file_path,'a')
                g_file_object.writelines('#telnet       \r\n')
                msg = '            init$                '+ g_telnet_ip +' ,23 ,admin ,admin ,1 \r\n' 
                g_file_object.writelines(msg)
            g_Stop_First_Flag = False
        if tmp_KeyId == 121:
            #F10 �������˳�
            g_Recoder_Flag=False
            if g_Stop_First_Flag ==False:
                print 'telnet modeule Record stop...:'
                if len(g_list)>1:
                    msg = Msg_set_1(g_list)
                    g_file_object.writelines(msg)
                    print msg
                g_list=['            mycommand$        ']
                g_file_object.writelines('            close$        \r\n')
                print '            close$        ' 
        else:
            if g_Recoder_Flag==True:
                if tmp_KeyId  == 123:
                    #F12
                    st= g_list.pop()
                    if g_Tab_add_space==False:
                        g_list.append(st[:-1])
                    else:
                        g_list.append(st[:-2])
                    g_tmp_stop_Flag =False
                if tmp_KeyId ==122:
                    #F11
                    if g_tmp_stop_Flag ==False:
                        g_tmp_stop_Flag = True
                        if len(g_list)>0:
                            tmp_list =g_list[1:]
                        else:
                            tmp_list=['']
                        print 'If you continue,please Sendkey F12,record cmd: ',''.join(tmp_list)
                if g_tmp_stop_Flag ==True:
                    pass
                else:
                    if tmp_KeyId==13:
                        #�س�����
                        if len(g_list)>1:
                            msg = Msg_set_1(g_list)
                            g_file_object.writelines(msg)
                            print msg
                            g_list=['            mycommand$        ']
                    
                    elif tmp_KeyId ==9:
                        #TAB����
                        if g_Tab_add_space ==True:
                            g_list.append(' ')
                        tmp_list =g_list[1:]
                        print 'warn...,you used key TAB ,record cmd:',''.join(tmp_list)
                        pass
                    elif tmp_KeyId ==20:
                        #��Сд�л���
                        pass
                    elif tmp_KeyId ==8:
                        #Backspace����
                        if len(g_list)>1:
                            del g_list[-1]
                    else:
                        g_list.append( chr(tmp_asscii))
    return True

def  Msg_set_1(list_g):
    global g_find_show_cmd 
    global g_MultiFind
    global g_sys_timeget
    msg =''
    if g_find_show_cmd == True and ''.join(list_g).upper().find(' SHOW ')>-1:
        if g_MultiFind==True:
            msg = '            find_command_Multi$        '+''.join(list_g[1:]) + ', )# ,**..**,' + g_sys_timeget + ',1,1\r\n'
        else:
            msg = '            find_command_Multi$        '+''.join(list_g[1:]) + ', )# ,**..**,' + g_sys_timeget + ',0,1\r\n'
    else:
        msg = ''.join(g_list) + '  , )# , ' + g_sys_timeget + '\r\n'
    return msg
    
def main():
    global g_Recoder_Flag 
    global g_sys_Debug
    global g_sys_timeget
    global g_file_object
    global g_telnet_ip
    global g_file_path
    
    Get_SystemParam()
    g_telnet_ip = raw_input("please input the SecureCRT session Ip:")
    g_file_path = raw_input("please save the records script Name:")
    if g_file_path.find(':')<0:
        g_file_path= find_parentpath() +'\\tmp_result\\'+g_file_path
    
    if file_exist(g_file_path)==True:
        os.remove(g_file_path)
    # ����һ�������ӡ��������
    print '............Please run SecureCRT sendkeys.............'
    print 'F9  -- start telnet module '    
    print 'F10 -- stop telnet module'
    print 'F11 -- temporary pause      '
    print 'F12 -- temporary continue    '
    print 'F8  -- Record  program  exit'
    hm = pyHook.HookManager()
    # �������м����¼�
    hm.KeyDown = onKeyboardEvent
    # ���ü��̡����ӡ�
    hm.HookKeyboard()
    # ������������¼�
    hm.MouseAll = onMouseEvent
    # ������ꡰ���ӡ�
    hm.HookMouse()
    # ����ѭ�����粻�ֶ��رգ�����һֱ���ڼ���״̬
    pythoncom.PumpMessages()
    
if __name__ == "__main__":
    main()
    