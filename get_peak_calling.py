# -*- coding:utf-8 -*-
from peak_calling import *
import commands,os,sys,subprocess
def get_peak_call(file):
    try:
        os.remove('NA_peaks.Peak')
    except:
        pass
    try:
        mycallpeak=call_peak()
        mycallpeak.get_count(file)
        lambd=mycallpeak.get_lambda()
        with open('counted_peak.bed') as count_file:
            count_lines=count_file.readlines()
        c=open('NA_peaks.Peak','w')
        number=0
        for count_line in count_lines:  
            count_line_split=count_line.rstrip('\n').split('\t')  
            actual=int(count_line_split[3])    
            actual_number=mycallpeak.get_p_value(actual,lambd)
            if actual_number<=0.0001:
                try:
                    number+=1
                    count_p_line=count_line_split[0]+'\t'+count_line_split[1]+'\t'+count_line_split[2]+'\t'+'NA_peak_%s'%str(number)+'\t'+'0'+'\t'+'.'+'\t'+str(-math.log10(actual_number))+'\t'+'0'+'\t'+'0'+'\n'
                    c.write(count_p_line)
                except:
                    pass  #for a bin has too many reads p will become very little,and -10log10() will say over math domain ,we should drop this number with might be caused by pcr. 
        count_file.close
        os.remove('counted_peak.bed')
        print 'peak calling has been finished,you can get the peak file "NA_peaks.Peak".'
    except:
        print 'your file has something wrong'
    return number
