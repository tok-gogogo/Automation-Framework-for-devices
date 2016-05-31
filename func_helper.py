import re,shutil,os
#encoding=gbk
class fixfunc:    
    def fix_formal_param(self,func_file='e://func_file.txt',user_file='e://ippool.txt'):
        #get a table from func_file
        dictionary = self.get_func_dic(func_file)        
        fixfile = open(user_file,'r')
        line = fixfile.readline()
        p = re.compile('\s')
        pathfilebak = user_file[0:-4]+'_bak'+user_file[len(user_file)-4:len(user_file)]
        tmpfile = open(pathfilebak,'w')
        while len(line)!=0:
            if line.find('****')!=-1:
                while 1:
                    tmpfile.write(line)
                    line = fixfile.readline()
                    if line.find('****')!=-1:
                        break
            if line.find('$')!=-1:                
                tmpline = p.sub('',line)
                tmplist = tmpline.split('$')
                if dictionary.has_key(tmplist[0]) == 1:
                    line = self.fix_prama(dictionary,line,tmplist)
            elif line.find('==')==-1 and line.find('#')==-1 and line.find('****')==-1 :
                if line.strip()!='':
                    line = '#注释 format error here:' + line
            tmpfile.write(line)
            line = fixfile.readline()
        fixfile.close()
        tmpfile.close()
        
        shutil.copy(pathfilebak,user_file)
        os.remove(pathfilebak)
        
    def fix_prama(self,dic,line,tmplist):
        #length of user cmd param 
        src_func = len(tmplist[1].split(','))
        #function table get params count
        dst_func = int(dic[tmplist[0]].split('__')[-1])
        if src_func == dst_func:
            return line
        elif src_func > dst_func:
            line = "注释：有多余参数"+line
            return line 
        else:
            if line.find('=')==-1:
                line = "注释：缺少参数"+line
                return line
            else:
                #fix function params
                list_src = tmplist[1].split(',')
                list_dst = dic[tmplist[0]].split(',')                
                i = 0
                tmpline = ''
                dic_src = {}
                while i<src_func:
                    if list_src[i].find('=')!=-1:
                        dic_src[list_src[i].split('=')[0]] = list_src[i].split('=')[1]
                    i += 1
                i = 0
                while i<dst_func:
                    dic_dst = {}
                    if list_dst[i].find('=')==-1:
                        tmpline = tmpline + '  ,' + list_src[i] 
                    else:
                        dic_dst[list_dst[i].split('=')[0]] = list_dst[i].split('=')[1]
                        try :
                            dic_dst[list_dst[i].split('=')[0]] = dic_src[list_dst[i].split('=')[0]]
                            tmpline = tmpline + '  ,' + dic_dst[list_dst[i].split('=')[0]]
                        except:
                            tmpline = tmpline + '  ,' + dic_dst[list_dst[i].split('=')[0]]
                    i+=1
                #print line.split('$')[1]
                line = line.split('$')[0] + '$' +'\t\t\t\t\t' + tmpline[3:] +'\n'             
        return line
    def get_func_dic(self,func_file):
        file_table = open(func_file,'r')
        dictionary = {}
        table = file_table.readline()
        #get a dictionary :  key is function name ; value is a params tuple
        while len(table)!=0:
            #func = re.findall('\(.*\)',table)
            key = table.split('(')[0]            
            s = str(len(table.split('(')[1].split(')')[0].split(',')))
            func = table.split('(')[1].split(')')[0] + ',__param__'+s
            dictionary[key]=func
            table = file_table.readline()
        file_table.close()
        return dictionary
    def add_func_table(self,str,func_file='e:\\func_file.txt'):
        
        
    #formal of str : As well as the function declaration
        addstr = str.split('(')[0]
        file = open(func_file,'r')
        pathfilebak = func_file[0:-4]+'_bak'+func_file[len(func_file)-4:len(func_file)]
        addflag = 1         
        tmpfile = open(pathfilebak,'w')
        line = file.readline() 
        while len(line)!=0:
            if addstr==line.split('(')[0]:
                line = str+'\n'
                addflag = 0
            tmpfile.write(line)
            line = file.readline()
        file.close()
        tmpfile.close()
        if addflag ==1: 
            file = open(func_file,'a+')
            str = str+'\n'
            file.write(str)
            file.close()
        else:
            file.close()          
            shutil.copy(pathfilebak,func_file)
        os.remove(pathfilebak)
        
'''      
if __name__=='__main__':
     
    fix_table = fixfunc()
    #fix_table.add_func_table('LaunchVugen(ExePath,ScriptPath)')
    #fix_table.add_func_table('Launch(ExePath,ScriptPath)')
    fix_table.fix_formal_param()
'''
     
