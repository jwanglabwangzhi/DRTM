# -*- coding:utf-8 -*-
import os
import math
from intersect_summit import *

#print file_name
class top_three_gender:
    def __init__(self):
        pass
    def get_intersect_file(self,file_name):
        expressed_mirna_number=intersect_summit(file_name) # 只需要一个peak文件，就可以产生一个交集文件
        with open('b.bed') as bfile:
            file_lines=bfile.readlines()
            length=len(file_lines)
            print 'there are %d peak in the region'%length
            intersect_set=set()
            for file_line in file_lines:
                intersect_set.add(file_line.split('\t')[-3])
            print 'there are %d miRNA has peak'%len(intersect_set)
            express_peak_rate=len(intersect_set)/float(expressed_mirna_number)
            print express_peak_rate
            if express_peak_rate<0.7:
                print 'only %d expressed miRNA has peak in their region,you need to find more peaks by other algorithm or do your chip-seq again'%express_peak_rate
            else:
                top_three_gender.call_tss(self)
        
    def call_tss(self):
        with open('b.bed') as bfile:
            file_lines=bfile.readlines()
            intersect_set=set()
            for file_line in file_lines:
                intersect_set.add(file_line.split('\t')[-3])
            peak_site_score=open('c.bed','w')
            for mirna_name in intersect_set:
                for file_line in file_lines:
                    file_line_split=file_line.rstrip('\n').rstrip('\r').split('\t')
                    if file_line_split[-3]==mirna_name:
                        if file_line_split[-1]=='+':
                            distance=str(int(file_line_split[-4])-int(file_line_split[2]))
                            file_new_line=file_line_split[-3]+'\t'+distance+'\t'+file_line_split[6]+'\t'+file_line_split[7]+'\t'+file_line_split[8]+'\n'
                            peak_site_score.write(file_new_line)
                        else:
                            distance=str(int(file_line_split[1])-int(file_line_split[-5]))
                            file_new_line=file_line_split[-3]+'\t'+distance+'\t'+file_line_split[6]+'\t'+file_line_split[7]+'\t'+file_line_split[8]+'\n'
                            peak_site_score.write(file_new_line)
            peak_site_score.close()
            dic6={}
            dic7={}
            
            for mirna_name in intersect_set: 
                with open('c.bed') as score_file:
                    score_lines=score_file.readlines()
                    for score_line in score_lines:
                        score_line_split=score_line.rstrip('\n').rstrip('\r').split('\t')
                        if len(score_line_split)<>5:
                            print score_line
                        if score_line_split[0]==mirna_name:
                            dic6.setdefault(score_line_split[0],[]).append(float(score_line_split[2]))
            for h in dic6.keys():
                if len(dic6[h])>=3:
                    #print sorted(dic6[h],reverse=True)[0],sorted(dic6[h],reverse=True)[1],sorted(dic6[h],reverse=True)[2]
                    dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[0]))
                    dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[1]))
                    dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[2]))
                else:
                    if len(dic6[h])==2:
                        dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[0]))
                        dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[1]))
                    else:
                        dic7.setdefault(h,[]).append(float(sorted(dic6[h],reverse=True)[0]))

            d=open('first_three.bed','w')
            for hh in dic7.keys():
                for hhh in dic7[hh]:
                    d.write(str(hhh)+'\t'+hh+'\n') 
            d.close()

        top_three_gender.get_first_three(self)
                
    def get_first_three(self):
        first_three=open('first_three_score.bed','w')
        with open('first_three.bed') as ffile:
            ffile_lines=ffile.readlines()
        mirna_set=set()
        with open('b.bed') as b_file:
            b_file_lines=b_file.readlines()
                        
        for ffile_line in ffile_lines:
            ffile_split=ffile_line.rstrip('\n').split('\t')
            for b_file_line in b_file_lines:
                b_file_split=b_file_line.rstrip('\n').split('\t')
                if b_file_split[-3]+b_file_split[6]==ffile_split[1]+ffile_split[0]:
			        first_three.write(b_file_line)
        first_three.close
        os.remove('b.bed')
        os.remove('c.bed')
        os.remove('first_three.bed')
