 
#-----------------------------------------------------------------------------
# Name:        WtLog.py
# Purpose:     write log informatin at a file.log file is create at folder of tool(or Module)
# format is:[DATE TIME NO TYPEMARK INFOMATION ]-2013-01-23 20:12:33,812 INFO 456
#
# Author:      <your name>
#
# Created:     2013/01/23
# RCS-ID:      $Id: WtLog.py $
# Copyright:   (c) 2006
# Licence:     <0.0.1>
#-----------------------------------------------------------------------------
#<0.0.2> 2013/02/28 modify repeat write log. 

LOG = 0 #LOG is an object.
g_bShowScreen = False
import logging 
import os
import sys 
from logging import handlers   

#init Logging obj -LOG
def log_public(s,LogPath='AutoTestLog.log'):
    global g_bShowScreen
    global LOG
    if (os.path.isfile(LogPath))==False:
        path1 = os.path.abspath(sys.argv[0])
        filepath = os.path.dirname(path1)
        LogPath = filepath + "\\AutoTestLog.log"
        f=open(LogPath,'a')
        f.close()
    
    #create log object
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
    
    
    
    
    #create handler,create Screan show
    if g_bShowScreen == True:  
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)               
        LOG.addHandler(streamhandler) 
        
    #write log informain
    LOG.info(s)
    LOG.removeHandler(handler)
    #create handler,create Screan show    
    if g_bShowScreen == True:
        LOG.removeHandler(streamhandler)
        
def enableToScreen():
    global g_bShowScreen
    g_bShowScreen = True
    
def disenableToScreen():
    global g_bShowScreen
    g_bShowScreen = False
    
        
if __name__ =="__main__":
    path = "D:\6_wtLog\AutoTestLog.log"
    s={1:{'1':'a'}}
    
    log_public("1")
    log_public("2")
    log_public("3")
    log_public("4")
    log_public("5")
    log_public(s)        