# 6. Dependências - Versões e Configurações

## Versões de Linguagens e Runtimes

```
┌─────────────────────────────────────────────────┐
│  REQUIREMENT MATRIX                             │
├─────────────────────────────────────────────────┤
│ Python          │ 3.9, 3.10, 3.11 (tested)      │
│ Apache Spark    │ 3.5.0                         │
│ Apache Airflow  │ 2.7.1                         │
│ PostgreSQL      │ 15                            │
│ Docker          │ 20.10+                        │
│ Docker Compose  │ 2.20+                         │
│ Node.js (opt)   │ 18+ (se usar JS frontend)     │
└─────────────────────────────────────────────────┘
```

## Dependências Python - requirements.txt

```
# Veja arquivo completo em requirements.txt

# Principais:
apache-airflow==2.7.1
pyspark==3.5.0
pandas==2.1.3
numpy==1.26.2
sqlalchemy==2.0.23
flask==3.0.0
minio==7.2.0
psycopg2-binary==2.9.9
plotly==5.18.0
pytest==7.4.3
```

## Variáveis de Ambiente - .env

Copiar `.`.env.example`` para ``.env`` e preencher:

```bash
# AMBIENTE
ENVIRONMENT=development  # ou production
LOG_LEVEL=INFO

# MINIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=localhost:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin

# DATABASE
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bigdata_project
DB_USER=postgres
DB_PASSWORD=postgres

# API
API_HOST=0.0.0.0
API_PORT=5000

# PATHS
RAW_DATA_PATH=s3://raw-data/
BRONZE_DATA_PATH=s3://bronze-data/
SILVER_DATA_PATH=s3://silver-data/
GOLD_DATA_PATH=s3://gold-data/
```

## Serviços Docker

### docker-compose.yml Structure

```yaml
version: '3.8'

services:
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"      # API S3
      - "9001:9001"      # Web console
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - minio_data:/minio_data
      
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  spark-master:
    image: bitnami/spark:3.5.0
    environment:
      SPARK_MODE: master
    ports:
      - "8080:8080"      # Spark UI
      - "7077:7077"      # Master port
      
  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: ${DB_NAME}
      MB_DB_PORT: ${DB_PORT}
      MB_DB_USER: ${DB_USER}
      MB_DB_PASS: ${DB_PASSWORD}
      MB_DB_HOST: postgres

volumes:
  minio_data:
  postgres_data:
```

## Testes de Conectividade

```bash
# 1. Verificar Python
python --version  # >= 3.9

# 2. Verificar Docker
docker --version
docker-compose --version

# 3. Verificar PostgreSQL
psql -h localhost -U postgres -d bigdata_project -c "SELECT 1"

# 4. Verificar MinIO
aws s3 --endpoint-url http://localhost:9000 ls

# 5. Verificar Spark
spark-submit --version

# 6. Testar importações Python
python -c "import pyspark; import pandas; import airflow; print('OK')"
```

## Checklist de Pré-requisitos

- [ ] Python 3.9+ instalado e no PATH
- [ ] Git instalado e configurado
- [ ] Docker instalado e rodando
- [ ] Docker Compose v2+
- [ ] 8GB RAM disponível (mínimo)
- [ ] 100GB espaço em disco
- [ ] Acesso à internet (para downloads)
- [ ] Terminal/Shell com suporte a bash scripts

## Problemas Comuns

### "ModuleNotFoundError: No module named 'pyspark'"

```bash
# Solução:
pip install --upgrade pyspark==3.5.0

# Ou use requirements.txt
pip install -r requirements.txt
```

### "Port 9000 is already in use"

```bash
# Verificar processo usando porta 9000
lsof -i :9000  # macOS/Linux
netstat -ano | findstr :9000  # Windows

# Mudar porta em docker-compose.yml
ports:
  - "9010:9000"  # novo mapeamento
```

### "PostgreSQL connection refused"

```bash
# Verificar container está rodando
docker-compose ps

# Ver logs
docker-compose logs postgres

# Aguardar startup (~30s)
sleep 30
```

## Performance Recommendations

```
RAM allocation (Docker Desktop):
├── Default: 2GB ❌
├── Recomendado: 8GB ✅
└── Máximo: 16GB 🚀

CPU cores:
├── Padrão: 2 cores ❌
├── Recomendado: 4 cores ✅
└── Máximo: 8 cores 🚀

Disco:
├── SSD > HDD
├── Mínimo: 50GB
└── Recomendado: 100GB+
```

---

**Documento de Referência**
- Versão: 1.0
- Última atualização: 8 de dezembro de 2025
