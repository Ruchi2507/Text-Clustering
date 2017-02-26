# Text-Clustering
Text Clustering: Used to cluster sentences using modified k-means clustering algorithm.

Advantage: User need not to specify the number of output clusters required.
Algorithm, will create clusters depending on the percentage of similairty between the sentences.

# Requirements:
- Python: 2.7.8
- gensim: 1.0.0

# Execution:
1. Change to the source package "Text-clustering".
2. Open and edit the config.ini with the desired inputs as specified below:
	1. word2vec_model: 
	   - Specify path of word2vec pre-trained model file (in bin format) which is 
	     to be used for converting sentence to vectors.
	   - Currently Google-news-pretrained vector model of dimension 300 is used.
	2. threshold:
	   - Threshold value to be used for clustering. 
	   - If similarity score of 2 sentences is greater that this threshold, 
	     then they are considered similar other different sentences.
	   - Default threshold value is 0.80
	3. input_file_path:
	   - Path of input text file, containing sentences to be clustered.
	4. output_dir_path:
	   - Path of directory, where output_clusters are to be generated.
	   - Default value is './output_clusters'
	5. cluster_overlap:
	   - Specified whether Cluster Overlapping is allowed or not.
       - If set to True, then a sentence can be present in more than 1 cluster.
       - If set to False, then a sentence can be present only in 1 cluster.
	   - Default value is: True
	6. word_vector_dim:
	   - Dimension of vector used for representing each input sentence.
	   - Default value is 300.
	   NOTE: if word_vector_dim is changed then corresponding word2vec trained model
	   is to be used.
	7. representative_word_vector:
	   - Specifies how Representation vector for each cluster is to be computed.
       - If "add": Representation vector for each cluster is computed by adding
	     all sentence vectors in a cluster.
       - If "average": Representation vector for each cluster is computed by
	     average of all the sentence vectors in a cluster.
	   - Default value is 'average'.
3. Once config.ini file is updated, execute text-clustering project by using below command:
	- $ python main_executor.py
