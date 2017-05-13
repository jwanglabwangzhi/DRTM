# -*- coding:utf-8 -*-
import tensorflow as tf 
import h5py
from tensorflow.python.platform import gfile
import os,sys
path = sys.path[0]
#os.mkdir('%s/model'%path)
def load_data(path):
	f = h5py.File(path,'r')   #h5py是一个压缩数据的包
	sequences = f['train_set_x']
	labels = f['train_set_y']
	return sequences,labels

def split_train_test(xs, ys, test_count=20000):
	return ((xs[test_count:,:,:], ys[test_count:,:]),(xs[:test_count,:,:], ys[:test_count,:]))

def weight_variable(shape):  
	initial = tf.truncated_normal(shape, stddev=0.1)  
	return tf.Variable(initial)  
      
def bias_variable(shape):  
	initial = tf.constant(0.1, shape=shape)  
	return tf.Variable(initial)  
 

def l2norm(Ws):
    return sum(tf.reduce_sum(tf.pow(W, 2)) for W in Ws)


def l1norm(Ws):
    return sum(tf.reduce_sum(tf.abs(W)) for W in Ws) 

x = tf.placeholder("float", shape=[None, 100,4])  
y_ = tf.placeholder("float", shape=[None, 2])
#keep_prob = tf.placeholder("float")  

x_channels = tf.reshape(x, [-1, 100,1,4])
W_1_1=weight_variable([1,1,4,20])
b_1_1=bias_variable([20])
conv1_1=tf.nn.conv2d(x_channels,W_1_1,strides=[1,1,1,1],padding='SAME')
h_conv1_1= tf.nn.relu(conv1_1+b_1_1)
W_conv1 = weight_variable([8, 1, 20, 40])
b_conv1 = bias_variable([40])
conv1 = tf.nn.conv2d(h_conv1_1, W_conv1, strides=[1, 1, 1, 1], padding='VALID')
h_conv1 = tf.nn.relu(conv1+b_conv1)
h_pool1 = tf.nn.avg_pool(h_conv1, ksize=[1, 4, 1, 1], strides=[1, 4, 1, 1], padding='VALID') 
h_pool1_flat=tf.reshape(h_pool1,[-1,40*23])
W_fc1 = weight_variable([40*23, 50])  
b_fc1 = bias_variable([50])     
h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1) 

#h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob) 
W_fc2 = weight_variable([50, 10])  
b_fc2 = bias_variable([10]) 
h_fc2=tf.matmul(h_fc1, W_fc2) + b_fc2
W_fc3 = weight_variable([10, 2])  
b_fc3 = bias_variable([2]) 
 
y=tf.nn.softmax(tf.matmul(h_fc2, W_fc3) + b_fc3) 

'''
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.AdamOptimizer(1e-4,0.01).minimize(cross_entropy)  
'''


error = -tf.reduce_sum(y_*tf.log(y) + (1-y_)*tf.log(1-y))
regularization = 5e-4 * l2norm([W_fc1, W_fc2,W_fc3]) + 1e-3 * l1norm([h_fc1,h_fc2])
loss = error + regularization
train_step = tf.train.RMSPropOptimizer(learning_rate=1e-3, momentum=0.5, decay=8e-5).minimize(loss)
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))  
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float")) 
saver = tf.train.Saver()
sess=tf.Session() 

sess.run(tf.initialize_all_variables())


sequences, labels = load_data('./pre_loaded_data/243768*100*4data.h5')
(train_xs, train_ys), (test_xs, test_ys) = split_train_test(sequences, labels)
step = 0
batch_size = 1000
total_batch = int(len(train_xs) / batch_size)
while step < 5:
	for it in range(total_batch):
		batch_x = train_xs[it * batch_size: it * batch_size + batch_size]
		batch_y = train_ys[it * batch_size: it * batch_size + batch_size]		
		if it %50 == 0:
			sess.run(train_step, feed_dict = {x: batch_x, y_: batch_y})			
			print "loss", sess.run(loss, feed_dict={x: batch_x, y_: batch_y})
			step += 1
			print 'test_loss',sess.run(loss,feed_dict={x:test_xs,y_:test_ys}),'accuracy',sess.run(accuracy,feed_dict={x:test_xs,y_:test_ys})

#tf.train.export_meta_graph(,filename='%s/tmp/my-model.meta'%path)
saver.save(sess, '%s/pre_loaded_data/tmp/my-model.meta'%path)


