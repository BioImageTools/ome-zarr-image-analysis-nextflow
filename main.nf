
params.input_image = "data/xy_8bit__nuclei_PLK1_control.ome.zarr"
params.sigma = "1,1,1,2.5,2.5"
params.outdir = "./output"

conda_env_spec = "conda-forge::scikit-image=0.22.0 conda-forge::ome-zarr=0.8.0 conda-forge::fire=0.5.0"
docker_img = "bioinfotongli/ome-zarr-nextflow-minimum:latest"

process BLUR {
    debug true

	conda conda_env_spec
    container docker_img

    input:
    tuple val(meta), path(omezarr_root), path(omezarr_out)
    val(sigma) //for blurring, e.g. "2.5,2.5" or "3,3,5"

    output:
    tuple val(meta), path(omezarr_out), emit: blurred
    // path("blurring_versions.yml"), emit: versions

    script:
    def args = task.ext.args ?: ''
    def verion_file_name = "blurring_versions.yml"
    """
    blur.py \
        -i $omezarr_root \
        -s $sigma \
        -o $omezarr_out \
        $args # channel, timepoint, resolution 

    cat <<-END_VERSIONS > ${omezarr_out}/${verion_file_name}
    "${task.process}":
        blurring: \$(echo \$(blur.py --version 2>&1 | sed 's/^.*blur.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $omezarr_out
    END_VERSIONS
    """
}

process SEGMENT {
    debug true

	conda conda_env_spec
    container docker_img

    input:
    tuple val(meta), path(omezarr_root)

    output:
    tuple val(meta), path(omezarr_root), emit: segmented
    // path(verion_file_name), emit: versions

    script:
    def args = task.ext.args ?: ''
    def verion_file_name = "segmentation_versions.yml"
    """
    segment.py run \
        $omezarr_root \
        --segmentation_name ${meta.segmentation_name} \
        $args #

    cat <<-END_VERSIONS > ${omezarr_root}/${verion_file_name}
    "${task.process}":
        segment: \$(echo \$(segment.py version 2>&1 | sed 's/^.*segment.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $omezarr_root/labels/$meta.segmentation_name
    END_VERSIONS
    """
}


process MORPHOMETRY {
    debug true

	conda conda_env_spec
    container docker_img

    input:
    tuple val(meta), path(omezarr_root)

    output:
    tuple val(meta), path(omezarr_root)
    // path(verion_file_name), emit: versions

    script:
    def verion_file_name = "feature_extraction_versions.yml"
    def args = task.ext.args ?: ''
    """
    extract_features.py run \
        $omezarr_root \
        --segmentation_method ${meta.segmentation_name} \
        $args

    cat <<-END_VERSIONS > ${omezarr_root}/${verion_file_name}
    "${task.process}":
        features: \$(echo \$(extract_features.py version 2>&1 | sed 's/^.*extract_features.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $omezarr_root/Features.csv
    END_VERSIONS
    """
}


workflow {

    // ch_versions = Channel.empty()
    // ch_versions = ch_versions.mix(BLUR.out.versions)

    datasets = channel.from(params.images)
        .multiMap{dataset ->
            new_output = file(params.outdir + "/" +dataset[0].processed_id)
            to_blur: [dataset[0], file(dataset[1]), new_output] //channel to be processed
            to_create_output: new_output //channel of output dirs to be created
        }

    datasets.to_create_output.map{ it -> it.mkdirs()} // create output dirs for all datasets

	BLUR(datasets.to_blur, params.sigma)
	SEGMENT(BLUR.out.blurred)
    MORPHOMETRY(SEGMENT.out.segmented)
}