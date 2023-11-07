# Wish list

## ome-zarr-py

- More concise way to find axes indices, currently: `channel_index = [i for i, axis in enumerate(image_node.metadata['axes']) if axis['name'] == 'c'][0]` 
