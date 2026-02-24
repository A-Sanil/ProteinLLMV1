#!/bin/bash
# Setup script for ProteinLLMV1 project
# Run this AFTER installing Python 3.10+ and Node.js 18+

set -e  # Exit on error

echo "=========================================="
echo "  ProteinLLMV1 Environment Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
python3 --version || { echo "❌ Python 3 not found! Install Python 3.10+"; exit 1; }
node --version || { echo "❌ Node.js not found! Install Node.js 18+"; exit 1; }
echo "✅ Prerequisites OK"
echo ""

# Backend setup
echo "=========================================="
echo "Setting up Backend Environment"
echo "=========================================="
cd backend

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies (this may take 5-10 minutes)..."
pip install -r requirements.txt

echo "Testing PyTorch installation..."
python -c "import torch; print(f'✅ PyTorch {torch.__version__} installed'); print(f'GPU Available: {torch.cuda.is_available()}')"

cd ..

# Frontend setup
echo ""
echo "=========================================="
echo "Setting up Frontend Environment"
echo "=========================================="
cd frontend

if [ ! -f "package.json" ]; then
    echo "Initializing Next.js project..."
    npx create-next-app@latest . --typescript --tailwind --app --no-git
fi

echo "Installing Node dependencies (this may take 3-5 minutes)..."
npm install

cd ..

# Create data directories
echo ""
echo "=========================================="
echo "Creating Data Directories"
echo "=========================================="
mkdir -p data/raw/{uniprot,go,pfam}
mkdir -p data/processed/{train,val,test}
mkdir -p models/{pretrained,finetuned}
mkdir -p backend/checkpoints
echo "✅ Directories created"

# Git initialization
echo ""
echo "=========================================="
echo "Initializing Git Repository"
echo "=========================================="
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: ProteinLLMV1 project setup"
    echo "✅ Git repository initialized"
else
    echo "⚠️ Git repository already exists"
fi

echo ""
echo "=========================================="
echo "  🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download datasets: Follow instructions in data/README.md"
echo "2. Review PROJECT_PLAN.md for architecture details"
echo "3. Check IMPLEMENTATION_CHECKLIST.md for task breakdown"
echo ""
echo "To start development:"
echo "  Backend:  cd backend && source venv/bin/activate && uvicorn api.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Happy coding! 🧬🤖"
