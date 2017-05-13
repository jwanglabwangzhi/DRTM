# -*- coding:utf-8 -*-
import os


def intersect_summit(file):

    expressed_mirna=open('expressed_intergentic_miRNA.txt')
    expressed_mirna_lines=expressed_mirna.readlines()
    expressed_mirna.close()
    expressed_mirna_set=set()
    for expressed_mirna_line in expressed_mirna_lines:
        expressed_mirna_set.add(expressed_mirna_line.rstrip('\n'))
    with open('./pre_loaded_data/please_inter_mirna_region.bed') as inter_mirna_file:
        inter_mirna_lines=inter_mirna_file.readlines()
    inter_expressed_mirna= open('s.bed','w')
    for inter_mirna_line in inter_mirna_lines:
        if inter_mirna_line.split('\t')[3] in expressed_mirna_set:
            inter_expressed_mirna.write(inter_mirna_line)
    inter_expressed_mirna.close()    
    os.system('bedtools intersect -a %s -b s.bed -wa -wb >a.bed'%file)   #这个地方的s.bed之后也会变成输入参数，变成表达的mirna列表。
    os.system('bedtools sort -i a.bed >b.bed')
    os.remove('a.bed')
    with open('s.bed') as f:
        text=f.read()
    length=len(text.splitlines())
    return length



