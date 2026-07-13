# BioCypher Synthetic Protein Adapter

This repository contains a BioCypher adapter that transforms a synthetic
protein interaction TSV dataset into node and edge files for graph import.

The adapter follows the BioCypher adapter interface and supports:

- Protein node creation with deduplication.
- Typed protein-protein interaction edges.
- Validation of required TSV columns before processing.
- Offline file export for Neo4j bulk import.

## Repository Layout

```
.
├── create_knowledge_graph.py
├── config/
│   ├── biocypher_config.yaml
│   └── schema_config.yaml
├── src/
│   └── adapters/
│       └── adapter_synthetic_proteins.py
├── tests/
│   └── test_adapter_synthetic_proteins.py
├── pyproject.toml
└── croissant.jsonld
```

## Data Source

The pipeline downloads:

- https://zenodo.org/records/16902349/files/synthetic_protein_interactions.tsv

Expected input columns are validated in the adapter before generation:

- source, target
- source_genesymbol, target_genesymbol
- ncbi_tax_id_source, ncbi_tax_id_target
- entity_type_source, entity_type_target
- type
- is_directed, is_stimulation, is_inhibition
- consensus_direction, consensus_stimulation, consensus_inhibition

## Installation

Using uv:

```bash
uv pip install -e .
```

Install test dependencies:

```bash
uv pip install -e .[test]
```

## Usage

Run the pipeline:

```bash
python create_knowledge_graph.py
```

This generates timestamped output under:

- biocypher-out/

and logs under:

- biocypher-log/

### What gets written

- Protein nodes from unique source/target identifiers.
- Interaction edges for binding, activation, inhibition,
  phosphorylation, and ubiquitination.
- A Neo4j import helper script in the output folder.

## Testing and Validation

Run all tests:

```bash
python -m pytest -q
```

The suite in tests/test_adapter_synthetic_proteins.py covers:

- Missing-column validation failures.
- Node deduplication and shape checks.
- Edge ID uniqueness and edge field shape checks.
- Relationship integrity (edge endpoints exist as nodes).
- Integration-style checks of generated headers vs schema mappings.

## Configuration Notes

- Node and edge schema mappings are defined in config/schema_config.yaml.
- Runtime and Neo4j export settings are defined in config/biocypher_config.yaml.
- The schema uses namespace for node identifier namespace conventions.

## Troubleshooting

1. Import errors when running create_knowledge_graph.py:
Use the repository root as working directory and ensure editable install is
active.

2. Warning about edge_labels_order in log output:
Set neo4j.edge_labels_order: Leaves in config/biocypher_config.yaml to align
with Neo4j import expectations.

3. Duplicate edge type warnings:
The source dataset can emit repeated interaction classes; this is expected in
some runs and does not indicate missing labels.

4. Dataset download or cache issues:
Clear .cache and rerun to refresh downloaded resources.

## Maintenance Guide

When extending the adapter:

1. Add new required input fields to _read_tsv validation.
2. Update emitted node or edge properties in adapter_synthetic_proteins.py.
3. Synchronize schema changes in config/schema_config.yaml.
4. Add or update tests in tests/test_adapter_synthetic_proteins.py.
5. Run python -m pytest -q before committing.

## Versioning

Package metadata is maintained in pyproject.toml.
Dataset and tool metadata are described in croissant.jsonld.
