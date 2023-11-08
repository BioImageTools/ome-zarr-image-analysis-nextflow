#! /usr/bin/env python3

from pathlib import Path
from skimage import filters, transform, morphology
import zarr
from ome_zarr import writer, scale, reader
from ome_zarr.io import parse_url
import numpy as np
from typing import Optional
import fire
import os


def segment(
        omezarr_root: str,
        dataset: str,
        resolution: int = 0,
        channel: Optional[int] = 0,
        segmentation_name: str = 'otsu',
        export_labels: bool = False,
    ):
    ### Apply otsu threshold to OME-Zarr and write output to a separate OME-Zarr directory.
    # Read OME-Zarr and specify a resolution layer.
    target_raw  = os.sep.join([omezarr_root, dataset])
    r = reader.Reader(parse_url(target_raw, mode="r"))
    inputs = list(r())
    data = inputs[0].data
    multimeta = inputs[0].metadata
    layer = data[int(resolution)]
    # Get the numpy array and perform threshold
    axes = multimeta['axes']
    axorder = ''.join([item['name'] for item in axes])
    ch_idx = axorder.index('c')
    # Get the numpy array and perform threshold
    array = np.array(layer)
    slicer = [slice(None, None, None) for _ in range(array.ndim)]
    slicer[ch_idx] = slice(channel, channel + 1, None)
    sliced = array[tuple(slicer)]
    t = filters.threshold_otsu(sliced)
    mask = morphology.label(sliced > t)
    # resize the top resolution layer to get the lower layers of the pyramid
    shape = np.array(mask.shape)
    nres = len(data)
    new_shapes = [np.where(shape > 1, shape // 2 ** n, shape) for n in range(nres)]
    layers = [transform.resize(mask, tuple(shape), preserve_range = True).astype(np.uint8) for shape in new_shapes]
    # Save the output
    if export_labels:
        # Write labels as a separate OME-Zarr hierarchy
        # assert outpath is not None, "If export_labels is True, outpath must be specified as a directory path."
        gr = zarr.open_group(omezarr_root + "/" + dataset, mode = 'a')
        _ = writer.write_multiscale(pyramid = layers, group = gr)
    else:
        # Write labels to the labels subdirectory of the input OME-Zarr hierarchy
        gr = zarr.open_group(target_raw, mode='a')
        _ = writer.write_multiscale_labels(pyramid = layers, group = gr, name = segmentation_name, storage_options={'dimension_separator': '/'})

def version():
    print("0.0.1")

if __name__ == '__main__':
    cli = {
        "version": version,
        "run": segment
    }
    fire.Fire(cli)
