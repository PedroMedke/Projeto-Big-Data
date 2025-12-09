# 3. Tecnologias - Stack Técnico

## Visão Geral do Stack

```
┌─────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                    │
├─────────────────────────────────────────────────────────┤
│ Linguagem       │ Python 3.9+ (principal)              │
│ Orquestração    │ Apache Airflow (batch jobs)          │
│ Processamento   │ Apache Spark (PySpark)               │
│ Storage         │ MinIO (S3-compatible) + PostgreSQL  │
│ Visualização    │ Metabase + Plotly                   │
│ API             │ Flask + Flask-RESTX                 │
│ Containerização │ Docker + Docker Compose             │
│ Testes          │ Pytest + Coverage                   │
│ Infra/DevOps    │ Docker Compose (local)              │
└─────────────────────────────────────────────────────────┘
```

## Detalhamento de Cada Componente

### 1. Ingestão de Dados

#### Apache Airflow
- **Versão**: 2.7.1
- **Função**: Orquestrar workflows de coleta de dados
- **Características**:
  - DAGs (Directed Acyclic Graphs) para definir pipelines
  - Scheduler automático com intervals configuráveis
  - Retry automático em falhas
  - Logging centralizado
  
#### Operadores Utilizados
```python
# PythonOperator: executar scripts Python
# BashOperator: executar comandos shell
# SimpleHttpOperator: chamar APIs
# S3Operator: interagir com MinIO
```

#### Exemplo de DAG Mínimo
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    'daily_ingestao',
    start_date=datetime(2025, 1, 1),
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
) as dag:
    
    def extract_data():
        # Implementação de coleta
        pass
    
    task_extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )
```

### 2. Processamento de Dados

#### Apache Spark
- **Versão**: 3.5.0
- **Modo**: Standalone (local) para desenvolvimento
- **Uso**: Transformações distribuídas de dados

#### Exemplo de Transformação
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataProcessing") \
    .getOrCreate()

# Ler dados brutos
df_raw = spark.read.parquet("s3://raw-data/")

# Transformações
df_cleaned = df_raw \
    .dropDuplicates() \
    .filter("age >= 18") \
    .withColumn("full_name", concat_ws(" ", "first_name", "last_name"))

# Salvar em Silver
df_cleaned.write.mode("overwrite").parquet("s3://silver-data/")
```

#### Padrões Utilizados
- **Lazy Evaluation**: operações são executadas apenas ao chamar `.collect()` ou `.write()`
- **Particionamento**: dados organizados por data para otimizar queries
- **Cache**: dados frequentes são mantidos em memória

### 3. Armazenamento

#### MinIO (S3-compatible)
- **Versão**: latest (docker image)
- **Função**: Data Lake com compatibilidade S3
- **Capacidade**: Escalável até terabytes
- **Buckets**:
  ```
  minio/
  ├── raw-data/        # Dados brutos
  ├── bronze-data/     # Dados validados
  ├── silver-data/     # Dados limpos
  └── gold-data/       # Dados agregados
  ```

#### PostgreSQL
- **Versão**: 15
- **Função**: Metadados, configurações, cache
- **Tabelas principais**:
  ```sql
  -- Catalogação de datasets
  CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    owner VARCHAR(100),
    last_updated TIMESTAMP,
    data_quality_score FLOAT
  );
  
  -- Histórico de execuções
  CREATE TABLE execution_history (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(255),
    status VARCHAR(20),  -- success, failed, running
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    records_processed INT
  );
  ```

### 4. API Rest

#### Flask
- **Versão**: 3.0.0
- **Framework**: Flask-RESTX para documentação automática
- **Port**: 5000
- **Endpoints**:
  ```
  GET  /api/v1/users        → Lista usuários
  GET  /api/v1/users/{id}   → Detalhe usuário
  GET  /api/v1/transactions → Transações agregadas
  POST /api/v1/queries      → Query customizada
  ```

#### Exemplo
```python
from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='BigData API')

ns = api.namespace('api/v1', description='Data endpoints')

@ns.route('/users')
class UserList(Resource):
    def get(self):
        """Lista todos os usuários"""
        # Implementação
        return {'users': []}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 5. Visualização

#### Metabase
- **Versão**: latest (docker)
- **Porta**: 3000
- **Características**:
  - Dashboards sem código
  - Conecta ao PostgreSQL para queries
  - Relatórios automáticos por email
  - Shareable links
  
#### Dashboard Exemplo
```
┌─────────────────────────────────────────┐
│   DASHBOARD: Análise de Transações     │
├─────────────────────────────────────────┤
│ [Total Transações: 142K] [Valor Médio]  │
├─────────────────────────────────────────┤
│ [Gráfico: Transações/Dia]               │
│ [Gráfico: Distribuição por Categoria]   │
├─────────────────────────────────────────┤
│ [Filtro: Data] [Filtro: Categoria]      │
└─────────────────────────────────────────┘
```

### 6. Containerização

#### Docker Compose
- **Arquivo**: `infrastructure/docker-compose.yml`
- **Serviços**: 7 containers coordenados
- **Network**: ponte interna para comunicação

```bash
# Iniciar tudo
docker-compose -f infrastructure/docker-compose.yml up -d

# Parar
docker-compose -f infrastructure/docker-compose.yml down

# Ver logs
docker-compose -f infrastructure/docker-compose.yml logs -f api
```

## Comparação com Alternativas

| Aspecto | Escolhido | Alternativa | Por quê? |
|---------|-----------|------------|---------|
| Ingestão | Airflow | Luigi, Prefect | Maduro, integrado com Spark |
| Processamento | Spark | Dask, Pandas | Distribuído, melhor p/ big data |
| Storage | MinIO | S3 AWS, GCS | Open-source, mesmo S3 API |
| DB Metadata | PostgreSQL | MySQL, MongoDB | Relacional + confiável |
| Visualização | Metabase | Tableau, Superset | Simples + free |
| API | Flask | FastAPI, Django | Leve + suficiente |

## Dependências Críticas

```
Python 3.9+ (com pip)
├── apache-airflow==2.7.1
├── pyspark==3.5.0
├── pandas==2.1.3
├── flask==3.0.0
├── minio==7.2.0
├── sqlalchemy==2.0.23
└── psycopg2==2.9.9

Docker
├── minio:latest
├── postgres:15
├── bitnami/spark:3.5.0
├── metabase/metabase:latest
└── python:3.9-slim
```

## Instalação de Dependências

```bash
# Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar
pip install -r requirements.txt

# Verificar
pip list | grep -E "airflow|spark|flask"
```

---

**Documento de Referência**
- Versão: 1.0
- Última atualização: 8 de dezembro de 2025
- Responsável: Engenheiro DevOps
