"""
Script de inicialização rápida do projeto
Executa setup básico automaticamente
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Executa comando e mostra status"""
    print(f"\n{'='*60}")
    print(f"▶️  {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent.parent)
    if result.returncode == 0:
        print(f"✅ {description} - OK")
        return True
    else:
        print(f"❌ {description} - FALHOU")
        return False

def main():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  BigData Project - Initialization Script                     ║
    ║  Prova Prática de Ciência de Dados e Big Data               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    checks_passed = 0
    checks_total = 7
    
    # 1. Verificar Python
    if run_command("python --version", "✓ Verificando Python 3.9+"):
        checks_passed += 1
    
    # 2. Verificar Docker
    if run_command("docker --version", "✓ Verificando Docker"):
        checks_passed += 1
    
    # 3. Criar venv
    if not (project_root / 'venv').exists():
        if run_command("python -m venv venv", "✓ Criando Virtual Environment"):
            checks_passed += 1
    else:
        print(f"✅ Virtual Environment já existe")
        checks_passed += 1
    
    # 4. Instalar dependências
    venv_python = project_root / 'venv' / 'Scripts' / 'python.exe' if sys.platform == 'win32' else project_root / 'venv' / 'bin' / 'python'
    if run_command(f"{venv_python} -m pip install -r requirements.txt", "✓ Instalando dependências"):
        checks_passed += 1
    
    # 5. Copiar .env
    if not (project_root / '.env').exists():
        import shutil
        shutil.copy(project_root / '.env.example', project_root / '.env')
        print(f"✅ Arquivo .env criado a partir de .env.example")
        checks_passed += 1
    else:
        print(f"✅ Arquivo .env já existe")
        checks_passed += 1
    
    # 6. Build Docker
    if run_command("docker-compose -f infrastructure/docker-compose.yml build", "✓ Building Docker images"):
        checks_passed += 1
    
    # 7. Informações finais
    print(f"\n{'='*60}")
    print(f"📊 RESUMO: {checks_passed}/{checks_total} verificações passaram")
    print(f"{'='*60}\n")
    
    if checks_passed == checks_total:
        print("""
        ✅ SETUP COMPLETO! Próximos passos:
        
        1. Iniciar containers:
           docker-compose -f infrastructure/docker-compose.yml up -d
        
        2. Aguardar 60 segundos para todos ficarem healthy
        
        3. Criar buckets MinIO:
           aws s3 --endpoint-url http://localhost:9000 mb s3://raw-data
           aws s3 --endpoint-url http://localhost:9000 mb s3://bronze-data
           aws s3 --endpoint-url http://localhost:9000 mb s3://silver-data
           aws s3 --endpoint-url http://localhost:9000 mb s3://gold-data
        
        4. Rodar testes:
           pytest tests/ -v
        
        5. Acessar:
           - Metabase: http://localhost:3000
           - API: http://localhost:5000/api/docs
           - Spark UI: http://localhost:8080
           - Airflow: http://localhost:8888
        
        Veja docs/08_guia_execucao.md para detalhes completos!
        """)
    else:
        print(f"""
        ⚠️  Alguns verificações falharam ({checks_passed}/{checks_total})
        
        Consulte logs acima e verifique:
        - Python >= 3.9 instalado
        - Docker Desktop rodando
        - Permissões de arquivo
        
        Veja docs/06_dependencias.md para troubleshooting
        """)

if __name__ == '__main__':
    main()
