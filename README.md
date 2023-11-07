# Minimal Nextflow OME-Zarr workflow

Simple example created by a group at the "Next generation bioimage analysis workflows hackathon".

## Aims

* Explore what nf-core gives us for specifying inputs and outputs
* Explore storing versioning file as in nf-core
* Create a github-repo for the below code
* Create a minimal workflow in Nextflow that uses OME-Zarr
  * Process 1: Segment image
  * Process 2: Measure segment shape features
* Should the input be only one scale? Or multiple?
* How to handle the multi-scales for the outputs?
* What exactly is the input for an image / labels?
* Where to store the label mask? Inside the input.zarr or create a new one?
* Explore how to link OME-Zarr data rather than copy it
* Where/how to store the table?
* A more tightly connected image visualisation tool?
* Probably good to look at Fractal tasks in this context
* Bonus
  * Process only a part of an image
  * Use a Fractal task as one of the Nextflow processes
 
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
