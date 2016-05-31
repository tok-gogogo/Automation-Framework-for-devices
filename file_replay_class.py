import os,os.path,shutil 
def file_Refresh(new_path='E://new',old_path='E://old'):
    #-----------------------------------------------------------------------------
        # Name:        file_Refresh
        # param:       new_path:new folder place old_path:which folder need to replace  
        # explain:     find and replace
        # Author:      chenzheng
        #
        # Created:     2013/03/19
        #-----------------------------------------------------------------------
    if(not os.path.isdir(new_path)): 
        print 'error new_path'
        return 
    if(not os.path.isdir(old_path)):
        print 'error old_path'
        return 
    newfilelist = []
    for root,dirs,files in os.walk(new_path):
        for filespath in files:
            newname = os.path.join(root,filespath)
            newname = newname.split(new_path + '\\')[-1]
            newfilelist.append(newname)
    #print '*****************oldfilelist **********************\n',newfilelist
    oldfilelist = []
    for root,dirs,files in os.walk(old_path):
        for filespath in files:
            oldname = os.path.join(root,filespath)
            oldfilelist.append(oldname)
    #print '*****************oldfilelist **********************\n',oldfilelist
    for newfile in newfilelist :
        for oldfile in oldfilelist :
            if  oldfile.split('\\')[-1].find(newfile)>-1 :
                shutil.copy(new_path+'\\'+newfile,oldfile)
        
'''     
if __name__=='__main__':
    file_Refresh('E:\\test_new','E:\\test_new_old')
'''
        
