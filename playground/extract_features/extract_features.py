#from ome_zarr import writer
#from ome_zarr.io import parse_url
#from ome_zarr.reader import Reader
import zarr
from skimage.measure import regionprops


def extract_features(inpath,
            label='',
            resolution='0',
            outpath=None
            ):
    ### Extract basic image features and append to the same OME-Zarr.
    # Read OME-Zarr label image and specify a resolution layer.
    #reader = Reader(parse_url(inpath))
    #inputs = list(reader())
    zarr_root = zarr.open_group(inpath, 'a')
    label_image = zarr_root
    if label != '':
        label_image = label_image.labels[label]
    label_root = label_image
    label_image = label_image[resolution]
    # Get the numpy array and perform threshold
    properties = regionprops(label_image[0, 0, 0, ...])
    areas = [{"label-value": i, "area (pixels)": int(property.area)} for i, property in enumerate(properties)]
    label_root.attrs["image-label"] = {"properties": areas}
    # Save the output
    #writer.write(pyramid=inputs, group=inputs)


if __name__ == '__main__':
    extract_features("data/xy_8bit__nuclei_PLK1_control.ome.zarr", label="otsu")
