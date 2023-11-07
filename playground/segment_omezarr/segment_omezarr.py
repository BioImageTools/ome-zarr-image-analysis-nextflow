from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from ome_zarr.scale import Scaler
from skimage import filters, morphology
import zarr
from ome_zarr import writer
import numpy as np


def segment(inpath,
            resolution=0,
            export_labels=False,
            outpath=None
            ):
    ### Apply otsu threshold to OME-Zarr and write output to a separate OME-Zarr directory.
    # Read OME-Zarr and specify a resolution layer.
    reader = Reader(parse_url(inpath))
    inputs = list(reader())
    image = inputs[0].data[int(resolution)]
    # Get the numpy array and perform threshold
    t = filters.threshold_otsu(image)
    mask = morphology.label(image > t)
    # Save the output
    if export_labels:
        # Write labels as a separate OME-Zarr hierarchy
        assert outpath is not None, "If export_labels is True, outpath must be specified as a directory path."
        group = zarr.open_group(outpath, mode='a')
        _ = writer.write_image(image=mask, group=group,
                               storage_options={'dimension_separator': '/'})
    else:
        # Write labels to the labels subdirectory of the input OME-Zarr hierarchy
        group = zarr.open_group(inpath, mode='a')
        _ = writer.write_labels(labels=mask, group=group, name='otsu',
                                storage_options={'dimension_separator': '/'})


if __name__ == '__main__':
    inpath = "data/xy_8bit__nuclei_PLK1_control.ome.zarr"
    segment(inpath)
