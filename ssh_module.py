#-*- coding: utf-8 -*-
#!/usr/bin/python 
# SSH ����ģ��
import paramiko 
from public import *


class ssh2:    
    def __init__(self,ip,username,passwd,port='22'):  
    	self.ip = ip  
        self.username = username  
        self.passwd = passwd
        self.port = string.atoi(port)

    #����sshģ���Ƿ����
    def command(self,cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            con_str = ssh.connect(self.ip,self.port,self.username,self.passwd,timeout=5)
            for m in cmd.split(','):
                stdin, stdout, stderr = ssh.exec_command(m)
                out = stdout.readlines()
            for o in out:
                print o,
            #msg = (self.ip) +'\tSSH2 Model is OK\n'
            #log_print(msg)
            ssh.close()
            return True
        except Exception,e:
            log_print(e)
            pass
        return False
if __name__=='__main__':
    cmd = 'df'
    username = "admin"
    passwd = "admin"
    ip = "192.168.22.170"
    print "Begin ssh test......"
    p = ssh2(ip,username,passwd)
    print p.command(cmd)
