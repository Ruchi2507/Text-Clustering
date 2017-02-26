"""
Main Module

@author: Ruchika Chhabra
"""

#!/usr/bin/python
import sys
import os
sys.path.insert(0, './word_embedding')
sys.path.insert(1, './clustering')
from word_embedding import WordEmbedding
from config_reader import ConfigParse
from cluster_sentences import Clustering

class MainExecutor():
	'''
	This class has the following functionality:
	1. Read the configuration settings.
	2. Convert input documents to vectors.
	2. Performs document clustering.
	'''

	def main(self):
		'''
		This is the main function for performing the 
		Document Clustering.
		'''

		# Create object of ConfigParser Class
		config_obj = ConfigParse()
    
		# Parse config file
		print 'READING CONFIG FILE'
		config_obj.config_reader()

		# Create object of WordEmbedding Class
		word_embedding_obj = WordEmbedding(config_obj.input_file_path,
    						 config_obj.word2vec_model,
    						 config_obj.word_vector_dim)

		print 'CONVERTING INPUT SENTENCES TO VECTORS'
		embedding_file = word_embedding_obj.sentence_to_vector()

		# Create object of Clustering Class
		clustering_obj = Clustering(embedding_file, config_obj.output_dir_path,
    					config_obj.threshold, config_obj.representative_word_vector,
    					config_obj.cluster_overlap, config_obj.word_vector_dim)

		print 'CLUSTERING SENTENCES'
		num_of_clusters = clustering_obj.cluster_sentences()
		print str(num_of_clusters) + ' NUMBER OF CLUSTERS ARE GENERATED.'

		# Remove Temporary Files
		os.remove(embedding_file)
		for subdir, dirs, cluster_files in os.walk(config_obj.output_dir_path):
			for cluster_file in cluster_files:
				if 'rep_' in cluster_file:
					os.remove(config_obj.output_dir_path + '/' + cluster_file)

if __name__ == '__main__':
	main_executor_obj = MainExecutor()
	main_executor_obj.main()