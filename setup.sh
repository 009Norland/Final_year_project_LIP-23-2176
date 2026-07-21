#!/usr/bin/env bash
# setup.sh — KRA-LIP one-command setup
set -e
GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${BLUE}=============================================="
echo "   KRA Legal Intelligence Platform (KRA-LIP) "
echo "   Project Setup                              "
echo -e "==============================================${NC}"

echo -e "${YELLOW}[1/5] Checking Python version...${NC}"
python3 --version

echo -e "${YELLOW}[2/5] Creating virtual environment...${NC}"
python3 -m venv venv

echo -e "${YELLOW}[3/5] Installing dependencies...${NC}"
venv/bin/pip install --upgrade pip --quiet
venv/bin/pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo -e "${YELLOW}[4/5] Downloading spaCy English model...${NC}"
venv/bin/python -m spacy download en_core_web_sm --quiet || echo "⚠️  spaCy model download failed — NER will use regex only."

echo -e "${YELLOW}[5/5] Creating .env file...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ .env created — open it and add your MongoDB Atlas URI${NC}"
else
    echo -e "${GREEN}✅ .env already exists${NC}"
fi

mkdir -p models/case_predictor models/document_intelligence data/raw data/synthetic data/processed logs

echo -e "${BLUE}=============================================="
echo "   ✅ Setup Complete!"
echo "=============================================="
echo -e "${NC}"
echo "Next steps:"
echo "  1. Add your MongoDB URI to .env  (optional — works without it)"
echo "  2. Activate venv:  source venv/bin/activate"
echo "  3. Train models:   python -m src.case_predictor.trainer"
echo "                     python -m src.document_intelligence.trainer"
echo "  4. Run dashboard:  streamlit run src/dashboard/app.py"
