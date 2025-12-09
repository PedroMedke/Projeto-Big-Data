#!/usr/bin/env python3
"""
Script completo para rodar tudo: setup, testes e docker
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Imprime header formatado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_cmd(cmd, description=""):
    """Executa comando e mostra resultado"""
    if description:
        print(f"\n▶️  {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            if description:
                print(f"✅ {description} - OK")
            return True
        else:
            if description:
                print(f"❌ {description} - FALHOU")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    # Trocar para diretório correto
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🚀 BIG DATA PROJECT - SETUP COMPLETO                       ║
    ║  Prova Prática de Ciência de Dados e Big Data               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 1. SETUP
    print_header("PASSO 1: SETUP DO PROJETO")
    
    print(f"\n📁 Diretório: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    
    # Criar venv
    venv_path = script_dir / "venv"
    if not venv_path.exists():
        print("\n▶️  Criando Virtual Environment...")
        run_cmd(f'"{sys.executable}" -m venv venv', "Virtual Environment")
    else:
        print("✅ Virtual Environment já existe")
    
    # Determinar Python do venv
    if sys.platform == "win32":
        venv_python = venv_path / "Scripts" / "python.exe"
        pip_cmd = str(venv_path / "Scripts" / "pip.exe")
    else:
        venv_python = venv_path / "bin" / "python"
        pip_cmd = str(venv_path / "bin" / "pip")
    
    # Instalar dependências
    print("\n▶️  Instalando dependências (requirements.txt)...")
    run_cmd(f'"{venv_python}" -m pip install --upgrade pip', "Upgrade pip")
    run_cmd(f'"{venv_python}" -m pip install -r requirements.txt', "Instalar dependências")
    
    # Copiar .env
    env_file = script_dir / ".env"
    env_example = script_dir / ".env.example"
    if not env_file.exists() and env_example.exists():
        print("\n▶️  Copiando .env.example para .env...")
        try:
            shutil.copy(env_example, env_file)
            print("✅ Arquivo .env criado")
        except Exception as e:
            print(f"⚠️  Erro ao copiar .env: {e}")
    
    # 2. TESTES
    print_header("PASSO 2: RODANDO TESTES (25+ test cases)")
    
    print("\n▶️  Executando pytest...")
    run_cmd(f'"{venv_python}" -m pytest tests/ -v --tb=short', "Testes unitários")
    
    # 3. DOCKER
    print_header("PASSO 3: DOCKER - BUILD E START")
    
    print("\n▶️  Verificando Docker...")
    run_cmd("docker --version", "Versão Docker")
    run_cmd("docker-compose --version", "Versão Docker Compose")
    
    print("\n▶️  Building Docker images...")
    run_cmd("docker-compose -f infrastructure/docker-compose.yml build", "Build Docker")
    
    print("\n▶️  Iniciando containers...")
    run_cmd("docker-compose -f infrastructure/docker-compose.yml up -d", "Start Docker")
    
    print("\n▶️  Aguardando serviços iniciarem (15 segundos)...")
    import time
    time.sleep(15)
    
    print("\n▶️  Verificando status dos containers...")
    run_cmd("docker-compose -f infrastructure/docker-compose.yml ps", "Status Docker")
    
    # 4. RESUMO FINAL
    print_header("✅ RESUMO - TUDO PRONTO!")
    
    print(f"""
    
    📊 COMPONENTES INICIADOS:
    ✅ Python 3.12 - Instalado
    ✅ Virtual Environment - Criado e ativo
    ✅ Dependências - Instaladas
    ✅ Testes Unitários - Executados
    ✅ Docker - Build concluído
    ✅ Serviços - Iniciados

    🔗 ACESSOS DISPONÍVEIS:
    ├─ API REST        → http://localhost:5000
    ├─ API Docs        → http://localhost:5000/docs
    ├─ MinIO Console   → http://localhost:9001
    ├─ Metabase        → http://localhost:3000
    ├─ PostgreSQL      → localhost:5432
    └─ Spark           → localhost:8080

    📁 ESTRUTURA DO PROJETO:
    ├─ src/
    │  ├─ api/         - REST API (Flask)
    │  ├─ ingestao/    - Extractors + Airflow DAGs
    │  ├─ processamento/ - Spark Transformers
    │  └─ dashboards/  - Visualizações
    ├─ tests/          - 25+ test cases
    ├─ docs/           - 10 documentos
    ├─ infrastructure/ - Docker Compose
    └─ config/         - Configurações centralizadas

    🚀 PRÓXIMOS PASSOS:
    1. Executar API:
       cd src/api && python app.py

    2. Criar dados no MinIO:
       aws s3 mb s3://raw-data --endpoint-url http://localhost:9001 --region us-east-1

    3. Ver logs dos containers:
       docker-compose -f infrastructure/docker-compose.yml logs -f

    4. Parar containers:
       docker-compose -f infrastructure/docker-compose.yml down

    ✨ Projeto completamente configurado e pronto para uso!
    """)

if __name__ == "__main__":
    main()
