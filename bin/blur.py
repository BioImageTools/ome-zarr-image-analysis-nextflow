#! /usr/bin/env python3

import argparse
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from ome_zarr.writer import Writer

#url = "https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0062A/6001240.zarr"
url = "../data/xy_8bit__nuclei_PLK1_control.ome.zarr"

# read the image data
store = parse_url(url, mode="r").store
reader = Reader(parse_url(url))
# nodes may include images, labels etc
nodes = list(reader())

# first node will be the image pixel data
image_node = nodes[0]

channel_index = [i for i, axis in enumerate(metadata['axes']) if axis['name'] == 'c'][0]










if __name__ == "__main__":


        #$args # channel, timepoint, resolution 
        #-i $omezarr_root/$dataset
        #-sigma $sigma
        #-o $omezarr_out

    parser = argparse.ArgumentParser(description='Blur an OME-Zarr image')

    parser.add_argument('-i', '--input', dest='input_path', type=str, required=True, \
        help='Path to the OME-Zarr data set containing the input image')
    parser.add_argument('-o', '--output', dest='output_path', type=str, required=True, \
        help='Path to the OME-Zarr data set where the output image will be written')
    parser.add_argument('-s', '--sigma', dest='sigma', type=float, required=True, \
        help='Sigma for blur kernel')
    

    args = parser.parse_args()


