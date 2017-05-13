# -*- coding:utf-8 -*-
import time
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
import commands,os,sys,subprocess
from intersect_summit import *
import tensorflow as tf 
import numpy as np
from get_top_three import *
from get_cnn_score import *
peak_file=sys.argv[1]      #这个最后用作调用
path = sys.path[0]
number=0
#list_bug=open('bugfile_line.bed','w')
my_top_three_gender=top_three_gender()
my_get_seq_score=get_seq_score()

def seq_translate_list(templet,seq):  
    final_list=[]
    templet=templet.strip()
    seq=seq.strip()
    seq=seq.lower()
    for i in seq:
        for j in templet:
            if i in j:
                final_list.append(1.0)
            else:
                final_list.append(0.0)
    return final_list



def get_mirna_tss(peak_file):
    my_top_three_gender.get_intersect_file(peak_file) 
    subprocess.call('bedtools sort -i first_three_score.bed >sort_first_three_score.bed',shell=True)
    hundred_bp_peak=open('hundred_bp_peak.bed','w')
    set_all_peak=set()
    with open('sort_first_three_score.bed') as sort_first_three_file:
        first_three_lines=sort_first_three_file.readlines()
        for first_three_line in first_three_lines:
            first_three_split=first_three_line.rstrip('\n').split('\t')
            set_all_peak.add(first_three_split[3])
            middle=int((int(first_three_split[1])+int(first_three_split[2]))*0.5)              	
            hundred_bp_peak.write(first_three_split[0]+'\t'+str(middle-50)+'\t'+str(middle+50)+'\t'+first_three_split[3]+'\t'+first_three_split[-2]+'\t'+first_three_split[-1]+'\n')
    hundred_bp_peak.close()
    os.system('bedtools getfasta -fi pre_loaded_data/hg19.fa -bed hundred_bp_peak.bed -s -fo peak_with_fasta.fasta')



    with open('hundred_bp_peak.bed') as hundred_bp_peak:
        hundred_bp_peak_lines=hundred_bp_peak.readlines()


                
    set_peak_have_fasta=set()
    peak_fasta_file=open('peak_with_fasta.fasta')
    peak_fasta_lines=peak_fasta_file.readlines()
    peak_have_seq=open('peak_have_seq.bed','w')
    for peak_fasta_index,peak_fasta_line in enumerate(peak_fasta_lines):
        if peak_fasta_line[0]=='>':
            for hundred_bp_peak_line in hundred_bp_peak_lines:
                hundred_bp_peak_split=hundred_bp_peak_line.rstrip('\n').split('\t')
                if peak_fasta_line.rstrip('\n')=='>'+hundred_bp_peak_split[0]+':'+hundred_bp_peak_split[1]+'-'+hundred_bp_peak_split[2]+'('+hundred_bp_peak_split[-1]+')':
                    peak_have_seq.write(hundred_bp_peak_line.rstrip('\n')+'\t'+peak_fasta_lines[peak_fasta_index+1])
                    set_peak_have_fasta.add(hundred_bp_peak_split[3])
    peak_fasta_file.close()


    set_not_have_fasta=set_all_peak-set_peak_have_fasta



    all_peak_with_sequence=open('all_peak_with_sequence.bed','w')
        #先跟据序列文件的位置信息，把数据回到hundred_bp_peak，再回到sort_first_three_score
    for hundred_bp_peak_line in hundred_bp_peak_lines:
        hundred_bp_peak_split=hundred_bp_peak_line.rstrip('\n').split('\t')
        if hundred_bp_peak_split[3] in set_not_have_fasta:
            all_peak_with_sequence.write(hundred_bp_peak_line.rstrip('\n')+'\t'+'n'*100+'\n')
    peak_have_seq=open('peak_have_seq.bed')
    peak_have_seq_lines=peak_have_seq.readlines()
    for peak_have_seq_line in peak_have_seq_lines:
        all_peak_with_sequence.write(peak_have_seq_line)

    all_peak_with_sequence.close()

    os.remove('first_three_score.bed')
    os.remove('peak_have_seq.bed')
    os.remove('hundred_bp_peak.bed')
    list_a=[]
    with open('all_peak_with_sequence.bed') as all_peak_with_sequence:
        all_peak_with_sequence_lines=all_peak_with_sequence.readlines()
        for all_peak_with_sequence_line in all_peak_with_sequence_lines:
                #下面把所有序列转成one_hot,并计算 
                #print all_peak_with_sequence_line.rstrip('\n').split('\t')[-1].strip('\n')
            list_a.append(seq_translate_list('atcg',all_peak_with_sequence_line.rstrip('\n').split('\t')[-1].strip('\n')))
        #print len(all_peak_with_sequence_lines)
    array_data=np.array(list_a,'float32').reshape(len(all_peak_with_sequence_lines),100,4)
    new_sort_three=open('new_sort_three.bed','w')
    score=my_get_seq_score.get_score(array_data) 

    for peak_score in zip(first_three_lines,score[:,1]):
        new_sort_three.write(peak_score[0].rstrip('\n')+'\t'+str(peak_score[1])+'\n')
        #zip()
        #记得最后把all_peak_with_sequence这个峰的6列的文件转换成sort_first_three_score.bed这种有miRNA的用于最后选择miRNA       

    new_sort_three.close()

    os.remove('all_peak_with_sequence.bed')
    os.remove('s.bed')
    os.remove('peak_with_fasta.fasta')
    os.remove('sort_first_three_score.bed')


try:
    get_mirna_tss(peak_file)
except:
    os.system('python final_net.py')



