#-*- coding: UTF-8 -*-  
"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

import Image
import subprocess

import util
import errors

from PIL import ImageGrab
import pyhk
import os
import sys
import ctypes
import win32gui
import ctypes.wintypes

tesseract_exe_name = 'C:\\Program Files\\Tesseract-OCR\\tesseract' # Name of executable to be called at command line

#tesseract_exe_name = 'E:\\Python_download\\pytesser_v0.0.1\\tesseract' # Name of executable to be called at command line
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation


def capture_fullscreen():
    '''
    Function:È«ÆÁ×¥Í¼
    Input£ºNONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-10
    '''  
    #×¥Í¼   
    pic = ImageGrab.grab()
    
    #±£´æÍ¼Æ¬
    save_pic(pic)
    

def save_pic(pic, filename = 'Î´ÃüÁîÍ¼Æ¬.png'):
    pic.save(filename)
    
def call_tesseract(input_filename, output_filename):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	
	args = [tesseract_exe_name, input_filename, output_filename]
	print' args : ', args
	proc = subprocess.Popen(args)
	retcode = proc.wait()
	if retcode!=0:
		errors.check_for_errors()

def image_to_string(im, cleanup = cleanup_scratch_flag):
	"""Converts im to file, applies tesseract, and fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root)
		text = util.retrieve_text(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text

def image_file_to_string(filename, cleanup = cleanup_scratch_flag, graceful_errors=True):
	"""Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
	converts to compatible format and then applies tesseract.  Fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		try:
			call_tesseract(filename, scratch_text_name_root)
			text = util.retrieve_text(scratch_text_name_root)
		except errors.Tesser_General_Exception:
			if graceful_errors:
				im = Image.open(filename)
				text = image_to_string(im, cleanup)
			else:
				raise
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text
	

if __name__=='__main__':
    im = Image.open('E:\\Python_download\\pytesser_v0.0.1\\phototest.tif')
    text = image_to_string(im)
    print text
    try:
        text = image_file_to_string('E:\\Python_download\\pytesser_v0.0.1\\fnord.tif', graceful_errors=False)
    except errors.Tesser_General_Exception, value:
        print "fnord.tif is incompatible filetype.  Try graceful_errors=True"
        print value
    text = image_file_to_string('E:\\Python_download\\pytesser_v0.0.1\\fnord.tif', graceful_errors=True)
    print "fnord.tif contents:", text
    text = image_file_to_string('E:\\Python_download\\pytesser_v0.0.1\\fonts_test.png', graceful_errors=True)
    print text
    
    text = image_file_to_string('E:\\Python_download\\pytesser_v0.0.1\\ttttt.bmp', graceful_errors=True)
    print "ttttt.bmp\n", text
    
    if text.find('0000')>-1:
        print 'text.find True'
    else :
        print 'text.find False'

