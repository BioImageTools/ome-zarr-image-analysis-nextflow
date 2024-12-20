#! /usr/bin/env python3

import argparse
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from ome_zarr.scale import Scaler
from ome_zarr import writer
from skimage.filters import gaussian
import zarr
import numpy as np


def main(args):
    # read the image data
    r = Reader(parse_url(args.input, mode="r"))
    # nodes may include images, labels etc
    nodes = list(r())

    # first node will be the image pixel data
    image_node = nodes[0]

    sigmas = [float(s) for s in args.sigma.split(",")]

    data = image_node.data
    layer = data[args.resolution]
    blurred_img = gaussian(
        layer,
        sigma=sigmas
    )

    # has to be append mode, otherwise: OSError: Cannot call rmtree on a symbolic link
    gr = zarr.open_group(args.output, mode = 'a')

    channel_index = [i for i, axis in enumerate(image_node.metadata['axes']) if axis['name'] == 'c'][0]
    combined = np.concatenate((layer, blurred_img), axis = channel_index)

    scaler = Scaler(max_layer = len(data) - 1)
    _ = writer.write_image(
                            combined,
                            group = gr,
                            scaler = scaler,
                            axes = image_node.metadata['axes'],
                            storage_options = {'dimension_separator': '/'},
                           )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Blur an OME-Zarr image')

    parser.add_argument('-i', '--input', type=str, required=True, \
                        help='Path to the OME-Zarr dataset containing the input image')
    parser.add_argument('-o', '--output', type=str, required=True, \
                        help='Path to the OME-Zarr dataset (relative to root) where the output image will be written')
    parser.add_argument('-s', '--sigma', type=str, required=True, \
        help='Sigma for blur kernel, comma delimited')
    parser.add_argument('-c', '--channel', type=int, default=0,
                        help='Channel index')
    parser.add_argument('-t', '--timepoint', type=int, default=0,
                        help='Timepoint index')
    parser.add_argument('-r', '--resolution', type=int, default=0,
                        help='Resolution index')
    parser.add_argument('-p', '--processing_method', type=str, default="", 
                        help='processing method')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
    args = parser.parse_args()

    main(args)
