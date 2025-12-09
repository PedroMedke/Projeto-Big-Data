#!/bin/bash
# Script de inicialização quick (Linux/Mac)

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  BigData Project - Quick Start (Linux/Mac)                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Verificar Python
python3 --version

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Copiar .env
cp .env.example .env

# Build Docker
docker-compose -f infrastructure/docker-compose.yml build

echo ""
echo "✅ Setup concluído!"
echo ""
echo "Próximos passos:"
echo "1. docker-compose -f infrastructure/docker-compose.yml up -d"
echo "2. Aguardar 60 segundos"
echo "3. pytest tests/ -v"
echo "4. Acessar http://localhost:5000/health"
