
params.input_image = "data/xy_8bit__nuclei_PLK1_control.ome.zarr"
params.sigma = "1,1,1,2.5,2.5"
params.dataset = ''

process BLUR {
    debug true
	conda "conda-forge::scikit-image=0.22.0 conda-forge::ome-zarr=0.8.0"

    publishDir "output", mode: 'copy'
	
    input:
    tuple val(meta), path(omezarr_root), val(dataset)
    val(sigma) //for blurring, e.g. "2.5,2.5" or "3,3,5"

    output:
    tuple val(meta), path(omezarr_out), emit: blurred
    path("blurring_versions.yml"), emit: versions

    script:
    omezarr_out = meta['id'] + "_blurred.ome.zarr"
    def args = task.ext.args ?: ''
    def dataset = dataset ?: ''
    def verion_file_name = "blurring_versions.yml"
    """
    blur.py \
        -i $omezarr_root$dataset \
        -s $sigma \
        -o $omezarr_out\
        $args # channel, timepoint, resolution 

    cat <<-END_VERSIONS > ${verion_file_name}
    "${task.process}":
        blurring: \$(echo \$(blur.py --version 2>&1) | sed 's/^.*blur.py //; s/Using.*\$//' ))
    END_VERSIONS
    """
}

process SEGMENT {
    debug true
	conda "conda-forge::scikit-image=0.22.0 conda-forge::ome-zarr=0.8.0"

    input:
    tuple val(meta), path(omezarr_root), val(dataset)

    output:
    tuple val(meta), path(omezarr_root), val(dataset)
    path(verion_file_name), emit: versions

    script:
    def args = task.ext.args ?: ''
    def dataset = dataset ?: ''
    def verion_file_name = "segmentation_versions.yml"
    """
    segment.py \
        -i $omezarr_root$dataset \
        $args #

    cat <<-END_VERSIONS > ${verion_file_name}
    "${task.process}":
        segment: \$(echo \$(segment.py --version 2>&1) | sed 's/^.*segment.py //; s/Using.*\$//' ))
    END_VERSIONS
    """
}


process MORPHOMETRY {
	conda "scikit-image=0.22.0 ome-zarr=0.8.0"

    input:
    tuple val(meta), path(omezarr_root), val(dataset)

    output:

    script:
    """
    """
}


workflow {

    ch_versions = Channel.empty()
    meta = [:]
    meta.id = "input"

	BLUR(
        channel.from([[meta, file(params.input_image, checkIfExist:true), params.dataset]]),
        params.sigma
    )
    ch_versions = ch_versions.mix(BLUR.out.versions)

	SEGMENT(BLUR.out)
    MORPHOMETRY(SEGMENT.out)
}
