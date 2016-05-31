#-*- coding: UTF-8 -*-  
#-----------------------------------------------------------------------------
# Name:        xml_op.py
# Purpose:     
#
# Author:      gongke
#
# Created:     2014/03/21
# RCS-ID:      xml_op use for modify the xml
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------

from xml.dom import minidom
from global_parame import *
import os
import sys
import time
import string
import types
import re
from wtResult import clsWtResult
from public import *
import WtLog
import codecs



class Stc_load(object):
    def __init__(self,xml_unicode='UTF-8'):
        self.xmlfile = ''
        self.xml_unicode=xml_unicode
        if self.xml_unicode=='UTF-8':
            self.xml_unicode_flag =True
        else:
            self.xml_unicode_flag =False
        
    def Modify_xml_unicode(self,filename):
        file_xml = open(file_name,"r").read()
        file_xml = file_xml.replace('<?xml version="1.0" encoding="gbk"?>','<?xml version="1.0" encoding="utf-8"?>')
        file_xml = unicode(file_xml,encoding='gbk').encode('utf-8')
        
        #xmldoc  = minidoc.parseString(file_xml)
        
    
    