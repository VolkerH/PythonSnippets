import numpy as np
import omero
from omero.gateway import BlitzGateway
from itertools import product
import tifffile


def IDR_fetch_image(image_id: int, progressbar: bool = True) -> np.ndarray:
    """
    Download the image with id image_id from the IDR

    Will fetch all image planes corresponding to separate
    timepoints/channels/z-slices and return a numpy
    array with dimension order (t,z,y,x,c)

    Displaying download progress can be disabled by passing
    False to progressbar.
    """

    conn = BlitzGateway(
        host="ws://idr.openmicroscopy.org/omero-ws",
        username="public",
        passwd="public",
        secure=True,
    )
    conn.connect()
    conn.c.enableKeepAlive(60)

    idr_img = conn.getObject("Image", image_id)
    idr_pixels = idr_img.getPrimaryPixels()

    _ = idr_img
    nt, nz, ny, nx, nc = (
        _.getSizeT(),
        _.getSizeZ(),
        _.getSizeY(),
        _.getSizeX(),
        _.getSizeC(),
    )
    img_shape = (nt, nz, ny, nx, nc)

    plane_indices = list(product(range(nz), range(nc), range(nt)))
    idr_plane_iterator = idr_pixels.getPlanes(plane_indices)

    if progressbar:
        import tqdm

        idr_plane_iterator = tqdm.tqdm(idr_plane_iterator, total=len(plane_indices))
    # TODO Need to work on proper reshaping
    print("Warning. Reshaping not tested properly and likely wrong")
    return np.asarray(list(idr_plane_iterator)).reshape(img_shape)


def test_fetch():
    """as a test download a sample image that we have previously downloaded
    and see whether it matches previous hash and shape"""
    sample_img_id = 1512575
    sample_img_shape = (93, 1, 1024, 1344, 1)
    sample_img_hash = "368793dbb3477c5acfce647cc05ebfc3d86e3b5757a39791111571dc4c305862"
    import hashlib

    img = IDR_fetch_image(sample_img_id)
    h = hashlib.sha256(np.ascontiguousarray(img))
    assert h.hexdigest() == sample_img_hash
    assert img.shape == sample_img_shape