rule example:
    output:
        "results/example_done.txt"
    shell:
        """
        echo "project: {{ config['project_name'] }}" > {output}
        """