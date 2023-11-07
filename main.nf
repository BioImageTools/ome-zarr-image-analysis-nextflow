
process BLUR {
	conda "scikit-image==0.22.0 ome-zarr==0.8.2"
	
    input:
    tuple val(meta), path(omezarr_root), val(dataset)
    val(sigma) //for blurring, e.g. "2.5, 2.5"

    output:

    script:
    def args = task.ext.args ?: ''
    """
    blur.py \
        $args # channel, timepoint, resolution 
        -i $omezarr_root/$dataset
        -sigma $sigma
        -o 
    """

}

process SEGMENT {
	conda "scikit-image==0.22.0 ome-zarr==0.8.2"

    tuple val(meta), path()


}


process MORPHOMETRY {
	conda "scikit-image==0.22.0 ome-zarr==0.8.2"

    tuple val(meta), path()

}


workflow {
    meta = [:]
    meta.id = "input"
	BLUR(channel.from([meta, params.input_image, params.dataset]))
	SEGMENT(BLUR.out)
    MORPHOMETRY(SEGMENT.out)
}
