"""
Config Reader

@author: Ruchika Chhabra
"""

#!/usr/bin/python
from ConfigParser import ConfigParser
    
class ConfigParse():
    '''
    This class reads config.ini file and sets the required user inputs
    in the class attributes.

    Attributes
    ----------
    1. word2vec_model
    Type: str
    Description: Path of word2vec trained model file.
    Default Value: 'GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin'
    2. threshold
    Type: float
    Description: Threshold value to be used for clustering
    Default Value: 0.80
    3. input_file_path
    Type: str
    Description: Path of input text file containing sentences to be clustered.
    Default Value: None
    4. output_dir_path
    Type: str
    Description: Path of directory where output clusters are to be kept.
    Default Value: output_clusters
    5. cluster_overlap
    Type: bool
    Description: If set to False, then no two clusters will have same sentence.
    Default Value: True
    6. word_vector_dim
    Type: int
    Description: Dimension of word vectors.
    Default Value: 300
    7. representative_word_vector
    Type: str
    Description: Specify whether the representative sentence of each cluster is to be
				 computed using "add" or "average".
    Default Value: average
    '''
    
    def __init__(self):
        '''
        This method declares the class attributes.
        '''
        self.word2vec_model  = 'GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin'
        self.threshold       = 0.80
        self.input_file_path = None
        self.output_dir_path = './output_clusters'
        self.cluster_overlap = True
        self.word_vector_dim = 300
        self.representative_word_vector = 'average'

    def config_reader(self):    
        '''
        This method parses the config file and read the variables defined by
        the user in the config.ini file. The values of the variables are then
        set in the corresponding class attributes.
        '''
        
        parser = ConfigParser()
        # Read config.ini
        parser.read('config.ini')
        
        # Read input variables for the code
        if parser.get('Input Variables','word2vec_model'):
        	self.word2vec_model  = parser.get('Input Variables','word2vec_model')
        if parser.get('Input Variables','threshold'):
        	self.threshold       = parser.getfloat('Input Variables','threshold')
        if parser.get('Input Variables','input_file_path'):
        	self.input_file_path = parser.get('Input Variables','input_file_path')
        if parser.get('Input Variables', 'output_dir_path'):
        	self.output_dir_path = parser.get('Input Variables', 'output_dir_path')
        if parser.get('Input Variables', 'cluster_overlap'):
        	self.cluster_overlap = parser.getboolean('Input Variables', 'cluster_overlap')
        if parser.get('Input Variables', 'word_vector_dim'):
        	self.word_vector_dim = parser.getint('Input Variables', 'word_vector_dim')
        if parser.get('Input Variables', 'representative_word_vector'):
        	self.representative_word_vector = parser.get('Input Variables', 'representative_word_vector')