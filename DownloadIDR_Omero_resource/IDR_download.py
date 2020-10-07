# Download raw pixel data from IDR
# Volker.Hilsenstein@monash.edu
# License BSD-3

import numpy as np
from omero.gateway import BlitzGateway
from itertools import product


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

    plane_indices = list(product(range(nz), range(nc), range(nt)))
    idr_plane_iterator = idr_pixels.getPlanes(plane_indices)

    if progressbar:
        import tqdm

        idr_plane_iterator = tqdm.tqdm(idr_plane_iterator, total=len(plane_indices))

    _tmp = np.asarray(list(idr_plane_iterator))
    _tmp = _tmp.reshape((nz, nc, nt, ny, nx))
    return np.einsum("jmikl", _tmp)


def test_fetch_2d_timelapse():
    sample_img_id = 1512575
    sample_img_shape = (93, 1, 1024, 1344, 1)
    sample_img_hash = "368793dbb3477c5acfce647cc05ebfc3d86e3b5757a39791111571dc4c305862"
    import hashlib

    img = IDR_fetch_image(sample_img_id)
    h = hashlib.sha256(np.ascontiguousarray(img))
    assert h.hexdigest() == sample_img_hash
    assert img.shape == sample_img_shape


# TODO: use parametrized testing to adhere to DRY principle
def test_fetch_multichannel_zstack():
    sample_img_id = 10502968
    sample_img_shape = (1, 20, 480, 480, 3)
    sample_img_hash = "44190d5ed14a2d138bdf901bbc66367cded8e7cb5fac0cc4dc4b064106749256"
    import hashlib

    img = IDR_fetch_image(sample_img_id)
    h = hashlib.sha256(np.ascontiguousarray(img))
    assert h.hexdigest() == sample_img_hash
    assert img.shape == sample_img_shape