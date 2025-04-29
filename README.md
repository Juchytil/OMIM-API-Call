# OMIM-API-Call
This Python script retrieves OMIM phenotype MIM numbers and corresponding clinical synopses for a given gene symbol using the OMIM API. It is designed for bioinformaticians, geneticists, and researchers who want to explore gene-disease relationships directly from OMIM.

## WHAT IT DOES
Given a gene symbol (e.g., CFTR), the script:
1. Queries the OMIM GeneMap API to retrieve all associated phenotype MIM numbers.
2. Uses each MIM number to fetch detailed clinical synopses.
3. Prints the clinical synopses in formatted JSON.

## REQUIREMENTS
- Python 3.7+
- Internet connection
- OMIM API key

## OMIM API Key
You must have an OMIM API key to use this script. You can get one by following the steps below.
- Register for an account: https://omim.org/register
- Request an API key here: https://omim.org/help/api
- Replace the placeholder OMIM_API_KEY in the script with your own key:

## USAGE
Run the script via command line by specifying a gene name.

example input:
python OMIM_API_call.py CFTR

example output:
{
  "mimNumber": 219700,
  "preferredTitle": "CYSTIC FIBROSIS; CF",
  "Inheritance": "Autosomal recessive",
  "Respiratory": "Recurrent respiratory infections; Chronic cough; Nasal polyps",
  "Digestive": "Pancreatic insufficiency; Meconium ileus",
  ...
}

## FUNCTION BREAKDOWN
get_omim_numbers(gene_name) – Fetches all phenotype MIM numbers related to the gene.
get_clinical_synopsis(pheno_omim_id) – Returns the clinical synopsis for a given phenotype MIM ID.
get_phenotype_map(gene_name) – Core API call to the OMIM GeneMap endpoint.
get_nested_dict(keys, dictionary) – Helper function for navigating nested JSON.

## NOTES
The script prints only the first clinical synopsis returned for each phenotype (if available).
If a clinical synopsis is not found, the script will log a message but continue.
