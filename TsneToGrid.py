
'''
TSNE TO GRID
Jeff Thompson | 2017 | jeffreythompson.org

Converts a 2D tsne embedding to a uniform grid using the
rasterfairy library. Saves out to new CSV file.

Rasterfairy code usage adapted from this example:
https://github.com/Quasimondo/RasterFairy/blob/master/
examples/Raster%20Fairy%20Demo%201.ipynb

REQUIRES
+ rasterfairy
+ sklearn
+ numpy

'''

import numpy as np
from lib import rasterfairy
from sklearn.manifold import TSNE


input_filename =  'WikipediaDump-POS-2D-NORMALIZED.csv'
output_filename = 'WikipediaDump-POS-2D-NORMALIZED-GRID.csv'

skip_header = 	   False		# if csv has a header, skip it


# load 2D tsne data
print 'loading tsne data...'
labels = []
points = []
header = None
with open(input_filename) as f:
	for i, line in enumerate(f):
		if i == 0 and skip_header:
			header = line
			continue
		data = line.split(',')
		syllable = data[0]
		x = float(data[1])
		y = float(data[2])
		labels.append(syllable)
		points.append([x,y])
print '- found ' + str(len(labels)) + ' unique words'


# convert to tsne object and grid it
print 'reformatting into a grid...'
xy = TSNE().fit_transform(points)
arrangements = rasterfairy.getRectArrangements(len(labels))
grid_xy, (width, height) = rasterfairy.transformPointCloud2D(xy)
print '- grid dimensions: ' + str(width) + ' x ' + str(height)
print '- done'


# write out grid data to file
print 'saving to file...'
data = zip(labels, grid_xy)
with open(output_filename, 'w') as f:
	if header is not None:				# put back csv header, if there was one
		f.write(header)
	for label, point in data:
		f.write(label + ',' + str(int(point[0])) + ',' + str(int(point[1])) + '\n')
print '- done!'

