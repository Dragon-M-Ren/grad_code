'''
This script is used to debug te model
Write the code in a new file to test the models
'''

import tensorflow as tf
from load_data import create_input
from utils import *
from model.gcn import GCN
from model.mlp import MLP

learning_rate = 0.01
epochs = 4000
weight_decay = 5e-1
early_stopping = 500
activation_func = tf.nn.relu
dropout_prob = 0.5
bias = True
hidden_dim = 16
optimizer = tf.train.AdamOptimizer

directed, undirected, features, y_train, y_val, y_test, train_mask, val_mask, test_mask,\
info = create_input('./data', 'citeseer', 1, 230, 500, None)

#preprocess the adjancy matrix for GCN
sys_norm_directed = symmetric_normalized_laplacian(directed)
sys_norm_undirected = symmetric_normalized_laplacian(undirected)

#preprocess features
norm_features = row_normalized(features)

#information
nodes = directed.shape[0]
input_dim = features.shape[1]
output_dim = y_train.shape[1]

directed = create_load_sparse(directed)
undirected = create_load_sparse(undirected)
features = create_load_sparse(features)


#Dropout for input
print(len(directed[1]))
random_tensor = 1- dropout_prob
random_tensor += tf.random_uniform([len(directed[1])])
dropout_mask = tf.cast(tf.floor(random_tensor), dtype=tf.bool)
print(directed)
#pre_out = tf.sparse_retain(list(directed), dropout_mask)

#directed = pre_out * (1./(1- dropout_prob))


#Create model
model = GCN(
    hidden_num = 1, hidden_dim = [hidden_dim],
    input_dim = input_dim, output_dim = output_dim,
    node_num = nodes, cate_num = output_dim,
    learning_rate = learning_rate, epochs = epochs,
    weight_decay = weight_decay, early_stopping = early_stopping,
    activation_func = activation_func,
    dropout_prob = dropout_prob,
    bias = bias,
    optimizer = optimizer,
    name='GCN'
)

sess = tf.Session()

model.train(sess, undirected, features, y_train, y_val, train_mask, val_mask)


accu = model.test(sess, undirected, features, y_test, test_mask)
print('test acucracy: ', accu)
'''

#Create model
model = MLP(
    hidden_num = 1, hidden_dim = [32],
    input_dim = input_dim, output_dim = output_dim,
    node_num = nodes, cate_num = output_dim,
    learning_rate = learning_rate, epochs = epochs,
    weight_decay = weight_decay, early_stopping = early_stopping,
    activation_func = activation_func,
    dropout_prob = dropout_prob,
    bias = bias,
    optimizer = optimizer,
    name='MLP'
)

sess = tf.Session()

model.train(sess, directed, features, y_train, y_val, train_mask, val_mask)


accu = model.test(sess, directed, features, y_test, test_mask)
print('test acucracy: ', accu)
'''