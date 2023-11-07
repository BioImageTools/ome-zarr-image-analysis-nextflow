
process BLUR {
	conda "scikit-image==0.22.0 ome-zarr==0.8.0"

    publishDir "output", mode: 'copy'
	
    input:
    tuple val(meta), path(omezarr_root), val(dataset)
    val(sigma) //for blurring, e.g. "2.5,2.5" or "3,3,5"

    output:
    tuple val(meta), path(omezarr_out)

    script:
    omezarr_out = meta['id'] + "_blurred.ome.zarr"
    def args = task.ext.args ?: ''
    """
    blur.py \
        $args # channel, timepoint, resolution 
        -i $omezarr_root/$dataset
        -sigma $sigma
        -o $omezarr_out

    #cat <<-END_VERSIONS > blurring_versions.yml
    #"${task.process}":
    #    blurring: \$(echo \$(blur.py --version 2>&1) | sed 's/^.*blur.py //; s/Using.*\$//' ))
    #END_VERSIONS
    """
}

process SEGMENT {
	conda "scikit-image==0.22.0 ome-zarr==0.8.0"

    input:
    tuple val(meta), path()

    script:
    """
    """

}


process MORPHOMETRY {
	conda "scikit-image==0.22.0 ome-zarr==0.8.0"

    input:
    tuple val(meta), path()

    script:
    """
    """
}


workflow {

    ch_versions = Channel.empty()
    meta = [:]
    meta.id = "input"

	BLUR(channel.from([meta, params.input_image, params.dataset]))
    ch_versions = ch_versions.mix(BLUR.out.versions)

	// SEGMENT(BLUR.out)
    // MORPHOMETRY(SEGMENT.out)
}
