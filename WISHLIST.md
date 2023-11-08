# Wish list

## ome-zarr-py

- More concise way to find axes indices, currently: `channel_index = [i for i, axis in enumerate(image_node.metadata['axes']) if axis['name'] == 'c'][0]` 
- Find a proper way of writing extracted tabular feature data
    - for reference [SpatialData](https://github.com/scverse/spatialdata/blob/c5a29ad43533bf4877b76f429ae5471439a8f3f6/src/spatialdata/_io/io_table.py#L9) should work for both HCS and WSI datasets
- Find a proper way keeping crucial processing information, such as:
    - software version
    - software name
    - timestamp(?)
- A official Nextflow support of in-place ome-zarr folder update :)