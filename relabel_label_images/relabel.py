import numpy as np

def relabel_unique(label_in):
    """ relabels a label image with the unique labels
    being renumbered in consecutive order.  
    note: @jni just tolde me that there is
    skimage.segmentation.relabel_sequential
    """
    unique_labels = np.unique(label_in)
    relabel_lut = np.array([0]*(max(unique_labels)+1))
    relabel_lut[unique_labels] = np.arange(len(unique_labels))
    return relabel_lut[label_in]