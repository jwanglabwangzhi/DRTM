# -*- coding:utf-8 -*-
import time
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
import commands,os,sys
from intersect_summit import *
import tensorflow as tf 
import numpy as np
path = sys.path[0]
number=0




class get_seq_score:
    def __init__(self):
        pass

    def get_score(self,array_data):
        #list_a=[]
        #list_a.append(get_seq_score.seq_translate_list(self,'atcg',seq.rstrip('\n')))
        #array_data=np.array(list_a,dtype='float32').reshape(1,len(seq.rstrip('\n')),4)
	    #print array_data
        x_channels = tf.reshape(array_data, [-1, 100,1,4])
        sess = tf.Session()
        new_saver = tf.train.import_meta_graph('%s/pre_loaded_data/tmp/my-model.meta.meta'%path)
        new_saver.restore(sess, tf.train.latest_checkpoint('./pre_loaded_data/tmp/'))
        all_vars = tf.trainable_variables()
        print len(all_vars)
        conv1_1=tf.nn.conv2d(x_channels,all_vars[0],strides=[1,1,1,1],padding='SAME')
        conv1 = tf.nn.conv2d(conv1_1, all_vars[1], strides=[1, 1, 1, 1], padding='VALID')
        h_conv1 = tf.nn.relu(conv1+all_vars[2])
        h_pool1 = tf.nn.avg_pool(h_conv1, ksize=[1, 4, 1, 1], strides=[1, 4, 1, 1], padding='VALID') 
        h_pool1_flat=tf.reshape(h_pool1,[-1,40*23])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, all_vars[3]) + all_vars[4]) 
        h_fc2=tf.matmul(h_fc1, all_vars[5]) + all_vars[6]
        y=tf.nn.softmax(tf.matmul(h_fc2, all_vars[7]) + all_vars[8]) 
        return sess.run(y)







	
