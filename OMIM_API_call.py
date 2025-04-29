import requests
import json
import argparse

OMIM_API_KEY = "GUwwCFBvQ4ezXZVJKMbs8w"

### Navigates through the JSON dictionaries to extract all OMIM numbers from GeneMapSearch API call
def get_omim_numbers(gene_names: str):
    phenotypesmap = get_phenotype_map(gene_names)
    phenotype_response = get_nested_dict(['omim', 'searchResponse'], phenotypesmap)
    gene_maps = phenotype_response.get("geneMapList", [])
    summaries = []

    for gene_map_entry in gene_maps:
        gene_map = gene_map_entry.get("geneMap", {})
        phenotype_map_list = gene_map.get("phenotypeMapList", [])
        for phenotype_entry in phenotype_map_list:
            phenotype_map = phenotype_entry.get("phenotypeMap", {})
            phenotype_mim_number = phenotype_map.get("phenotypeMimNumber")
            if phenotype_mim_number:
                summaries.append(phenotype_mim_number)
    return summaries

### Returns a nested dictionary for other functions to call dictionaries within dictionaries
def get_nested_dict(keys: list, dictionary: dict):
    for key in keys:
        if dictionary:
            dictionary = dictionary.get(key, {})
    return dictionary

### Calls OMIM's API with a gene name to get all phenotype OMIM IDs
def get_phenotype_map(gene_names):
    url = f"https://api.omim.org/api/geneMap/search?search=gene_symbol%3A{gene_names}&format=json&start=0&limit=10&apiKey={OMIM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

### Using all OMIM phenotype ID's call the API again to get the phenotype clinical synopsis
def get_clinical_synopsis(pheno_omim_id):
    url = f"https://api.omim.org/api/clinicalSynopsis?mimNumber={pheno_omim_id}&include=clinicalSynopsis&format=json&apiKey={OMIM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

### Command-line argument parser
def main():
    parser = argparse.ArgumentParser(description="Get OMIM clinical synopses for a gene.")
    parser.add_argument("gene_name", type=str, help="Gene symbol (e.g., CFTR)")
    args = parser.parse_args()

    gene_name = args.gene_name
    pheno_ids = get_omim_numbers(gene_name)

    for pheno_id in pheno_ids:
        result = get_clinical_synopsis(pheno_id)
        try:
            synopsis = result["omim"]["clinicalSynopsisList"][0]["clinicalSynopsis"]
            print(json.dumps(synopsis, indent=2))
        except (KeyError, IndexError) as e:
            print(f"Clinical synopsis not found for MIM {pheno_id}.")

if __name__ == "__main__":
    main()
