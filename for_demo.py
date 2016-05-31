#-----------------------------------------------------------------------------
# Name:        for_demo.py
# Purpose:     change strings with a loop 
#
# Author:      <gongke>
#
# Created:     2013/03/18
# RCS-ID:      $Id: for_demo.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
def for_demo(filename,resultFilename,param_list,times):
    fileHandle=open(filename,"r")
    fileList=fileHandle.read()
    fileHandle.close()
    resultFile=open(resultFilename,"w")
    result=fileList
    resultFile.write(result+'\r') 
    
    for m in range(1,times+1):
        for line in param_list : 
            param1= line[0]
            param2= line[1]
            param3= line[2]
            param4= line[3] 
            length= line[4]
            pos=result.find(param1)
            while pos !=-1:
                result = result[0:pos]+param2+str(param3+m*param4)+result[pos+length:]
                pos=result.find(param1)
        resultFile.write(result+'\r')    
        result=fileList   
    resultFile.close()

#-----------------------------------------------------------------------------
# param_list:        param1:string that you want to change.
#                    param2:the string part of the changed strings,can't be ''.
#                    param3:the numeric part of the changed strings,can be ''.
#                    param4:increment each loop ,can be ''.
#                    length:the character numbers of the string. 
#filename:           the original file
#resultFilename:     the result file
#times:              loop times 
#-----------------------------------------------------------------------------
'''
if __name__=='__main__':
    param_list=[('ap1','ap',1,2,3),(' 10',' ',10,2,3),('QZWLAN-AC-MASTER-113','BNOS','','',20)]
    for_demo("e:\\ippool.txt","e:\\result_ippool.txt",param_list,3)
'''