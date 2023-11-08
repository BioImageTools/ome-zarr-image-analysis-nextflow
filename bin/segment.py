#! /usr/bin/env python3

from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from ome_zarr.scale import Scaler
from skimage import filters, morphology
import zarr
from ome_zarr import writer
import fire
from typing import Optional


def segment(
        omezarr_root: str,
        resolution: int = 0,
        export_labels: bool = False,
        outpath: Optional[str] = None
    ):
    ### Apply otsu threshold to OME-Zarr and write output to a separate OME-Zarr directory.
    # Read OME-Zarr and specify a resolution layer.
    reader = Reader(parse_url(omezarr_root))
    inputs = list(reader())
    image = inputs[0].data[resolution]
    # Get the numpy array and perform threshold
    t = filters.threshold_otsu(image)
    mask = morphology.label(image > t)
    # Save the output
    if export_labels:
        # Write labels as a separate OME-Zarr hierarchy
        assert outpath is not None, "If export_labels is True, outpath must be specified as a directory path."
        group = zarr.open_group(outpath, mode='a')
        _ = writer.write_image(image=mask, group=group,
                               storage_options={'dimension_separator': '/'}
                               )
    else:
        # Write labels to the labels subdirectory of the input OME-Zarr hierarchy
        group = zarr.open_group(omezarr_root, mode='a')
        _ = writer.write_labels(labels=mask, group=group, name='otsu',
                                storage_options={'dimension_separator': '/'}
                                )

def version():
    return "0.0.1"

if __name__ == '__main__':
    cli = {
        "version": version,
        "run": segment
    }
    fire.Fire(cli)
