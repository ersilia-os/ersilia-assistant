disease = {"M": "Malaria",
           "T": "Tuberculosis",
           "C": "COVID-19"}

dataset = {"N": "Natural products",
           "S": "Synthetic compounds"}

objective = {"Select":"Select the best candidates for experimental testing" ,
             "Toxic": "Eliminate toxic compounds from my collection",
             "Expand": "Expand my initial collection of hits with new molecules"}

prompts = {
    ("M", "N", "Select"): "I have a collection of compounds isolated from Cameroonian plants based on traditional healer knowledge around malaria treatment. How can I identify the most promising candidates?",
    ("M", "N", "Toxic"): "How can I ensure that natural products in my collection are free from hERG toxicity and safe for CYP metabolism when designing antimalarial therapies?",
    ("M", "N", "Expand"): "I have an initial library of 30 compounds, isolated from plants with activity against P.falciparum. Can you help me expand it with new molecules that are easy to synthesize and retain the bioactivity? Scaffold hopping techniques would be useful.",
    ("M", "S", "Select"): "I want to identify synthetic compounds with high efficacy against Plasmodium falciparum, the causal agent of malaria, while prioritizing those with good solubility and permeability for initial studies.",
    ("M", "S", "Toxic"): "From an initial hit with in vitro activity against Plasmodium falciparum (IC50 < 1uM), but toxic in human cells, I have devised 100 derivatives. Which ones retain the bioactivity without causing toxicity?",
    ("M", "S", "Expand"): "How can I design new synthetic compounds for malaria treatment, particularly for drug-resistant strains, by leveraging scaffold hopping and fragment-based drug design to improve chemical diversity?",
    ("T", "N", "Select"): "I need to identify the most effective natural products for Mycobacterium tuberculosis treatment, focusing on compounds with high permeability across the bacterial membrane. What would you recommend for further investigation?",
    ("T", "N", "Toxic"): "I have curated the scientific literature for African Natural Products with potential antituberculosis activity. I want to get a full toxicity profile to annotate the compounds before moving forward.",
    ("T", "N", "Expand"): "My initial set of natural products includes compounds with activity against Mycobacterium tuberculosis. How can I explore related chemical structures to identify derivatives that improve solubility and ADME properties?",
    ("T", "S", "Select"): "I want to prioritize synthetic compounds targeting drug-resistant Mycobacterium tuberculosis strains for preclinical studies. How can I do this effectively?",
    ("T", "S", "Toxic"): "I want to use ChemDiv Diversity Set as starting library for my tuberculosis drug discovery program. Which molecules in my library are least likely to interfere with CYP3A4 metabolism while showing selective activity against Mycobacterium tuberculosis?",
    ("T", "S", "Expand"): "How can I use computational methods to propose new derivatives of synthetic hits that enhance activity against tuberculosis while maintaining good pharmacokinetics?",
    ("C", "N", "Select"): "I have access to a collection of marine natural products that may inhibit SARS-CoV-2 replication. How do I prioritize candidates for antiviral testing?",
    ("C", "N", "Toxic"): "What natural products in my library can be prioritized for COVID-19 treatment by assessing low cytotoxicity and good metabolic stability in liver microsomes?",
    ("C", "N", "Expand"): "I have manually curated the literature in search of natural products reportedly inhibiting SARS-CoV-1 and/or SARS-CoV-2. Can you help me explore the chemical space around them?", 
    ("C", "S", "Select"): "Which synthetic compounds in my library are best suited for developing antivirals targeting the SARS-CoV-2 spike protein, considering bioavailability as a key factor?",
    ("C", "S", "Toxic"): "I am at the starting point of a drug discovery campaign for COVID-19. I have a virtual library of 1M compounds. How can I filter it to ensure minimal risk of hERG toxicity while retaining antiviral activity against SARS-CoV-2?",
    ("C", "S", "Expand"): "What computational techniques can I use to design new synthetic compounds that optimize binding to SARS-CoV-2 targets while increasing diversity in my chemical library?",
}

about = [
    "This app is a demo of the Ersilia Assistant developed during the Mozilla Builders Accelerator.",
    "For more information about the Ersilia Assistant, please see code and data in this [GitHub repository](https://github.com/ersilia-os/ersilia-assistant).",
    "If you have questions or suggestions, please contact us at: [hello@ersilia.io](mailto:hello@ersilia.io)."
]
