'''
Created on 2013Äê12ÔÂ20ÈÕ

@author: ZHANGDONG
'''

import gtk, gobject, logging, sys,os,re,time,string
from win_exec import *
from public import *
from wtResult import clsWtResult

class Java_Gui:
    def __init__(self):
        self.model = gtk.ListStore(gobject.TYPE_STRING)
        self.nameEntry = gtk.Entry()
        self.buttons = []
        
    
    def getWindons(self):
        command = 'D:\\CYEMS\\client\\start.bat'
        dir = os.path.dirname(command)
        os.chdir(dir)
        os.popen(command).read()
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        return win
    def run(self):
        self.getWindons()

if __name__ == "__main__": 
    program = Java_Gui()
    print program.run()