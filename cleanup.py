"""
Script para parar e limpar infraestrutura
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    print(f"▶️  {description}...")
    result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent.parent)
    if result.returncode == 0:
        print(f"✅ {description} - OK\n")
        return True
    else:
        print(f"❌ {description} - FALHOU\n")
        return False

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║  Cleanup Script - Stop Infrastructure   ║
    ╚════════════════════════════════════════╝
    """)
    
    # Parar containers
    run_command(
        "docker-compose -f infrastructure/docker-compose.yml down",
        "Parando containers"
    )
    
    # Perguntar se quer remover volumes
    response = input("""
    ⚠️  Deseja remover volumes de dados também? (S/N)
    Isso deletará: MinIO data, PostgreSQL data, logs
    """)
    
    if response.lower() in ['s', 'sim', 'yes', 'y']:
        run_command(
            "docker-compose -f infrastructure/docker-compose.yml down -v",
            "Removendo volumes"
        )
        print("🗑️  Volumes deletados!")
    
    print("""
    ✅ Infraestrutura parada!
    
    Para iniciar novamente:
    docker-compose -f infrastructure/docker-compose.yml up -d
    """)

if __name__ == '__main__':
    main()
