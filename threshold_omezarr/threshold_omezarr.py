from pathlib import Path
from skimage import filters, transform
import zarr
from ome_zarr import writer
import numpy as np

def apply_threshold(mainpath,
                    outpath,
                    resolution = '0',
                    ):
    ### Apply otsu threshold to OME-Zarr and write output to a separate OME-Zarr directory.
    inpath = Path(mainpath)
    inputs = zarr.open_group(inpath)
    nres = len(list(inputs.array_keys()))
    layer = inputs[resolution]
    ###
    array = np.array(layer)
    t = filters.threshold_otsu(array)
    mask = array > t
    shape = np.array(mask.shape)
    new_shapes = [np.where(shape > 1, shape // 2 ** n, shape) for n in range(nres)]
    layers = [transform.resize(mask, tuple(shape)) for shape in new_shapes]
    gr = zarr.open_group(outpath, mode = 'a')
    _ = writer.write_multiscale(pyramid = layers, group = gr)
    return None

