# ProteinLLMV1 - Requirements & Resources List

## 🎯 Quick Reference: What You Need

### Hardware Requirements
```
Minimum:
- CPU: 4+ cores (Intel/AMD/Apple Silicon)
- RAM: 16GB
- Storage: 20GB free
- GPU: None (CPU-only mode works, just slower)

Recommended:
- CPU: 8+ cores
- RAM: 32GB
- Storage: 50GB free
- GPU: NVIDIA RTX 3060+ (8GB VRAM) or Apple M1 Pro/Max
```

### Software to Install
```bash
✓ Python 3.10 or 3.11
✓ Node.js 18+
✓ Git
✓ Docker (optional, for deployment)
✓ CUDA 11.8+ (if using NVIDIA GPU)
```

**Installation check**:
```bash
python3 --version  # Should be 3.10+
node --version     # Should be 18+
git --version      # Any recent version
```

---

## 📦 Datasets & Models

### Datasets (Total: ~2-3GB)

| Name | Size | URL | Purpose |
|------|------|-----|---------|
| **UniProt Swiss-Prot** | 300MB | https://www.uniprot.org/downloads | Protein sequences |
| **GO Annotations** | 500MB | http://geneontology.org/docs/download-ontology/ | Function labels |
| **Pfam** (optional) | 500MB | https://pfam.xfam.org/ | Domain info |

**Download commands** available in `data/README.md`

### Pre-trained Models (Auto-downloaded)

| Model | Size | Will download when |
|-------|------|-------------------|
| ESM-2 (650M) | 2.5GB | First use of ESM features (optional) |
| ESMFold | 5GB | First structure prediction |

---

## 📚 Learning Resources (Study First)

### Essential Videos (6 hours total)
1. **Andrej Karpathy - "Let's build GPT"** ⭐ MUST WATCH
   - https://www.youtube.com/watch?v=kCc8FmEb1nY
   - Duration: 2 hours
   - Why: Understand transformer architecture and nanoGPT

2. **FastAPI Tutorial**
   - https://fastapi.tiangolo.com/tutorial/
   - Duration: 1 hour
   - Why: Build REST APIs

3. **Next.js 14 Tutorial**
   - https://www.youtube.com/results?search_query=nextjs+14+tutorial
   - Duration: 2 hours
   - Why: Modern React framework

4. **Biopython Basics**
   - https://biopython.org/wiki/Biopython_Tutorial
   - Duration: 1 hour (skim)
   - Why: Parse FASTA files, manipulate sequences

### Key Papers (Read Abstracts)
1. **ESM Paper** - "Biological structure and function emerge from scaling unsupervised learning"
   - https://www.pnas.org/doi/10.1073/pnas.2016239118
   - Why: Understand protein language models

2. **Attention is All You Need**
   - https://arxiv.org/abs/1706.03762
   - Why: Transformer architecture (skip heavy math)

3. **AlphaFold 2**
   - https://www.nature.com/articles/s41586-021-03819-2
   - Why: Context on protein structure prediction

### Documentation Bookmarks
- nanoGPT: https://github.com/karpathy/nanoGPT
- PyTorch: https://pytorch.org/docs/stable/index.html
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- Biopython: https://biopython.org/wiki/Documentation
- Shadcn UI: https://ui.shadcn.com/

---

## 🛠️ Development Tools

### Code Editor
**Option 1: VS Code** (Recommended)
```bash
# Download from: https://code.visualstudio.com/

# Recommended Extensions:
- Python (Microsoft)
- Pylance
- ESLint
- Tailwind CSS IntelliSense
- Thunder Client (API testing)
```

**Option 2: PyCharm Professional**
- Better for pure Python work
- Built-in database tools

### Terminal
- **Mac**: iTerm2 (https://iterm2.com/) or built-in Terminal
- **Windows**: Windows Terminal or WSL2
- **Linux**: GNOME Terminal or Konsole

### API Testing
- **Postman**: https://www.postman.com/downloads/
- **Thunder Client**: VS Code extension
- **curl**: Command-line (already installed)

### Browser DevTools
- **Chrome**: Built-in DevTools (F12)
- **Firefox**: Built-in DevTools
- Use for frontend debugging

---

## 💻 Python Dependencies (Installed Automatically)

```
Core ML/DL:
- torch (PyTorch)
- transformers (HuggingFace)
- fair-esm (Meta ESM models)

Web Framework:
- fastapi
- uvicorn
- pydantic

Biology:
- biopython
- biotite
- prody

Data Science:
- numpy
- pandas
- scikit-learn

Utilities:
- redis (caching)
- loguru (logging)
- pytest (testing)
```

Full list in `backend/requirements.txt`

---

## 🌐 Frontend Dependencies (Installed Automatically)

```
Core:
- next (Next.js 14)
- react
- react-dom

Styling:
- tailwindcss
- @radix-ui/* (Shadcn components)

Visualization:
- molstar (3D protein viewer)
- recharts (charts)
- framer-motion (animations)

Utilities:
- axios (API requests)
- zustand (state management)
- react-hook-form (forms)
- zod (validation)
```

Full list in `frontend/package.json` (created during setup)

---

## 📊 Estimated Costs

| Item | Cost |
|------|------|
| Hardware | $0 (use existing laptop) |
| Software | $0 (all open-source) |
| Cloud GPU (optional) | ~$0.50/hour (Google Colab Pro, Paperspace) |
| Domain name (optional) | ~$10/year |
| Cloud hosting (optional) | ~$20-50/month (if deploying public) |
| **Total (local only)** | **$0** |
| **Total (with cloud)** | **$30-70/month** |

---

## ⏱️ Time Investment

### Development Time (Part-time)
| Phase | Duration | Hours/Week | Total Hours |
|-------|----------|------------|-------------|
| Learning Prerequisites | 1 week | 10 | 10 |
| Setup & Data | 1-2 weeks | 12 | 24 |
| Model Training | 2 weeks | 15 | 30 |
| Backend API | 1 week | 18 | 18 |
| Frontend | 2 weeks | 18 | 36 |
| Testing & Polish | 2 weeks | 12 | 24 |
| **Total** | **10 weeks** | **15/week** | **~150 hours** |

### Training Time (Compute)
| Task | GPU | CPU-only |
|------|-----|----------|
| Pre-training (100K sequences) | 3-7 days | 2-4 weeks |
| Fine-tuning | 1-2 days | 3-5 days |
| Inference (per sequence) | <1 second | 2-5 seconds |

---

## 🎯 Skill Prerequisites

### Required
- ✅ **Python basics**: Functions, classes, file I/O
- ✅ **Command line**: cd, ls, pip, git
- ✅ **Basic ML concepts**: Training, evaluation, overfitting
- ✅ **Web basics**: HTTP requests, JSON, APIs

### Helpful (But Can Learn)
- 🟡 PyTorch or TensorFlow
- 🟡 React or other frontend framework
- 🟡 Biology (proteins, DNA, amino acids)
- 🟡 Databases and caching

### Will Learn During Project
- 🟢 Transformers and attention mechanism
- 🟢 Protein bioinformatics
- 🟢 FastAPI and async Python
- 🟢 Next.js and modern React
- 🟢 Docker and deployment

---

## 📁 Project Files Created

```
✓ PROJECT_PLAN.md              - Full architecture & roadmap
✓ README.md                    - Project overview
✓ IMPLEMENTATION_CHECKLIST.md  - Task-by-task guide
✓ GETTING_STARTED.md          - Quick start & summary
✓ REQUIREMENTS_LIST.md        - This file
✓ backend/requirements.txt     - Python dependencies
✓ data/README.md              - Dataset download guide
✓ scripts/setup_environment.sh - Automated setup
✓ .gitignore                   - Git ignore rules
✓ Folder structure (backend/, frontend/, data/, etc.)
```

---

## 🚀 Quick Start Commands

### 1. Setup (First Time Only)
```bash
cd ~/Desktop/ProteinLLMV1
./scripts/setup_environment.sh
```

### 2. Download Data
```bash
# See data/README.md for commands
cd data/raw/uniprot
wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
gunzip uniprot_sprot.fasta.gz
```

### 3. Start Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn api.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🆘 Common Issues & Solutions

### Issue: Python version too old
```bash
# Mac (using Homebrew)
brew install python@3.11

# Linux
sudo apt update
sudo apt install python3.11
```

### Issue: GPU not detected
```bash
# Check CUDA
nvidia-smi

# Install PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Issue: Out of memory during training
**Solution**: Reduce batch size in `backend/training/configs/pretrain_config.yaml`
```yaml
training:
  batch_size: 32  # Reduce from 64
```

### Issue: Frontend won't start
```bash
# Clear cache
rm -rf frontend/.next
rm -rf frontend/node_modules
cd frontend && npm install
```

### Issue: Dataset download fails
- Try `curl -O <URL>` instead of `wget`
- Or download manually from browser and move to `data/raw/`

---

## 🎓 Additional Learning Resources

### Courses (Free)
- Fast.ai Practical Deep Learning: https://course.fast.ai/
- DeepLearning.AI Transformers: https://www.deeplearning.ai/
- Full Stack Open (Next.js): https://fullstackopen.com/

### Books (Optional)
- "Deep Learning for Coders" by Jeremy Howard
- "Hands-On Machine Learning" by Aurélien Géron
- "Bioinformatics Data Skills" by Vince Buffalo

### Communities
- Reddit: r/bioinformatics, r/MachineLearning, r/learnprogramming
- Discord: TDS AI Community, LearnProgramming
- Stack Overflow: Tag [pytorch], [fastapi], [next.js]

---

## ✅ Pre-Launch Checklist

Before you start coding:
- [ ] Read `GETTING_STARTED.md` fully
- [ ] Watch Karpathy's GPT video
- [ ] Install Python 3.10+, Node.js 18+, Git
- [ ] Run `./scripts/setup_environment.sh`
- [ ] Download datasets (or small subset)
- [ ] Clone nanoGPT: `git clone https://github.com/karpathy/nanoGPT.git`
- [ ] Open `IMPLEMENTATION_CHECKLIST.md`
- [ ] Start with Phase 1, Task 1

---

## 🎉 You're Ready!

Everything you need is now in this folder:
```
~/Desktop/ProteinLLMV1/
```

**Next steps**:
1. Read `GETTING_STARTED.md` (10 min)
2. Run setup script (30 min)
3. Follow `IMPLEMENTATION_CHECKLIST.md` task-by-task

**Questions?**
- Check `PROJECT_PLAN.md` for detailed answers
- Search GitHub issues in nanoGPT/ESM repos
- Ask on relevant subreddits

---

**Good luck! You've got this. 🚀🧬**

---

**Last Updated**: February 20, 2026
