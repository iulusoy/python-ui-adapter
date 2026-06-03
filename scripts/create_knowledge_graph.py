from biocypher import BioCypher, FileDownload
from template_package.adapters.adapter_synthetic_proteins import (
    AdapterNodeType,
    AdapterProteinField,
    AdapterEdgeType,
    Adapter,
)

# Create an instance of BioCypher
bc = BioCypher()

# Download the file with cache capabilities
url_dataset = (
    "https://zenodo.org/records/16902349/files/synthetic_protein_interactions.tsv"
)

resource = FileDownload(
    name="protein-protein-interaction-dataset",  # Name of the resource
    url_s=url_dataset,  # URL to the resource(s)
    lifetime=7,  # seven days cache lifetime
)
paths = bc.download(resource)  # Downloads to '.cache' by default

print(f"Path to the resouce: {paths}")


# Choose the node type you want appear in the Knowledge Graph
node_types = [AdapterNodeType.PROTEIN]

# Choose protein adapter fields to include in the knowledge graph.
node_fields = [
    AdapterProteinField.ID,
    AdapterProteinField.PREFERRED_ID,
    AdapterProteinField.GENE_SYMBOL,
    AdapterProteinField.NCBI_TAX_ID,
]

# Choose the node type you want appear in the Knowledge Graph
edge_types = [
    AdapterEdgeType.PROTEIN_PROTEIN_INTERACTION,
    AdapterEdgeType.BINDING,
    AdapterEdgeType.ACTIVATION,
    AdapterEdgeType.PHOSPHORYLATION,
    AdapterEdgeType.UBIQUITINATION,
    AdapterEdgeType.INHIBITION,
]

# (there is not code here!) Choose interaction adapter fields to include in the knowledge graph.
# By default, in case of not specifying this, BioCypher will bring all the fields defined in the adapter

# Create an adapter instance
adapter = Adapter(
    tsv_path=paths[0],
    node_types=node_types,
    node_fields=node_fields,
    edge_types=edge_types,
)

# Create a knowledge graph from the adapter
bc.write_nodes(adapter.get_nodes())
bc.write_edges(adapter.get_edges())

# Generate assets for Neo4j exportation
bc.write_import_call()

# Print a summary when
bc.summary()