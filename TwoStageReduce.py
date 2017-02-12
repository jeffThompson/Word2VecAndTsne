
'''
TWO STAGE REDUCE
Jeff Thompson | 2016-17 | jeffreythompson.org

Loads word2vec model, reduces to N dimensions.

(First, use TrainModel.py to train, then feed into here)

(Then, optionally use TsneToGrid.py to convert to a 2D grid)

OPTIONS
+ Do an initial reduction, best for large data sets
  that would choke on a direct 2D reduction – uses
  PCA from sklearn (much faster than tsne)
+ Keep only N most common words, also helpful for
  large data sets – any count up to 50k allowed

REQUIRES
+ gensim
+ sklearn
+ numpy

TO DO
+ try export 3D data, convert to STL for printing

'''

from gensim import models, matutils					# word2vec model loading
from sklearn.decomposition import IncrementalPCA	# inital reduction
from sklearn.manifold import TSNE 					# final reduction
import numpy as np 									# array handling
import os, warnings


model_filename =    'ModelsAndData/WikipediaDump-POS.model'		# model file to reduce
model_name = 		'WikipediaDump-POS'							# name for exporting files

num_dimensions =     2				# final num dimensions (2D, 3D, etc)

run_init_reduction = True			# run an initial reduction with PCA?
init_dimensions =    20				# initial reduction before t-SNE

# use only most common words (helpful for big data sets)
only_most_common =   True
num_common = 		 50000			# how many words to filter to? (max 50k)

common_filename = 	 'ModelsAndData/50kMostCommonWords.txt'


def normalize_list(vals):
	'''
	normalize a list of vectors to range of -1 to 1
	input: list of vectors
	output: normalized list
	'''
	min_val = float(min(vals))
	max_val = float(max(vals))
	output = []
	for val in vals:
		if val < 0:
			val = (val / min_val) * -1
		elif val > 0:
			val = val / max_val
		output.append(val)			# note if 0, stays the same :)
	return output


# ignore unicode warnings
# (they don't cause any problems, just ugly output from this code)
warnings.filterwarnings('ignore', '.*Unicode.*')


# load existing model from file
print 'loading model...' 
model = models.Word2Vec.load(model_filename)
print '- done'


# load model as numpy array
# if specified, keep only most common words
print 'converting model/words to numpy array...'
if only_most_common:
	print '- loading ' + str(num_common) + ' most common words...'
	most_common = []
	with open(common_filename) as f:
		for i, line in enumerate(f):
			if i > num_common:
				break
			most_common.append(line.strip())

print '- creating list of words/vectors for reduction...'
if only_most_common:
	print '  - keeping only ' + str(num_common) + ' most common words'

vectors= []			# positions in vector space
labels = []			# keep track of words to label our data again later
for word in model.vocab:
	if only_most_common:
		parts = word.split('_')		# split _ for POS-tagged words
		w = parts[0].lower()
		p = parts[1]
		if w in most_common:
			word = w + '_' + p
			try:
				vectors.append(model[word])
				labels.append(word)
			except:
				pass
	else:
		vectors.append(model[word])
		labels.append(word)
print '- found ' + str(len(labels)) + ' entities x ' + str(len(vectors[0])) + ' dimensions'


# convert both lists into numpy vectors for reduction
vectors = np.asarray(vectors)
labels =  np.asarray(labels)
print '- done'


# if specified, reduce using IncrementalPCA first (down 
# to a smaller number of dimensions before the final reduction)
if run_init_reduction:
	print 'reducing to ' + str(init_dimensions) + 'D using IncrementalPCA...'
	ipca = IncrementalPCA(n_components=init_dimensions)
	vectors = ipca.fit_transform(vectors)
	print '- done'

	# save reduced vector space to file
	print '- saving as csv...'
	with open(model_name + '-' + str(init_dimensions) + 'D.csv', 'w') as f:
		for i in range(len(labels)):
			f.write(labels[i] + ',' + ','.join(map(str, vectors[i])) + '\n')


# reduce using t-SNE
print 'reducing to ' + str(num_dimensions) + 'D using t-SNE...'
print '- may take a really, really (really) long time :)'
vectors = np.asarray(vectors)
tsne = TSNE(n_components=num_dimensions, random_state=0)
vectors = tsne.fit_transform(vectors)
print '- done'


# save reduced vector space to file
print 'saving as csv...'
x_vals = [ v[0] for v in vectors ]
y_vals = [ v[1] for v in vectors ]
with open(model_name + '-' + str(num_dimensions) + 'D.csv', 'w') as f:
	for i in range(len(labels)):
		label = labels[i]
		x = x_vals[i]
		y = y_vals[i]
		f.write(label + ',' + str(x) + ',' + str(y) + '\n')
print '- done'


# normalize values -1 to 1, save to file
print 'normalizing position values...'
x_vals = normalize_list(x_vals)
y_vals = normalize_list(y_vals)
print '- saving as csv...'
with open(model_name + '-' + str(num_dimensions) + 'D-NORMALIZED.csv', 'w') as f:
	for i in range(len(labels)):
		label = labels[i]
		x = x_vals[i]
		y = y_vals[i]
		f.write(label + ',' + str(x) + ',' + str(y) + '\n')
print '- done'

