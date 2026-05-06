import argparse
import scanpy as sc
import yaml


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def preprocess(adata, cfg):
    # QC filtering
    if cfg["preprocessing"]["min_genes"]:
        sc.pp.filter_cells(adata, min_genes=cfg["preprocessing"]["min_genes"])
    if cfg["preprocessing"]["min_cells"]:
        sc.pp.filter_genes(adata, min_cells=cfg["preprocessing"]["min_cells"])

    # Remove MT genes
    if cfg["preprocessing"]["remove_mt"]:
        adata = adata[:, ~adata.var_names.str.startswith("MT-")]

    # Remove ribosomal
    if cfg["preprocessing"]["remove_ribo"]:
        adata = adata[:, ~adata.var_names.str.startswith(("RPL", "RPS"))]

    keep_obs = [
    "n_counts",
    "cell_type_gao",
    "response",
    "patient",
    'venetoclax', 'treat','mut', 'relapse', 'age', 'timing', 'category',  'cellType', 'dcellType','nUMI', 'nGene', 
    ]

    adata_aml = adata_aml[:, :]  # copy if needed
    adata_aml.obs = adata_aml.obs[keep_obs]

    adata_aml.var = adata_aml.var[["ensembl_id"]]

    # 清空这些
    adata_aml.obsm = {}
    adata_aml.obsp = {}
    adata_aml.uns = {}
    adata_aml.layers = {}



    # Normalize + log
    sc.pp.normalize_total(adata)
    sc.pp.log1p(adata)

    # PCA
    sc.pp.pca(adata, n_comps=cfg["representation"]["n_pcs"])

    # Neighbors
    sc.pp.neighbors(
        adata,
        n_neighbors=cfg["representation"]["n_neighbors"]
    )

    # UMAP
    sc.tl.umap(
        adata,
        min_dist=cfg["representation"]["min_dist"]
    )

    return adata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--config")
    args = parser.parse_args()

    cfg = load_config(args.config)

    adata = sc.read_h5ad(args.input)

    adata = preprocess(adata, cfg)

    adata.write(args.output)


if __name__ == "__main__":
    main()