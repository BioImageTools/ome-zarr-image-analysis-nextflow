# dependencies
# mamba create -n ngff-zarr python=3.9
# pip install 'ngff-zarr'

import ngff_zarr

# open
input_multiscales = ngff_zarr.from_ngff_zarr("/Users/tischer/Documents/ome-zarr-image-analysis-nextflow/data/xy_8bit__nuclei_PLK1_control.ome.zarr")

# inspect one resolution
num_resolutions = len(input_multiscales.images)
image = input_multiscales.images[0]

data = image.data
scale = image.scale
translation = image.translation
units = image.axes_units

# process one resolution
numpy_array = data.compute()
print("some pixel value:", numpy_array[0, 0, 0, 1, 1])
spatial_indices = [index for index, value in enumerate(image.dims) if value in ('x', 'y', 'z')]
numpy_array = numpy_array + 2
print("same pixel after adding 2:", numpy_array[0, 0, 0, 1, 1])

# save one resolution
output_image = ngff_zarr.to_ngff_image(numpy_array, image.dims, image.scale, image.translation, "processed", image.axes_units )

# Below line
# Error: ModuleNotFoundError: No module named 'dask_image'
# Fix: pip install dask-image
output_multiscales = ngff_zarr.to_multiscales(output_image, 1)
ngff_zarr.to_ngff_zarr("/Users/tischer/Desktop/output_ome_zarr", output_multiscales)

# the output can be opened with Napari, using the ome-zarr plugin
