rule preprocess:
    input:
        h5ad=config["data"]["input_h5ad"]
    output:
        h5ad=config["data"]["output_h5ad"]
    log:
        "logs/preprocess.log"
    conda:
        "envs/scanpy.yaml"
    shell:
        """
        python workflow/scripts/preprocess.py \
            --input {input.h5ad} \
            --output {output.h5ad} \
            --config config/config.yaml \
            > {log} 2>&1
        """