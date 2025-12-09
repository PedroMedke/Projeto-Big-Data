# 7. Limitações e Pontos de Falha

## Limitações de Design

### 1. Processamento em Batch (Não Streaming)

**Limitação:**
- Dados processados 1x por dia (2 AM)
- Latência entre ingestão e visualização: ~24h

**Impacto:**
- ❌ Não é real-time
- ✅ Suficiente para análises operacionais
- ✅ Reduz complexidade

**Mitigation:**
```
Se precisar real-time depois:
1. Integrar Kafka para streaming
2. Usar Spark Structured Streaming
3. Metabase refresh mais frequente (10 min)
```

### 2. Single-Node Spark (Não Distribuído)

**Limitação:**
- Spark roda em modo local (1 máquina)
- Volume máximo: ~100GB com 8GB RAM

**Impacto:**
- ❌ Não escalável para PB-scale
- ✅ Suficiente para datasets < 50GB
- ✅ Mais simples de manter

**Escalação:**
```
Cluster Spark (requer +50h setup):
├── Spark Master (1 node)
├── Spark Workers (N nodes)
├── HDFS ou S3 (storage distribuído)
└── Yarn/Mesos (resource manager)
```

### 3. Armazenamento MinIO (Não Distribuído)

**Limitação:**
- MinIO roda em modo standalone
- Sem replicação entre nós
- Sem erasure coding (alta disponibilidade)

**Impacto:**
- ❌ Sem backup automático
- ❌ Ponto único de falha
- ✅ Adequate para desenvolvimento

**Backup Policy:**
```bash
# Backup manual semanal
aws s3 sync s3://raw-data/ ./backup/raw --endpoint-url http://localhost:9000

# Ou use snapshots do container volume
docker cp <container>:/minio_data ./backup/
```

### 4. Autenticação Básica

**Limitação:**
- Sem LDAP/OAuth
- Senhas em .env (não seguro em prod)
- Sem granularidade de permissões por usuário

**Impacto:**
- ❌ Não adequado para produção
- ✅ Suficiente para ambiente educacional

**Upgrade Futuro:**
```
1. Keycloak (open-source OAuth provider)
2. LDAP integration (Airflow + Metabase)
3. Vault (gerenciar secrets)
```

### 5. Documentação Manual em Markdown

**Limitação:**
- Sem data catalog automático (tipo Apache Atlas)
- Sem lineage tracking visual

**Impacto:**
- ⚠️ Requer manutenção manual
- ✅ Simples + versionável no Git

**Upgrade:**
```
Integrar OpenMetadata:
├── Descoberta automática de datasets
├── Lineage visual
├── Data quality SLAs
└── Glossário de negócio
```

---

## Pontos de Falha Identificados

### 1️⃣ Falha na Ingestão (API externa cai)

```
Cenário: https://api.example.com retorna 500

┌──────────────┐
│ Airflow DAG  │─────────────────┐
└──────────────┘                 │
        │                        │
        ▼                        ▼
┌──────────────────┐     ┌──────────────┐
│ Extract (1a vez) │────▶│ API CAIA ❌  │
│ Retry x3         │     └──────────────┘
└──────────────────┘
        │
        ▼
    FALHA
        │
        ▼
┌──────────────────────────┐
│ Email alerta enviado     │
│ Humano investiga manual  │
│ Reprocessa quando API OK │
└──────────────────────────┘

Tempo de recuperação: ~1-2 horas
```

**Mitigation:**

```python
# src/ingestao/main.py
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

@apply_defaults
def extract_with_retry(endpoint, max_retries=3, backoff=300):
    """
    Tenta 3x com backoff exponencial
    Falhas registradas em logs para análise
    """
    import requests
    import time
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                endpoint,
                timeout=30,
                headers={'User-Agent': 'BigDataPipeline/1.0'}
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                logger.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {wait_time}s")
                time.sleep(wait_time)
            else:
                logger.error(f"All {max_retries} attempts failed for {endpoint}")
                raise AirflowException(f"Failed to extract from {endpoint}")
```

### 2️⃣ Falha na Transformação (Dados Inválidos)

```
Cenário: Dados chegam com schema diferente

Raw Data:
{
  "id": "ABC123",        ← Esperava INT
  "amount": "1299.99",   ← Esperava DECIMAL
  "date": "2025-01-15"   ← OK
}

Resultado:
┌────────────────────────────┐
│ Spark Schema Validation    │
│ Error: Invalid int "ABC123"│
└────────────────────────────┘
        │
        ▼
    FALHA
        │
        ├─► Log em: logs/transformacao_20250115.log
        ├─► Tabela quarentena criada
        ├─► Dados descartados
        └─► Alerta enviado
```

**Mitigation:**

```python
# src/processamento/validators.py
from pydantic import BaseModel, validator
from typing import Optional

class TransactionSchema(BaseModel):
    id: str
    amount: float
    date: str
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Amount must be positive')
        return v
    
    @validator('date')
    def date_must_be_valid(cls, v):
        from datetime import datetime
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError('Invalid date format')
        return v

def validate_batch(df):
    """Valida dataframe em lote"""
    errors = []
    for idx, row in df.iterrows():
        try:
            TransactionSchema(**row.to_dict())
        except ValueError as e:
            errors.append({'row': idx, 'error': str(e)})
    
    if errors:
        # Salvar em tabela quarentena
        df_invalid = df.iloc[[e['row'] for e in errors]]
        df_invalid.to_parquet('s3://quarantine/invalid_20250115.parquet')
        logger.warning(f"Found {len(errors)} invalid rows")
    
    # Retorna apenas válidas
    return df.drop([e['row'] for e in errors])
```

### 3️⃣ Falha no Armazenamento (MinIO offline)

```
Cenário: Docker container MinIO cai

Processamento Spark tenta escrever para S3:
┌────────────────────────┐
│ Spark write_parquet()  │
│ Destination: s3://gold │
└────────────────────────┘
        │
        ▼
┌────────────────────────────────┐
│ Connection to localhost:9000   │
│ ERROR: Connection refused ❌   │
└────────────────────────────────┘
        │
        ▼
   FALHA (sem retry automático)
        │
        ├─► Dados em memória perdidos
        ├─► Job falha
        └─► Precisa reprocessar tudo
```

**Mitigation:**

```bash
# docker-compose.yml - Health checks
services:
  minio:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
      start_period: 60s
    restart: unless-stopped  # ← Reinicia automático

# src/processamento/storage.py - Client com retry
from botocore.exceptions import ClientError
import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
    stop=tenacity.stop_after_attempt(3),
    reraise=True
)
def write_to_s3(df, bucket, path):
    """Escreve com retry automático"""
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    try:
        df.to_parquet(f"s3://{bucket}/{path}")
        logger.info(f"Successfully wrote to s3://{bucket}/{path}")
    except ClientError as e:
        logger.error(f"Failed to write to S3: {e}")
        raise
```

### 4️⃣ Falha no Banco de Dados (PostgreSQL offline)

```
Cenário: Metabase tenta conectar em PostgreSQL que caiu

Impacto:
├─ Dashboards mostram "Connection Error"
├─ Relatórios agendados não rodam
└─ API falha se consultar banco
```

**Mitigation:**

```bash
# docker-compose.yml
postgres:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 10s
    timeout: 5s
    retries: 5
  restart: unless-stopped
```

### 5️⃣ Falha de Espaço em Disco

```
Cenário: Disco atingiu 100% de uso

Causas possíveis:
├─ Logs crescendo infinitamente
├─ MinIO acumulando dados
└─ Cache do Spark não limpando

Sintomas:
├─ Ingestão falha ("No space left on device")
├─ Spark crashes
└─ Metabase fica lento
```

**Mitigation:**

```bash
# Limpeza automática em docker-compose.yml
services:
  minio:
    volumes:
      - minio_data:/minio_data
      # Limpar a cada 7 dias de arquivos > 30 dias
    command: |
      server /minio_data --lifecycle-days=30

# Logrotate em Linux
/var/log/bigdata-pipeline/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 root root
}

# Limpeza manual Spark cache
from pyspark.context import SparkContext
spark.catalog.clearCache()
```

---

## RTO e RPO

```
┌──────────────────────────────────────────┐
│  Recovery Objectives                      │
├──────────────────────────────────────────┤
│ Componente  │ RTO (Recovery Time)         │
├─────────────┼─────────────────────────────┤
│ MinIO       │ 30 min (restart + restore)  │
│ PostgreSQL  │ 15 min (restart)            │
│ Spark       │ 5 min (rerun job)           │
│ Metabase    │ 2 min (restart)             │
│ API/Flask   │ 1 min (restart)             │
├──────────────────────────────────────────┤
│ Componente  │ RPO (Recovery Point)        │
├─────────────┼─────────────────────────────┤
│ Raw Data    │ 1 dia (última ingestão ok)  │
│ Bronze      │ 1 dia (transformação)       │
│ Silver/Gold │ 1 dia (processos)           │
└──────────────────────────────────────────┘
```

---

## Recomendações de Monitoramento

```python
# monitoring/health_check.py
import requests
import psycopg2
from minio import Minio

def check_all_services():
    """Monitora saúde de todos os serviços"""
    health = {}
    
    # MinIO
    try:
        minio = Minio("localhost:9000", ...)
        minio.list_buckets()
        health['minio'] = 'OK'
    except:
        health['minio'] = 'DOWN'
    
    # PostgreSQL
    try:
        conn = psycopg2.connect("dbname=bigdata_project user=postgres")
        conn.close()
        health['postgres'] = 'OK'
    except:
        health['postgres'] = 'DOWN'
    
    # Metabase
    try:
        r = requests.get("http://localhost:3000/api/health", timeout=5)
        health['metabase'] = 'OK' if r.status_code == 200 else 'DOWN'
    except:
        health['metabase'] = 'DOWN'
    
    # API
    try:
        r = requests.get("http://localhost:5000/health", timeout=5)
        health['api'] = 'OK' if r.status_code == 200 else 'DOWN'
    except:
        health['api'] = 'DOWN'
    
    return health

# Executar a cada 5 min via cron
if __name__ == '__main__':
    health = check_all_services()
    print(health)
    # Enviar alertas se algum estiver DOWN
```

---

**Documento de Referência**
- Versão: 1.0
- Última atualização: 8 de dezembro de 2025
- Responsável: SRE/DevOps
