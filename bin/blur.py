#! /usr/bin/env python3

import argparse
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from ome_zarr import writer
from skimage.filters import gaussian
import zarr

#url = "https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0062A/6001240.zarr"
url = "../data/xy_8bit__nuclei_PLK1_control.ome.zarr"

def main(args):
    # read the image data
    reader = Reader(parse_url(args.input, mode="r").store)
    # nodes may include images, labels etc
    nodes = list(reader())

    # first node will be the image pixel data
    image_node = nodes[0]

    channel_index = [i for i, axis in enumerate(metadata['axes']) if axis['name'] == 'c'][0]

    sigma = args.sigma.split(",")

    dask_img = image_node.data
    blurred_img = gaussian(dask_img, sigma=sigma)
    two_ch_img = da.array([blurred_img, blurred_img])
    gr = zarr.open_group(args.output, mode = 'w')
    _ = writer.write_multiscale(pyramid = layers, group = gr)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Blur an OME-Zarr image')

    parser.add_argument('-i', '--input', type=str, required=True, \
                        help='Path to the OME-Zarr data set containing the input image')
    parser.add_argument('-o', '--output', type=str, required=True, \
                        help='Path to the OME-Zarr data set where the output image will be written')
    parser.add_argument('-s', '--sigma', type=str, required=True, \
        help='Sigma for blur kernel, comma delimited')
    parser.add_argument('-c', '--channel', type=int, default="0", 
                        help='Channel index')
    parser.add_argument('-t', '--timepoint', type=int, default="0", 
                        help='Timepoint index')
    parser.add_argument('-r', '--resolution', type=int, default="0", 
                        help='Resolution index')
    args = parser.parse_args()

    main(args)
