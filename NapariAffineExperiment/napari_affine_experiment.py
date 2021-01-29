
# quick experiment 
# using affine in napari to load and arrange tiles from a gridscan
import collections
from os import getuid
import numpy as np
from pathlib import Path
import tifffile
import napari
 
# for testing and to conserve memory (set to None if all)
n_images = 30 

# layout and distances
nrows=9 # (these tiles are coming in with rows increasing fastest)
shift_vert = 1637.16
shift_horiz = 1630.68

# input and channel selection
basefolder = Path("/home/hilsenst/Desktop/NStim_0.3_1/PreMaldi_D3_NStim_0.3_1")
files = sorted(list(basefolder.glob("Seq*.tif")))
print(files)
if n_images is None:
    n_images = len(files)
imgs = list(map(tifffile.imread, files[:n_images]))
imgs = map(lambda im: im[0,...], imgs)

# setup basic transforms
affine_vert = np.eye(3)
affine_vert[0,2] = shift_vert

affine_horiz = np.eye(3)
affine_horiz[1,2] = 1630.68

# for cycling through colors for tiles, not used anymore
colormap = ['red', 'green','blue']   

with  napari.gui_qt():
    v = napari.Viewer()
    for i, img in enumerate(imgs):
        ny = i % nrows
        nx = int(i/nrows) 
        transform = np.eye(3)
        for _ in range(ny):
            transform = affine_vert @ transform
        for _ in range(nx):
            transform = affine_horiz @ transform
        v.add_image(img.T, affine=transform, opacity=0.8, name = f'nx:{nx}, ny:{ny}, i:{i}') 
