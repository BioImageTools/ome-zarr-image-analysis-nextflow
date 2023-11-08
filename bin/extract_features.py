#! /usr/bin/env python3

#from ome_zarr import writer
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
from skimage.measure import regionprops_table
import fire
import os
import csv


def write_dict_to_csv(dictionary, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dictionary.keys())
        writer.writerow(dictionary.values())


def extract_features(
        omezarr_root: str,
        segmentation_method: str="otsu",
        resolution=0,
    ):
    ### Extract basic image features and append to the same OME-Zarr.
    # Read OME-Zarr label image and specify a resolution layer.
    label_path = os.sep.join([omezarr_root, "labels", segmentation_method])
    label_reader = Reader(parse_url(label_path))
    label = list(label_reader())[0].data[resolution]

    raw_reader = Reader(parse_url(omezarr_root))
    raw = list(raw_reader())[0].data[resolution]

    # zarr_root = zarr.open_group(label_path, 'r')
    # Get the numpy array and perform measurements 
    properties = regionprops_table(
        label[0, 0, 0, ...].compute(),
        intensity_image=raw[0, 0, 0, ...].compute(),
        properties=['label', 'area', 'centroid', 'mean_intensity', 'max_intensity', 'min_intensity']     
    )
    np_dict = {}
    for k, v in properties.items():
        if k == "image_intensity":
            continue
        try:
            np_dict[k] = v.get()
        except:
            np_dict[k] = v
    # Save the output
    write_dict_to_csv(np_dict, f"{omezarr_root}/Features.csv")
    #writer.write(pyramid=inputs, group=inputs)

def version():
    print("0.0.1")

if __name__ == '__main__':
    cli = {
        "version": version,
        "run": extract_features
    }
    fire.Fire(cli)
