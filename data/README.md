# Data Download Guide

## Overview
This directory contains the datasets needed to train and evaluate the Protein LLM. Due to their large size, datasets are not included in the repository and must be downloaded separately.

**Total Storage Required**: ~10-50GB (depending on datasets chosen)

---

## Required Datasets

### 1. UniProt Swiss-Prot (Reviewed Protein Sequences)

**Purpose**: Curated, high-quality protein sequences with functional annotations  
**Size**: ~90MB compressed, ~300MB uncompressed  
**URL**: https://www.uniprot.org/downloads

**Download Instructions**:
```bash
cd data/raw/uniprot

# Download reviewed sequences (Swiss-Prot)
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

# Extract
gunzip uniprot_sprot.fasta.gz

# Verify
wc -l uniprot_sprot.fasta
# Should see ~1.1M lines (approx. 570K sequences)
```

**Alternative**: For larger training (optional):
```bash
# Download TrEMBL (unreviewed, 240M+ sequences, ~100GB)
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz
```

### 2. Gene Ontology (GO) Annotations

**Purpose**: Functional annotations for supervised learning  
**Size**: ~500MB compressed  
**URL**: http://geneontology.org/docs/download-ontology/

**Download Instructions**:
```bash
cd data/raw/go

# Download GO ontology
wget http://purl.obolibrary.org/obo/go/go-basic.obo

# Download GO annotations for UniProt
wget http://geneontology.org/gene-associations/goa_uniprot_all.gaf.gz

# Extract
gunzip goa_uniprot_all.gaf.gz

# Verify
head goa_uniprot_all.gaf
```

### 3. Pfam Protein Families (Optional)

**Purpose**: Conserved domain identification  
**Size**: ~500MB compressed  
**URL**: https://pfam.xfam.org/

**Download Instructions**:
```bash
cd data/raw/pfam

# Download Pfam-A HMM profiles
wget http://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz

# Extract
gunzip Pfam-A.hmm.gz

# Optional: Download Pfam-A sequences
wget http://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.fasta.gz
gunzip Pfam-A.fasta.gz
```

---

## Dataset Preprocessing

After downloading the raw data, run the preprocessing scripts to create train/val/test splits:

```bash
# Activate virtual environment
cd ../../backend
source venv/bin/activate

# Run preprocessing (creates processed datasets)
python data/preprocessing.py

# Expected output:
# - data/processed/train/sequences.fasta
# - data/processed/train/labels.json
# - data/processed/val/sequences.fasta
# - data/processed/val/labels.json
# - data/processed/test/sequences.fasta
# - data/processed/test/labels.json
```

---

## Alternative: Smaller Subsets for Testing

If you want to test the pipeline without downloading full datasets:

```bash
# Create small test dataset (1000 sequences)
cd data/raw/uniprot
wget "https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=reviewed:true&size=1000" -O uniprot_sample_1k.fasta
```

---

## Dataset Structure After Preprocessing

```
data/
├── raw/
│   ├── uniprot/
│   │   └── uniprot_sprot.fasta           # ~570K sequences
│   ├── go/
│   │   ├── go-basic.obo                   # GO ontology
│   │   └── goa_uniprot_all.gaf            # GO annotations
│   └── pfam/
│       ├── Pfam-A.hmm                     # Pfam profiles
│       └── Pfam-A.fasta                   # Pfam sequences
│
└── processed/
    ├── train/                             # 80% of data
    │   ├── sequences.fasta                # Protein sequences
    │   └── labels.json                    # GO term labels
    ├── val/                               # 10% of data
    │   ├── sequences.fasta
    │   └── labels.json
    └── test/                              # 10% of data
        ├── sequences.fasta
        └── labels.json
```

---

## Data Statistics (Expected)

| Dataset | Sequences | Total Residues | Avg Length | With GO Annotations |
|---------|-----------|----------------|------------|---------------------|
| Swiss-Prot | ~570K | ~200M | ~350 AA | ~450K (~79%) |
| Train | ~456K | - | - | ~360K |
| Val | ~57K | - | - | ~45K |
| Test | ~57K | - | - | ~45K |

---

## Storage Breakdown

| Component | Size |
|-----------|------|
| Raw UniProt (Swiss-Prot) | ~300MB |
| Raw GO Annotations | ~500MB |
| Raw Pfam (optional) | ~500MB |
| Processed Datasets | ~1-2GB |
| **Total** | **~2-3GB** |

For larger datasets (TrEMBL): ~100GB+

---

## Troubleshooting

### Download Fails
If `wget` is not available, use `curl`:
```bash
curl -O https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
```

Or download manually from the URLs and place in the appropriate directories.

### Preprocessing Takes Too Long
The preprocessing script can be slow for large datasets. Use a subset for testing:
```python
# In backend/data/preprocessing.py, add:
max_sequences = 10000  # Limit to 10K sequences for testing
```

### Out of Disk Space
- Use Swiss-Prot only (skip TrEMBL)
- Skip Pfam if not needed
- Store datasets on external drive and create symlinks:
  ```bash
  ln -s /path/to/external/drive/data raw
  ```

---

## Data License & Citation

### UniProt
- **License**: CC BY 4.0
- **Citation**: UniProt Consortium (2023). "UniProt: the Universal Protein Knowledgebase in 2023." *Nucleic Acids Research*, 51(D1), D523–D531.

### Gene Ontology
- **License**: CC BY 4.0
- **Citation**: Gene Ontology Consortium (2023). "The Gene Ontology knowledgebase in 2023." *Genetics*, 224(1), iyad031.

### Pfam
- **License**: CC0 1.0 (Public Domain)
- **Citation**: Mistry et al. (2021). "Pfam: The protein families database in 2021." *Nucleic Acids Research*, 49(D1), D412–D419.

---

## Automated Download Script

For convenience, use the automated download script:

```bash
cd scripts
./download_datasets.sh
```

This script will:
1. Download all required datasets
2. Extract compressed files
3. Verify file integrity
4. Run preprocessing

**Estimated time**: 30-60 minutes (depending on internet speed)

---

**Last Updated**: February 20, 2026
