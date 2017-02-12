
'''
TRAIN MODEL
Jeff Thompson | 2016-17 | jeffreythompson.org

Takes a text file, trains it into a word2vec model.

(Then use TwoStageReduce.py to reduce to 2D)

REQUIRES
+ gensim

'''

from gensim import models, matutils


input_filename =  'ModelsAndData/WikipediaDump-POS.txt'		# file of text to train on
model_filename =  'ModelsAndData/WikipediaDump-POS.model'	# name for saving trained model

# train using skip-gram?
# (ignore unless you wanna do detailed tweaking)
skip_gram = 	  False


# create vocabulary
print 'building vocabulary...'
model = models.Word2Vec()
sentences = models.word2vec.LineSentence(input_filename)
model.build_vocab(sentences)


# train model
print 'training model...'
if skip_gram:
	model.train(sentences, sg=1)
else:
	model.train(sentences)


# and save
print '- saving model...'
model.save(model_filename)

# bye
print 'all done, whew!'

