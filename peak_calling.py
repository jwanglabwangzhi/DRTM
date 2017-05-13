# -*- coding:utf-8 -*-
import os
import math
class call_peak:
    def init(self):
        pass
    def get_count(self,file_name):
        os.system('bedtools bamtobed -i %s> peak.bed'%file_name)
        os.system('bedtools sort -i peak.bed > sorted_peak.bed')
        os.system('bedtools intersect -a ./pre_loaded_data/sorted_hg19_windows_100bp.bed -b sorted_peak.bed -c -sorted > counted_peak.bed')
        os.remove('peak.bed')
        os.remove('sorted_peak.bed')

    def get_lambda(self):
        with open('counted_peak.bed') as count_file1:
            count_lines1=count_file1.readlines()
        count_lines_length=len(count_lines1)
        count_number=0
        for count_line1 in count_lines1:
            count_line_split1=count_line1.rstrip('\n').split('\t')
            count_number+=float(count_line_split1[3])
        avg_count_number=count_number/count_lines_length
        return avg_count_number

    def get_p_value(self,actual,lambd):
        p=math.exp(-lambd)
        for i in xrange(actual):
            p*=lambd
            p/=i+1
        return p
        

