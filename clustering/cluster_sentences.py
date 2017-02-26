"""
Sentence Clustering Module

@author: Ruchika Chhabra
"""

#!/usr/bin/python
import re
import os
import csv
import argparse as cmdline
import gensim 
import numpy as np
import sys
from numpy import *
import operator
import shutil

class Clustering():
	'''
	This class has the following functionality:
	1. Find cosine similarity between sentence vectors.
		- If similarity is greater than a threshold value then 
		  sentences are marked as similar otherwise not-similar.
		- Similar sentences constitute a cluster.

	Attributes:
	-----------
	1. embedding_file_path: Path of CSV file, which contains sentences 
	                        to be clustered along with the corresponding 
	                        sentence vector.
	2. output_dir_path    : Path of output directory.
	3. threshold		  : Threshold value to be used for clustering.
	4. representative_vec : Specifies how the representative vector for
							each cluster is to be computer. 
	-add    : Add all the vectors in clusters to find representative 
	          vector.
	-average: Average of all vectors in clusters is to be used for
	   		  computing representative vector.
	5. overlap_cluster	  : If set to False, then no two clusters will 
							have same sentence.
	6. word_vector_dim	  : Dimension of vector corresponding to sentence.
	'''

	def __init__(self, embedding_file_path, output_dir_path, threshold, \
				 representative_vec, overlap_cluster, word_vector_dim):
		'''
		This method is called to create an instance of this class.

        Parameters
        ----------
        embedding_file       : Path of CSV file, which contains sentences 
	                           to be clustered along with the corresponding 
	                           sentence vector.
	    output_dir_path      : Path of output directory.
	    Threshold            : Threshold value to be used for clustering.
	    representative_vec   : Specify whether the representative sentence 
	    					   of each cluster is to be computed using "add"
	    					   or "average" of vectors in cluster.
	    overlap_cluster		 : Specify if overlapping clusters to be generated
	     					   or not.
	    word_vector_dim		 : Dimension of sentence vector.
		'''
		self.embedding_file_path = embedding_file_path
		self.output_dir_path	 = output_dir_path
		self.threshold 			 = threshold
		self.representative_vec  = representative_vec
		self.overlap_cluster	 = overlap_cluster
		self.word_vector_dim	 = word_vector_dim
	
	def find_sentence_similarity(self, sentence1, sentence2):
		'''
		This method finds similarity between two sentence received as arguments.

		Parameters:
		-----------
		1. sentence1 : Row of input CSV file representing sentence 1.
		2. sentence2 : Row of input CSV file representing sentence 2.

		Return Value:
		-------------
		Returns cosine similairty between two input sentence vectors.
		'''

		# Fetch word embedding of Sentence1
		sentence1_vector = np.zeros(int(self.word_vector_dim))
		count = 0
		index = 1

		while count < int(self.word_vector_dim):
			 sentence1_vector[count] = float(sentence1[index])
			 index +=1
			 count +=1

		# Fetch word embedding of Sentence2
		sentence2_vector = np.zeros(int(self.word_vector_dim))
		count = 0
		index = 1
		while count < int(self.word_vector_dim):
			 sentence2_vector[count] = float(sentence2[index])
			 index +=1
			 count +=1

		# Find cosine distance between sentence1_vector and sentence2_vector
		cosine_distance = (np.dot(sentence1_vector,sentence2_vector)\
						  /(np.linalg.norm(sentence1_vector) * \
						  np.linalg.norm(sentence2_vector))) 
		return cosine_distance

	def create_new_cluster(self, number_of_clusters, sentence):
		'''
		This method creates a new cluster.

		Parameters:
		-----------
		1. number_of_clusters: Current number of clusters/
		2. sentence: sentence to be added to new cluster.

		Return Value:
		------------
		Total number of clusters.
		'''
		number_of_clusters = number_of_clusters + 1
		filename = self.output_dir_path + '/cluster_' + str(number_of_clusters) + '.csv'
		self.write_to_csv_file(filename, sentence)
		return number_of_clusters

	def write_to_csv_file(self, filename, row):
		'''
		This method writes given row in given file.

		Parameters:
		----------
		1. filename: file to be written
		2. row: row to be written in file
		'''
		if os.path.exists(filename):
			output_file = open(filename,'ab+')
		else:
			output_file = open(filename,'wb+')
		csv_writer  = csv.writer(output_file)
		csv_writer.writerow(row)
		output_file.close()

	def cluster_sentences(self): 
		'''
		This method involves following functionality:
		1. Read representative sentence of each cluster.
		2. Compare the input sentence with the representative sentence vector 
		   of cluster.
		3. If the sentence similarity is greater than threshold then:
		   Input sentence belong to same cluster as candidate sentence.
		   Otherwise:
		   Input sentence belong to other cluster.
		4. In case input sentence is not similar to any existing cluster then, 
		   a new cluster is created.
		'''
		number_of_clusters = 0
		with open(self.embedding_file_path,'r') as csvinput:
			reader = csv.reader(csvinput) 

			# Create Output Directory if does not exist
			if os.path.exists(self.output_dir_path):
				shutil.rmtree(self.output_dir_path)
			os.mkdir(self.output_dir_path)

			# Read Embedding Input CSV File line by line
			for row in reader:
				if (number_of_clusters == 0):
					# If Number of existing clusters is 0, then create a new cluster
					# for input sentence
					number_of_clusters = self.create_new_cluster(number_of_clusters, row)
				else:
					# If clusters exist, then:
					# - find similarity between input sentence and representative sentence
					#   of each cluster.
					# - if similarity is greater than threshold then add entry in dict.
					#   matched_cluster_dict = {cluster_id = similarity_score}
					matched_cluster_dict = {}
					for subdir, dirs, cluster_files in os.walk(self.output_dir_path):
						for cluster_file in cluster_files:
							if 'rep_' in cluster_file:
								cluster_fh = open(self.output_dir_path + '/' + cluster_file,'r')
								csv_reader = csv.reader(cluster_fh)
								c_row 	   = next(csv_reader)
								similarity_score = self.find_sentence_similarity(row,c_row)
		 
								if (similarity_score > self.threshold): 
									matched_cluster_dict[(cluster_file.split('.')[0])[4:]] = similarity_score
									cluster_fh.close()

					if matched_cluster_dict == {}:
						# If no existing cluster matched input sentence then create a 
						# new cluster.
						number_of_clusters = self.create_new_cluster(number_of_clusters, row)
					else:
						# If there are clusters matching input sentence and cluster overlaping
						# is not allowed, then insert input sentence to the cluster with
						# highest similarity. 
						if not self.overlap_cluster:
							cluster_id = max(matched_cluster_dict.iteritems(), key=operator.itemgetter(1))[0]
							filename   = self.output_dir_path + '/'+ cluster_id + '.csv'
							self.write_to_csv_file(filename, row)
						# If cluster overlapping is allowed then, add input sentence to
						# each of the matched cluster.
						else:
							for cluster_id in matched_cluster_dict.keys():
								filename = self.output_dir_path + '/' + cluster_id + '.csv'
								self.write_to_csv_file(filename, row)
				# Find representative sentence of each cluster
				self.find_representative_sentence(number_of_clusters)
		return number_of_clusters

	def find_representative_sentence(self, number_of_clusters):
		'''
		This method is used to compute representative sentence vector
		of each cluster.
		If self.representative_vec is "add" then:
			All the Vectors of sentences, in given cluster are added to
			find representative sentence vector of given cluster.
		else if self.representative_vec is "average" then:
			All the vectors of sentences, in given cluster are average
			to find representative sentence of given cluster.
		'''
		counter = number_of_clusters
		while counter:
			filename   = self.output_dir_path + '/cluster_' + str(counter) + '.csv'
			read_file  = open(filename,'r')
			csv_reader = csv.reader(read_file)
			vec_sum    = np.zeros(self.word_vector_dim)
			input_vec  = np.zeros(self.word_vector_dim)

			num_rows = 0

			# Find sum and average of all the vectors in a cluster file.
			for row in csv_reader:
				num_rows += 1
				column = 1
				count  = 0
				while count < int(self.word_vector_dim):
					input_vec[count] = row[column]
					column += 1
					count  += 1
				vec_sum = vec_sum + input_vec
			read_file.close()

			vec_avg = vec_sum/num_rows

			# Create a CSV file which contains only the representative vector of the cluster.
			cluster_rep_file  = self.output_dir_path + '/rep_cluster_' + str(counter) + '.csv'
			write_file = open(cluster_rep_file, 'wb+')
			csv_writer = csv.writer(write_file)
			row = ['Representative Vector']
			if self.representative_vec == 'add':
				row.extend(vec_sum)
			else:
				row.extend(vec_avg)
			csv_writer.writerow(row)
			write_file.close()
			counter = counter - 1