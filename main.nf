
params.input_image = "data/xy_8bit__nuclei_PLK1_control.ome.zarr"
params.sigma = "1,1,1,2.5,2.5"
params.dataset = ''

conda_env_spec = "conda-forge::scikit-image=0.22.0 conda-forge::ome-zarr=0.8.0 conda-forge::fire=0.5.0"
docker_img = "bioinfotongli/ome-zarr-nextflow-minimum:latest"

process BLUR {
    debug true

	conda conda_env_spec
    container docker_img

    input:
    tuple val(meta), path(omezarr_root), val(dataset), path(outdir)
    val(sigma) //for blurring, e.g. "2.5,2.5" or "3,3,5"

    output:
    tuple val(meta), path(outdir), val(dataset), emit: blurred
    // path("blurring_versions.yml"), emit: versions

    script:
    def args = task.ext.args ?: ''
    def dataset = dataset ?: ''
    def verion_file_name = "blurring_versions.yml"
    """
    blur.py \
        -i $omezarr_root$dataset \
        -s $sigma \
        -o $outdir \
        $args # channel, timepoint, resolution 

    cat <<-END_VERSIONS > ${outdir}/${verion_file_name}
    "${task.process}":
        blurring: \$(echo \$(blur.py --version 2>&1 | sed 's/^.*blur.py //; s/Using.*\$//' ))
        timestamp: \$(date)
        modified_path: $outdir
    END_VERSIONS
    """
}

process SEGMENT {
    debug true

	conda conda_env_spec
    container docker_img

    input:
    tuple val(meta), path(omezarr_root), val(dataset)

    output:
    tuple val(meta), path(omezarr_root), val(dataset), emit: segmented
    // path(verion_file_name), emit: versions

    script:
    def args = task.ext.args ?: ''
    def dataset = dataset ?: ''
    def verion_file_name = "segmentation_versions.yml"
    """
    segment.py run \
        $omezarr_root$dataset \
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
    tuple val(meta), path(omezarr_root), val(dataset)

    output:
    tuple val(meta), path(omezarr_root), val(dataset)
    // path(verion_file_name), emit: versions

    script:
    def verion_file_name = "feature_extraction_versions.yml"
    def args = task.ext.args ?: ''
    """
    extract_features.py run \
        $omezarr_root$dataset \
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
    meta = [:]
    meta.id = "demo"
    meta.processing_method = "gaussian_blur"
    meta.segmentation_name = "otsu1"
    meta.processed_id = meta.id + "_" + meta.processing_method + ".ome.zarr"

    def directory = new File(meta.processed_id)
    if (!directory.exists()) {
        directory.mkdirs()
    }

	BLUR(
        channel.from(
            [
                [meta, file(params.input_image, checkIfExists:true), params.dataset, file(meta.processed_id, checkIfExists:true)],
            ]
        ),
        params.sigma
    )
    // ch_versions = ch_versions.mix(BLUR.out.versions)

	SEGMENT(BLUR.out.blurred)
    MORPHOMETRY(SEGMENT.out.segmented)
}
