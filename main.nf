
params.input_image =[
    [["id": "ome-zarr-1"], "./data/xy_8bit__nuclei_PLK1_control.ome.zarr"],
]
params.sigma = "1,1,1,2.5,2.5"
params.outdir = "./output"

conda_env_spec = "conda-forge::scikit-image=0.22.0 conda-forge::ome-zarr=0.8.0 conda-forge::fire=0.5.0"
verbose = true

process BLUR {
    debug verbose

    conda conda_env_spec
    container "quay.io/bioinfotongli/ome-zarr-nextflow-minimum:latest"

    publishDir params.outdir

    input:
    tuple val(meta), path(omezarr_root)
    val(sigma) //for blurring, e.g. "2.5,2.5" or "3,3,5"

    output:
    tuple val(meta), path("${meta.id}"), emit: blurred
    path("${meta.id}/${version_file_name}"), emit: versions

    script:
    def args = task.ext.args ?: ''
    version_file_name = "blurring_versions.yml"
    """
    blur.py \
        -i $omezarr_root \
        -s $sigma \
        -o $meta.id \
        $args # channel, timepoint, resolution 

    cat <<-END_VERSIONS > ${meta.id}/${version_file_name}
    "${task.process}":
        blurring: \$(echo \$(blur.py --version 2>&1 | sed 's/^.*blur.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $meta.id
    END_VERSIONS
    """
}

process SEGMENT {
    debug verbose 

    conda conda_env_spec
    container "quay.io/bioinfotongli/ome-zarr-nextflow-minimum:latest"

    publishDir params.outdir

    input:
    tuple val(meta), path(omezarr_root)

    output:
    tuple val(meta), path(omezarr_root), emit: segmented
    path("${omezarr_root}/${version_file_name}"), emit: versions

    script:
    def args = task.ext.args ?: ''
    version_file_name = "segmentation_versions.yml"
    """
    segment.py run \
        $omezarr_root \
        --segmentation_name ${meta.segmentation_name} \
        $args #

    cat <<-END_VERSIONS > ${omezarr_root}/${version_file_name}
    "${task.process}":
        segment: \$(echo \$(segment.py version 2>&1 | sed 's/^.*segment.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $omezarr_root/labels/$meta.segmentation_name
    END_VERSIONS
    """
}


process MORPHOMETRY {
    debug verbose

    conda conda_env_spec
    container "quay.io/bioinfotongli/ome-zarr-nextflow-minimum:latest"

    publishDir params.outdir

    input:
    tuple val(meta), path(omezarr_root)

    output:
    tuple val(meta), path(omezarr_root)
    path("${omezarr_root}/${version_file_name}"), emit: versions

    script:
    version_file_name = "feature_extraction_versions.yml"
    def args = task.ext.args ?: ''
    """
    extract_features.py run \
        $omezarr_root \
        --segmentation_method ${meta.segmentation_name} \
        $args

    cat <<-END_VERSIONS > ${omezarr_root}/${version_file_name}
    "${task.process}":
        features: \$(echo \$(extract_features.py version 2>&1 | sed 's/^.*extract_features.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $omezarr_root/Features.csv
    END_VERSIONS
    """
}


workflow {
    BLUR(channel.from(params.input_image), params.sigma)
    SEGMENT(BLUR.out.blurred)
    MORPHOMETRY(SEGMENT.out.segmented)
}
