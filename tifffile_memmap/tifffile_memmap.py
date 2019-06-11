# this is a code snippet posted by Chris Gohlke here:
# https://forum.image.sc/t/create-tif-with-4-channels-per-pixel/26457/9


import tifffile

# memory-map the ir values in the TIFF file
ir = tifffile.memmap('vs_demo.tif')[..., 3]

# process the ir array in-place or write processing results to ir array
#...

# write any changes in the array back to the TIFF file
ir.flush()

