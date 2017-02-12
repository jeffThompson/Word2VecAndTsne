
'''
TAG TEXT FOR TRAINING
Jeff Thompson | 2017 | jeffreythompson.org

Splits text into words and their POS for Word2Vec
training, to keep different senses of the same
word separate in vector space.

Writes the word_POS to keep them together 
when gensim tokenizes the text.

	<word>_<POS> ie: pizza_NN

(Then use TrainModel.py to run the training)

REQUIRES
+ pattern

TO DO
+ how to ignore a unicode warning from pattern?

'''

from pattern.en import parse
import warnings


input_filename =  'ModelsAndData/WikipediaDump.txt'
output_filename = 'ModelsAndData/WikipediaDump-POS.txt'

skip_ahead =       0		# skip ahead in source file?


# ignore unicode warnings
# (they don't cause any problems, just ugly output from this code)
warnings.filterwarnings('ignore', '.*Unicode.*')


# get number of lines in input file
# (used for feedback during parsing later)
print 'getting number of lines in file...'
num_lines = 0
with open(input_filename) as f:
	for line in f:
		num_lines += 1


# parse line-by-line, split into words, get POS for each
print 'parsing text...'
print '- may take a while for large datasets'
with open(input_filename) as f:
	if skip_ahead > 0:
		print '- skipping ahead ' + str(skip_ahead) + ' lines...'
	
	for i, line in enumerate(f):	
		if i < skip_ahead:
			continue
		print '  - line ' + str(i+1) + ' / ' + str(num_lines)
		line = line.strip()
		pos = parse(line).split()[0]
		with open(output_filename, 'a') as out:
			for p in pos:
				try:
					out.write(p[0] + '_' + p[1] + '\n')
				except UnicodeEncodeError:
					pass
print '- done!'

