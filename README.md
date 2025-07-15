# Minimal Nextflow OME-Zarr workflow

Simple example created by a group at the "Next generation bioimage analysis workflows hackathon".


## Usage

1. Git pull this repository
2. cd into the repository folder
3. Modify the `data/input_params.yaml` file to point to the _absolute_ input image path 
4. Run the following command:
If you have a conda environment with nextflow installed, you can run the following command:
```
nextflow run . -params-file data/input_params_local.yaml -profile docker
```
or run with docker:
```
nextflow run . -params-file data/input_params_local.yaml -profile docker
```

## Aims

- [x] Explore what nf-core gives us for specifying inputs and outputs
- [x] Explore storing versioning file as in nf-core. Update: putting all versioning logging file at the root for now.
- [x] Create a github-repo for the below code
- [x] Create a minimal workflow in Nextflow that uses OME-Zarr
  - [x] Process 1: Create new gaussian blurred ome-zarr image
  - [x] Process 2: Segment image
  - [x] Process 3: Measure segment shape features
- [ ] Should the input be only one scale? Or multiple?
- [ ] How to handle the multi-scales for the outputs?
- [x] Root ome-zarr + subfolder strings as input. Numpy/dask object as Image/labels data.
- [x] label image stored within the same ome-zarr file as an image
- [x] 'Hacked' nextflow IO to allow for reading/writing valid OME-Zarr files
- [ ] Where/how to store the table?
- [ ] A more tightly connected image visualisation tool?
- [ ] Integration Fractal tasks into Nextflow 
* Bonus
  - [ ] Process only a part of an image
  - [ ] Use a Fractal task as one of the Nextflow processes
 
## Observations

 * Important tools and libraries require arrays of specific input dimensionality to operate on, thus we need convenient APIs and implementations that allow us to subset OME-Zarr.
   * Very few (none?) of the current tools natively work on multi-resolution input, thus be able to specify which resolution level to work on is important and not well supported by the python libraries that we found.

## Analysis tools landscape in terms of input dimensionalities

### 2D RGB  

- YOLO
- SAM

### 2D or 3D RGB  

- Cellpose
  - Is it really RGB?  

### 2D or 3D multi-channel

- elastix

### ND

- skimage ?!
- ImgLib2 ?!
