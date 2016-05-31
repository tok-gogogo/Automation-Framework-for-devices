import os
import re,shutil
class global_param:
    def param_instead(self,path = 'e:\\ippool.txt'):
        #-----------------------------------------------------------------------------
        # Name:        replace_param
        # param:       path:path of users config file 
        # explain:     redefined the local_param,The content behind the variable substitution
        # Author:      chenzheng
        # 
        # Created:     2013/03/25
        #-----------------------------------------------------------------------
        file = open(path,'r')
        tmplist = []
        #get global params to a tmplist
        line = file.readline()
        pathfilebak = path[0:-4]+'_bak'+path[len(path)-4:len(path)]
        tmpfile = open(pathfilebak,'w')
        readflag = 1
        while len(line) != 0:           
            if line.find('==')!=-1:
                p = re.compile('\s')
                tmpline = p.sub(' ',line)
                list = tmpline.split(' ')             
                for a in list :              
                    if (a=='') or (a==' '):
                        continue
                    tmplist.append(a)
                print tmplist
                tmpfile.write(line)  
                readflag = 0              
            else : readflag = 1              
            i=0
            j=0
            while i<len(tmplist)/3 :
                #tmplist[i] instand to tmplist[i+2]               
                i+=1
                line = line.replace(tmplist[j],tmplist[j+2])
                print line
                j+=3
                print j
            if readflag ==1 : tmpfile.write(line)
            line = file.readline()
        file.close()
        tmpfile.close()
        shutil.copy(pathfilebak,path)
        os.remove(pathfilebak)
'''
if __name__ == "__main__":
    
    g_macro_instead = global_param()
    g_macro_instead.param_instead()
'''
