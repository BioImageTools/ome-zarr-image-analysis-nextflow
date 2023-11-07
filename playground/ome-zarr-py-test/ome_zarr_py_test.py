# https://ome-zarr.readthedocs.io/en/stable/python.html#reading-ome-ngff-images

from ome_zarr.io import parse_url
from ome_zarr.reader import Reader

#url = "https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0062A/6001240.zarr"
url = "data/xy_8bit__nuclei_PLK1_control.ome.zarr"

# read the image data
reader = Reader(parse_url(url))
# nodes may include images, labels etc
nodes = list(reader())
# first node will be the image pixel data
image_node = nodes[0]
metadata = image_node.metadata
dask_data = image_node.data
dask_data
