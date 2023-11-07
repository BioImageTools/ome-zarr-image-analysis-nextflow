from pathlib import Path
from skimage import filters, transform, morphology
import zarr
from ome_zarr import writer
import numpy as np

def apply_threshold(inpath,
                    resolution = '0',
                    export_labels = False,
                    outpath = None
                    ):
    ### Apply otsu threshold to OME-Zarr and write output to a separate OME-Zarr directory.
    # Read OME-Zarr and specify a resolution layer.
    inputs = zarr.open_group(inpath)
    nres = len(list(inputs.array_keys()))
    layer = inputs[resolution]
    # Get the numpy array and perform threshold
    array = np.array(layer)
    t = filters.threshold_otsu(array)
    mask = morphology.label(array > t)
    # resize the top resolution layer to get the lower layers of the pyramid
    shape = np.array(mask.shape)
    new_shapes = [np.where(shape > 1, shape // 2 ** n, shape) for n in range(nres)]
    layers = [transform.resize(mask, tuple(shape)) for shape in new_shapes]
    # Save the output
    if export_labels:
        # Write labels as a separate OME-Zarr hierarchy
        assert outpath is not None, "If export_labels is True, outpath must be specified as a directory path."
        gr = zarr.open_group(outpath, mode = 'a')
        _ = writer.write_multiscale(pyramid = layers, group = gr)
    else:
        # Write labels to the labels subdirectory of the input OME-Zarr hierarchy
        _ = writer.write_multiscale_labels(pyramid = layers, group = inputs, name = 'thresholded')
    return None

