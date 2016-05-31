#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        telnet_class.py
# Purpose:     telnet class of users
#
# Author:      gongke
#
# Created:     2013/01/13
# RCS-ID:      $Id: telnet_class.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
import time   
import sys
import string
import telnetlib
import re
import socket
from public import *
import os

reload(sys)
sys.setdefaultencoding("utf-8")

class  pthread_cls:
    def __init__(self):
        self.m = 0
    
    