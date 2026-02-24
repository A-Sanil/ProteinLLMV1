# ProteinLLMV1 🧬

> **Protein Function Prediction using Language Models**  
> A machine learning system that predicts protein functions from amino acid sequences using a nanoGPT-based architecture with ESMFold integration.

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Overview

ProteinLLMV1 is an end-to-end protein function prediction system that combines:
- **Custom Protein Language Model** based on nanoGPT architecture
- **Pre-trained ESMFold** for structure prediction
- **Interactive Web Interface** for easy sequence analysis
- **Local Deployment** to run entirely on your laptop

### Key Features
✅ **Function Prediction**: GO terms, EC numbers, subcellular localization  
✅ **Structure Prediction**: 3D structure via ESMFold  
✅ **Batch Processing**: Analyze multiple proteins simultaneously  
✅ **Interactive Visualization**: 3D structure viewer, attention maps  
✅ **REST API**: Programmatic access to predictions  
✅ **Fast Inference**: <2 seconds per sequence  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm/yarn
- CUDA-capable GPU (recommended) or Apple Silicon Mac
- 16GB+ RAM
- 10-50GB free disk space

### Installation

#### 1. Clone the repository
```bash
cd ~/Desktop/ProteinLLMV1
```

#### 2. Set up backend
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download datasets (see data/README.md)
python data/download_data.py
```

#### 3. Set up frontend
```bash
cd ../frontend

# Install dependencies
npm install
# or
yarn install
```

#### 4. Start the application
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser! 🎉

---

## 📁 Project Structure

```
ProteinLLMV1/
├── backend/           # Python FastAPI backend
│   ├── api/           # API routes and endpoints
│   ├── ml/            # Model definitions and inference
│   ├── data/          # Data processing and datasets
│   ├── training/      # Training scripts
│   └── utils/         # Helper utilities
│
├── frontend/          # Next.js React frontend
│   └── src/
│       ├── app/       # Pages (Next.js 14 app router)
│       ├── components/# React components
│       └── lib/       # API client and utilities
│
├── data/              # Datasets (raw and processed)
├── models/            # Trained model checkpoints
├── notebooks/         # Jupyter notebooks for experiments
├── scripts/           # Automation scripts
└── docs/              # Documentation
```

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed architecture and roadmap.

---

## 🧪 Usage Examples

### Web Interface

1. **Single Prediction**
   - Go to `/predict`
   - Paste FASTA sequence or enter UniProt ID
   - Click "Predict Function"
   - View results with confidence scores

2. **Batch Processing**
   - Go to `/batch`
   - Upload CSV/FASTA file
   - Monitor progress
   - Download results

### API

```python
import requests

# Predict function
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "sequence": "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"
    }
)

prediction = response.json()
print(prediction["go_terms"])
```

### Python SDK (Coming Soon)
```python
from proteinllm import ProteinPredictor

predictor = ProteinPredictor(model_path="models/finetuned/")
result = predictor.predict("MKTAYIAK...")
print(result.go_terms)
```

---

## 📊 Performance

### Model Benchmarks (Target)
| Task | Metric | Score |
|------|--------|-------|
| GO Term Prediction | F1 (top-5) | >65% |
| EC Classification | Accuracy | >80% |
| Localization | Accuracy | >75% |

### System Performance
- **Inference**: <2 seconds per sequence
- **Structure Prediction**: 10-30 seconds (ESMFold)
- **Batch Throughput**: 50-100 sequences/minute

---

## 🛠️ Development Roadmap

### Phase 1: Foundation ✅ (Current)
- [x] Project structure
- [x] Documentation
- [ ] Environment setup
- [ ] Data acquisition

### Phase 2: Model Development (Weeks 3-4)
- [ ] Pre-training pipeline
- [ ] Fine-tuning pipeline
- [ ] Model evaluation

### Phase 3: Backend API (Week 5)
- [ ] FastAPI implementation
- [ ] Inference optimization
- [ ] ESMFold integration

### Phase 4: Frontend (Weeks 6-7)
- [ ] UI/UX design
- [ ] Core pages
- [ ] 3D visualization

### Phase 5: Integration & Testing (Week 8)
- [ ] End-to-end testing
- [ ] Documentation
- [ ] Performance optimization

### Phase 6: Deployment (Week 9)
- [ ] Docker containers
- [ ] Local deployment
- [ ] Monitoring

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete checklist.

---

## 📚 Documentation

- [**PROJECT_PLAN.md**](PROJECT_PLAN.md) - Comprehensive project plan and architecture
- [**docs/API.md**](docs/API.md) - API documentation (coming soon)
- [**docs/MODEL.md**](docs/MODEL.md) - Model architecture details (coming soon)
- [**docs/TRAINING.md**](docs/TRAINING.md) - Training guide (coming soon)
- [**docs/DEPLOYMENT.md**](docs/DEPLOYMENT.md) - Deployment guide (coming soon)

---

## 🎓 Resources

### Key Papers
1. [Biological Structure and Function Emerge from Scaling Unsupervised Learning (ESM)](https://www.pnas.org/doi/10.1073/pnas.2016239118)
2. [Language models enable zero-shot prediction of the effects of mutations](https://www.nature.com/articles/s41587-021-01146-5)
3. [Attention is All You Need (Transformers)](https://arxiv.org/abs/1706.03762)

### Repositories
- [nanoGPT by Karpathy](https://github.com/karpathy/nanoGPT)
- [ESM by Meta AI](https://github.com/facebookresearch/esm)
- [Biopython](https://biopython.org/)

### Datasets
- [UniProt](https://www.uniprot.org/)
- [Gene Ontology](http://geneontology.org/)
- [Protein Data Bank (PDB)](https://www.rcsb.org/)

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

**Project Lead**: [Your Name]  
**Email**: [your.email@example.com]  
**GitHub**: [@yourusername](https://github.com/yourusername)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Andrej Karpathy for [nanoGPT](https://github.com/karpathy/nanoGPT)
- Meta AI for ESM models
- UniProt for protein sequence database
- The open-source community

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for advancing computational biology**
