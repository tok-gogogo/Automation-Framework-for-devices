import os, os.path, sys
import win32process,win32event
import subprocess

class do_win_exec:
    def __init__(self,FILEPATH=None):
        self.filepath = FILEPATH
        self.running = False
        
    
    def sub_return_exec(self,FILEPATH=None):
        if FILEPATH==None:
            FILEPATH = self.filepath
        else:
            self.filepath = FILEPATH
        '''
        exe_path = os.path.dirname(FILEPATH)
        print "sub_do_exe111111111 ",FILEPATH
        exe_file = FILEPATH.split('\\')[-1]
        print "sub_do_exe " ,exe_path,exe_file
        os.chdir(exe_path)
        '''
        try:
            self.running = subprocess.call(FILEPATH)
            #self.running = True
        except Exception, e:
            print "Create Error!"
            handle  = None
            self.running = False
            
        
    def sub_ac_upgrade_exec(self,FILEPATH=None):
        
        
        if FILEPATH==None:
            FILEPATH = self.filepath
        else:
            self.filepath = FILEPATH
        '''
        exe_path = os.path.dirname(FILEPATH)
        print "sub_do_exe111111111 ",FILEPATH
        exe_file = FILEPATH.split('\\')[-1]
        print "sub_do_exe " ,exe_path,exe_file
        os.chdir(exe_path)
        '''
        try:
            subprocess.Popen(FILEPATH)
            self.running = True
        except Exception, e:
            print "Create Error!"
            handle  = None
            self.running = False
        
    def sub_do_exe(self,FILEPATH=None):
        
        
        if FILEPATH==None:
            FILEPATH = self.filepath
        else:
            self.filepath = FILEPATH
       
        exe_path = os.path.dirname(FILEPATH)
        exe_file = FILEPATH.split('\\')[-1]
        
        tmp_path = exe_path.split('  ')[0]
        if os.path.isdir(tmp_path) == False:
            os.chdir(os.path.split(tmp_path)[0])
        else:
            os.chdir(exe_path)
        try:
            subprocess.Popen(exe_file)
            self.running = True
        except Exception, e:
            print "Create Error!"
            handle  = None
            self.running = False
        
    def result(self):
        info = ''
        if self.running:
            info = self.filepath  + ' start ok'
        else:
            info = self.filepath  + ' start fail'
        print info
        return info 
    
    
    
    def do_createprocess_exe(self,FILEPATH=None):
        if FILEPATH==None:
            FILEPATH = self.filepath
        exe_path = os.path.dirname(FILEPATH)
        exe_file = FILEPATH.split('\\')[-1]
        os.chdir(exe_path)
        try:
            handle = win32process.CreateProcess(
                os.path.join(exe_path, exe_file),
                '', None, None, 0,
                win32process.CREATE_NO_WINDOW,
                None ,
                exe_path,
                win32process.STARTUPINFO())
            self.running = True
        
        except Exception, e:
            print "Create Error!"
            handle  = None
            self.running = False
        '''    
        while self.running :
            rc = win32event.WaitForSingleObject(handle[0], 1000)
            if rc == win32event.WAIT_OBJECT_0:
                self.running = False
        '''
        print "GoodBye"
'''   
if __name__ == "__main__":  
    test_path ="E:\\ap_moniqi\\apSimulation.exe  -0"
    test = do_win_exec(test_path)
    #test.do_exe()
    test.sub_do_exe()
    test.result()
    if test.running:
        print "*********start ok ***********"
    else:
        print "*********start fail ***********"
'''