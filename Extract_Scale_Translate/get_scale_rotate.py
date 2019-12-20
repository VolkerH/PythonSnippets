# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Demonstration of how to interact with visuals, here with simple
arcball-style control.
"""


import numpy as np
from vispy.visuals import  transforms


def is_diag(m: np.ndarray):
    ''' check whether a numpy array is diagonal within floating point accuracy'''
    # https://stackoverflow.com/questions/43884189/check-if-a-large-matrix-is-diagonal-matrix-in-python
    return np.allclose(np.diag(np.diag(m)), m)    

def get_translation_from_MatrixTransform(M: transforms.MatrixTransform):
    ''' returns the translation vector from a MatrixTransform '''
    
    assert isinstance(M, transforms.MatrixTransform), "need MatrixTransform object"
    # scaling, rotation, shear happens in the top left 3x3 matrix
    t = np.array(M.matrix)[3,:3]
    return(t)

def get_scale_from_MatrixTransform(M: transforms.MatrixTransform):
    ''' 
        checks whether a MatrixTransform is essentially just a
        scale + translate transform, and 
        if that is the case it returns the scaling information
        as a vector of length 3.

        otherwise it returns None
    
        alternative to consider: issue a warning and return 1.0, 1.0, 1.0
        if it is not a pure scaling transform
    '''

    assert isinstance(M, transforms.MatrixTransform), "need MatrixTransform object"
    # scaling, rotation, shear happens in the top left 3x3 matrix
    R = np.array(M.matrix)[:3,:3]
    if not is_diag(R):
        # issue warning that it is not pure scale + translate
        return None
    # scaling information is just the diagonal
    return np.diag(R)


if __name__ == "__main__":
    transform = transforms.MatrixTransform()
    print("after instantiation")
    print("scale: ", get_scale_from_MatrixTransform(transform))
    print("translate: ", get_translation_from_MatrixTransform(transform))

    transform.scale((99.0, 11.0, 1.1))
    transform.translate((200, 100))
    print("After scale and translate")
    print("scale: ", get_scale_from_MatrixTransform(transform))
    print("translate: ", get_translation_from_MatrixTransform(transform))

    transform.rotate(33.0, (0.5,1.0,1.0))
    print("After rotate")
    print("scale: ", get_scale_from_MatrixTransform(transform))
    print("translate: ", get_translation_from_MatrixTransform(transform))


