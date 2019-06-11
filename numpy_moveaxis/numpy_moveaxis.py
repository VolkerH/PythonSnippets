# code snippet demonstrating use of np.moveaxis
# posted by Chris Gohlke to the image.sc forum
# https://forum.image.sc/t/create-tif-with-4-channels-per-pixel/26457/9


import numpy
import tifffile

# read interleaved RGB+extrasample channels from TIFF into separate arrays
im = tifffile.imread('vs_demo.tif')
r, g, b, ir = numpy.moveaxis(im, -1, 0)

# process arrays; make sure not to change the data type
...

# save arrays as interleaved RGB+extrasample TIFF
im = numpy.moveaxis([r, g, b, ir], 0, -1)
tifffile.imwrite('vs_demo.out.tif', im, photometric='rgb',
                 planarconfig='contig', extrasamples='unspecified',
                 rowsperstrip=6, metadata=None)