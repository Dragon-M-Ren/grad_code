import tensorflow as tf
from .layer_utils import *

class BaseLayer(object):
    def __init__(self,
                 input_dim, output_dim,
                 activation_func,
                 name,
                 dropout_prob = None,
                 bias = False,
                 sparse = False
                 ):
        #Initialize some variables
        self.name = name
        self.activation_func = activation_func
        self.dropout_prob = dropout_prob
        self.bias = bias
        self.sparse = sparse


        #If dropout_prob is assigned a value
        if self.dropout_prob:
            #Check if the type of dropout_prob is legal
            if type(self.dropout_prob) is type(1.0):
                pass
            else:
                print("droupout_prob is: ", self.dropout_prob)
                raise Exception('Invalid type for dropout.')

            #Check if the value is legal
            if 0.0 < self.dropout_prob < 1.0:
                pass
            else:
                print("droupout_prob is: ", self.dropout_prob)
                raise Exception('Invalid value for droupout.')
            

    #This function is invocked by the object name
    def __call__(self, inputs):
        with tf.name_scope(self.name):   
            return self.run(inputs)
    
    def run(self, inputs):
        '''
        Run the layers
        This will bulid the graph
        This function will connect the prev layer's output as input
        Then provide current layer's output as return value
        '''
        raise NotImplementedError

class GraphConvLayer(BaseLayer):
    '''
    Two layer GCN
    Semi-Supervised Classfication with Graph Convolution Networks, Kipf
    Model:
        Z = f(X, A) = softmax(A RELU(AXW(0))W(1))
    A = D^-0.5 L D^-0.5 (Renomalized Laplacian)
    X is the feature matrix
    NOTE: There is no bias or dropout in the orgin model
    
    '''
    def __init__(self,
                 adjancy,
                 input_dim, output_dim,
                 activation_func,
                 name,
                 dropout_prob = None,
                 bias = False,
                 sparse = False):
        super(GraphConvLayer, self).__init__(
                                            input_dim, output_dim,
                                            activation_func,
                                            name,
                                            dropout_prob,
                                            bias,
                                            sparse
                                            )
        self.adjancy = adjancy
        
        #Define layers' variable
        with tf.variable_scope(self.name + '_var'):
            self.weights = glort_init([input_dim, output_dim], name = 'weights')
        
        #If bias is used
            if self.bias:
                self.bias = zeros_inin([output_dim], name = 'bias')
    
    def run(self, inputs):
        '''
        Inputs are features, Since the feateure map will change through the network
        The symmertic normalized Laplacian matrix at the first layer
        Then the convoluted matrix in the following layers
        '''
        if not self.dropout_prob:
            pass

        else:
            if self.sparse:
                inputs = sparse_dropout(inputs, 1 - self.droupout_prob)
            else:
                x = tf.nn.dropout(inputs, 1 - self.dropout_prob)
        
        #Do convolution
        output = graph_conv(inputs, self.adjancy, self.weights, self.sparse)

        #bias
        if self.bias != None:
            output += self.bias

        #activation
        return self.activation_func(output)

        


