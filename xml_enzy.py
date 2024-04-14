import untangle
import pandas as pd

tree = 'full_database.xml'
obj = untangle.parse(tree)
df_drugbank_sm = pd.DataFrame(columns=["drugbank_id", "name", "enzy"])

# Iterate over drug entries to extract information
for i, drug in enumerate(obj.drugbank.drug):
    drugbank_id = None
    name = None
    enzyme_names = []  # List to store enzyme names
    
    # Get drugbank_id
    for id_tag in drug.drugbank_id:
        if id_tag['primary'] == "true":
            drugbank_id = id_tag.cdata
    
    # Drug name
    name = drug.name.cdata
    
    # Extract enzyme names from reactions
    if hasattr(drug, 'reactions') and hasattr(drug.reactions, 'reaction'):
        for reaction in drug.reactions.reaction:
            if hasattr(reaction, 'enzymes') and hasattr(reaction.enzymes, 'enzyme'):
                for enzyme in reaction.enzymes.enzyme:
                    if hasattr(enzyme, 'uniprot_id'):
                        enzyme_names.append(enzyme.uniprot_id.cdata)
    
    # Extract enzyme names from pathways
    if hasattr(drug, 'pathways') and hasattr(drug.pathways, 'pathway'):
        for pathway in drug.pathways.pathway:
            if hasattr(pathway, 'enzymes') and hasattr(pathway.enzymes, 'enzyme'):
                for enzyme in pathway.enzymes.enzyme:
                    if hasattr(enzyme, 'uniprot_id'):
                        enzyme_names.append(enzyme.uniprot_id.cdata)
    
    # Extract enzyme names from drug enzymes
    if hasattr(drug, 'enzymes') and hasattr(drug.enzymes, 'enzyme'):
        for enzyme in drug.enzymes.enzyme:
            if hasattr(enzyme, 'polypeptide'):
                enzyme_names.append(enzyme.polypeptide['id'])
    
    # Join enzyme names into a single string, separated by commas
    enzyme_names_str = ', '.join(enzyme_names)
    
    # Append the data to the DataFrame
    df_drugbank_sm.loc[i] = [drugbank_id, name, enzyme_names_str]

# Save DataFrame to a CSV file
df_drugbank_sm.to_csv('enzy_polypeptides.csv', index=None)
