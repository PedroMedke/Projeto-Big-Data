# 5. Decisões Técnicas - Trade-offs e Alternativas

## Sumário Executivo

Este documento detalha as principais decisões arquiteturais, justificativas e alternativas rejeitadas.

## 1. Orquestração: Apache Airflow vs Alternativas

### Decisão: ✅ Apache Airflow 2.7.1

### Alternativas Consideradas

| Alternativa | Vantagens | Desvantagens | Por quê rejeitado? |
|-------------|-----------|-------------|-------------------|
| **Luigi** | Simples, leve | Comunidade pequena, sem UI robusta | Airflow é padrão ouro |
| **Prefect** | Moderno, cloud-native | Requer conta Prefect Cloud | Overhead para projeto local |
| **Cron Jobs** | Simples, OS-nativo | Sem rastreamento, falhas silenciosas | Não há retry/alertas |
| **Kubernetes CronJob** | Escalável | Overhead de cluster k8s | Fora do escopo local |

### Justificativa da Escolha

```
Airflow oferece:
✅ DAGs versionáveis (código como infraestrutura)
✅ UI nativa para monitoramento
✅ Retry automático e backfill
✅ Alertas por email
✅ Integração natural com Spark/Python
✅ Comunidade madura (Apache Software Foundation)
```

### Trade-offs Aceitos

| Trade-off | Impacto | Mitigação |
|-----------|--------|-----------|
| Overhead de memória | ~300MB por Airflow | Aceitável em dev local |
| Curva de aprendizado DAGs | 1-2 dias | Documentação completa |
| Não é streaming nativo | Batch only | Suficiente para requisitos |

---

## 2. Processamento: Apache Spark vs Alternativas

### Decisão: ✅ Apache Spark (PySpark)

### Análise Comparativa

| Critério | Spark | Dask | Pandas | Polars |
|----------|-------|------|--------|--------|
| Escalabilidade | Excelente (distribuído) | Boa | Limitada (memória) | Muito Boa |
| Volume de dados | 100GB+ | 10-100GB | <5GB | <10GB |
| Comunidade | Gigante | Crescendo | Enorme | Emergente |
| Produção Ready | ✅ Sim | ⚠️ Sim | ✅ Sim | ❌ Beta |
| Maturidade | 10+ anos | 5+ anos | 15+ anos | <3 anos |

### Justificativa

```
Spark escolhido porque:
✅ Big Data padrão da indústria
✅ Suporta 100GB+ nativamente
✅ RDD + DataFrame API flexível
✅ SQL via Spark SQL (HiveSQL compatible)
✅ MLlib para feature engineering
✅ Integração com Airflow/Hadoop/Cloud
```

### Alternativa Secundária: Pandas

```python
# Usado em casos específicos:
# 1. EDA (exploração inicial)
# 2. Pequenos volumes (<1GB)
# 3. Prototipagem rápida

import pandas as pd
df = pd.read_parquet('s3://silver-data/small_dataset/')
# ... análises rápidas ...
```

---

## 3. Storage: MinIO vs Alternativas

### Decisão: ✅ MinIO (S3-compatible)

### Comparação de Soluções

| Solução | Custo | Self-Hosted | Escalabilidade | Setup |
|---------|-------|------------|-----------------|-------|
| **MinIO** | 🟢 Free | ✅ Sim | Boa | 5 min |
| **AWS S3** | 🔴 $$ | ❌ Não | Excelente | Imediato |
| **Azure Blob** | 🔴 $$ | ❌ Não | Excelente | Imediato |
| **HDFS** | 🟢 Free | ✅ Sim | Excelente | 30 min |
| **Local FS** | 🟢 Free | ✅ Sim | Limitada | Imediato |

### Justificativa

```
MinIO é ideal porque:
✅ API S3 idêntica (portável para AWS depois)
✅ Open-source (sem vendor lock-in)
✅ Simples de setupar (docker run)
✅ Performance: ~100MB/s writes
✅ Replicação integrada
✅ Web UI nativa
```

### Trade-off: Performance vs Custo

```
┌─────────────────────────────────────┐
│  MinIO (local)                      │
│  Throughput: ~100 MB/s              │
│  Latency: 1-10ms                    │
│  Setup: 5 min                       │
│  Custo: $0                          │
│  Cloud Ready: Sim (migrate to S3)   │
└─────────────────────────────────────┘
```

---

## 4. Banco de Dados: PostgreSQL vs Alternativas

### Decisão: ✅ PostgreSQL 15

### Uso Específico

```
PostgreSQL para:
├── Catálogo/Metadados (datasets, execuções)
├── Tabelas Gold (Star schema para BI)
├── Cache de queries frequentes
└── Índices para Metabase

MinIO/Parquet para:
├── Raw data (bruto, imutável)
├── Bronze transformações intermediárias
└── Silver dados limpos
```

### Alternativas Rejeitadas

| DB | Por quê rejeitado? |
|----|----|
| MongoDB | Sem schema ACID; dados analíticos precisam integridade |
| MySQL | PostgreSQL é mais poderoso em análises |
| Snowflake | Proprietary, não self-hosted |
| DuckDB | Novo, melhor para local OLAP (considerado para Silver) |

---

## 5. Visualização: Metabase vs Alternativas

### Decisão: ✅ Metabase

### Análise de Alternativas

```
┌────────────────────────────────────────────────────────┐
│  Ferramenta    │ Custo │ Complexidade │ Ideal Para    │
├────────────────────────────────────────────────────────┤
│ Metabase       │ Free │ Baixa        │ Dashboards    │
│ Apache Superset│ Free │ Média        │ Dashboards    │
│ Grafana        │ Free │ Média        │ Monitoramento │
│ Tableau        │ $$$  │ Média        │ Enterprise    │
│ Power BI       │ $$   │ Baixa        │ Enterprise    │
│ Custom Plotly  │ Time │ Alta         │ Customizado   │
└────────────────────────────────────────────────────────┘
```

### Justificativa

```
Metabase escolhido porque:
✅ Completamente free (open-source)
✅ UI intuitiva (não precisa SQL)
✅ Setup: docker run em 5 min
✅ Relatórios por email automático
✅ Shareable dashboards com links públicos
✅ Conecta direto em PostgreSQL
✅ Bom suficiente para prototipagem
```

### Escalação: Se precisar Superset

```python
# Migração futura seria simples:
# 1. Export dashboards de Metabase
# 2. Recriar no Superset (mesma lógica)
# 3. Superset tem mais opções de customização
```

---

## 6. API: Flask vs FastAPI

### Decisão: ✅ Flask + Flask-RESTX

### Comparação

| Critério | Flask | FastAPI |
|----------|-------|---------|
| Documentação automática | Flask-RESTX | Nativa (Swagger) |
| Type hints | Manual | Nativo |
| Performance | Boa | Excelente |
| Complexidade | Baixa | Baixa |
| Comunidade | Madura | Crescendo |
| Async/Await | Suportado | Nativo |

### Justificativa

```
Flask escolhido porque:
✅ Simplicidade ideal para MVP
✅ Flask-RESTX oferece Swagger automático
✅ Suficiente para throughput esperado
✅ Fácil debug e testes
✅ Compatível com qualquer provider

FastAPI seria melhor se:
❌ Precisasse sub-100ms latency
❌ WebSockets/streaming real-time
❌ Milhões de requests/day
```

### Exemplo de Ambos

```python
# ======== FLASK ========
from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app)

@api.route('/users')
class Users(Resource):
    def get(self):
        return {'users': []}

# ======== FASTAPI ========
from fastapi import FastAPI

app = FastAPI()

@app.get('/users')
async def get_users():
    return {'users': []}
```

---

## 7. Containerização: Docker Compose vs Kubernetes

### Decisão: ✅ Docker Compose

### Trade-off: Simplicidade vs Escalabilidade

```
╔════════════════════════════════════════════════╗
║       DOCKER COMPOSE                          ║
║  ✅ Setup: 5 min                              ║
║  ✅ Dev/Test environment                      ║
║  ❌ Não escalável horizontalmente             ║
║  ❌ Sem self-healing                          ║
║  Ideal para: Projeto academico/MVPs           ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║       KUBERNETES                              ║
║  ❌ Setup: 1-2 horas                          ║
║  ❌ Steep learning curve                      ║
║  ✅ Escalável                                 ║
║  ✅ Prod-ready                                ║
║  Ideal para: Produção em larga escala         ║
╚════════════════════════════════════════════════╝
```

### Migração Futura

```bash
# Se precisar escalar:
1. Export docker-compose.yml
2. Use kompose (docker-compose → kubernetes)
3. Deploy em EKS/GKE/AKS
```

---

## 8. Formato de Dados: Parquet vs Alternativas

### Decisão: ✅ Parquet (Raw/Silver/Gold)

### Comparação de Formatos

```
Formato    │ Compressão │ Speed │ Versionamento │ Ideal Para
-----------|------------|-------|---------------|------------------
Parquet    │ 90%        │ Rápida│ Sim (schema)  │ Big Data, Analytics
CSV        │ 20%        │ Lento │ Não           │ Exchange, Legacy
JSON       │ 30%        │ Lento │ Sim (flexible)│ APIs, Web
ORC        │ 95%        │ Rápida│ Sim           │ Hive/Hadoop
Avro       │ 60%        │ Média │ Sim (schema)  │ Messaging (Kafka)
```

### Justificativa Parquet

```python
# Vantagens na prática:
import pandas as pd
from pyspark.sql import SparkSession

# 1. Compressão automática
df.to_parquet('file.parquet', compression='snappy')  
# Resultado: 5GB JSON → 500MB Parquet

# 2. Schema enforcement
spark.read.parquet('data/').schema
# Garante tipo de dados

# 3. Column pruning (otimização)
df.select('user_id', 'total_amount').parquet(...)
# Lê apenas 2 colunas, não 50

# 4. Predicado pushdown
df.filter(df.date > '2025-01-01').read.parquet(...)
# Filtra no nível do storage
```

---

## 9. Estratégia de Teste

### Decisão: ✅ Pytest + Coverage > 80%

### Cobertura Planejada

```
src/
├── ingestao/          [80% coverage]
│   ├── extractors/    (mocks de APIs)
│   └── validators/    (100% - crítico)
├── processamento/     [85% coverage]
│   ├── transformers/  (90% - lógica)
│   └── aggregators/   (100% - resultados)
└── api/              [75% coverage]
    ├── endpoints/    (80% - rotas)
    └── models/       (70% - validações)
```

### Exemplo de Teste

```python
import pytest
from src.processamento.transformers import clean_user_data

def test_clean_user_data_removes_nulls():
    data = {
        'user_id': [1, 2, 3],
        'name': ['Alice', None, 'Bob'],
        'email': ['a@x.com', 'b@y.com', 'c@z.com']
    }
    result = clean_user_data(data)
    assert len(result) == 2
    assert None not in result['name'].values
```

---

## 10. Governança: Versionamento de Dados

### Decisão: ✅ Versionamento Semântico (SemVer) para Data Assets

```
silver/transactions/v1.0.0/    ← Schema inicial
silver/transactions/v1.1.0/    ← Coluna nova (backward compatible)
silver/transactions/v2.0.0/    ← Mudança major (quebra contrato)
```

### Política

```
- MAJOR (v2.0.0): Muda estrutura, remove colunas
- MINOR (v1.1.0): Adiciona colunas opcionais
- PATCH (v1.0.1): Correção de dados/bug

Cada versão mantém 90 dias de histórico
Rollback automático se qualidade < 95%
```

---

## Resumo de Decisões

| Componente | Escolha | Justificativa Chave |
|-----------|---------|-------------------|
| Ingestão | Airflow | Orquestração robusta com DAGs |
| Processamento | Spark | Big Data padrão, distribuído |
| Storage | MinIO | S3-compatible, self-hosted |
| Banco | PostgreSQL | ACID, Gold layer, Metabase |
| Visualização | Metabase | Simples + free |
| API | Flask | Leve, suficiente |
| Container | Docker Compose | Dev/MVP, não produção |
| Formato | Parquet | Compressão 90%, schema |
| Testes | Pytest | Cobertura > 80% |
| Versionamento | SemVer | Rastreabilidade |

---

**Documento de Referência**
- Versão: 1.0
- Última atualização: 8 de dezembro de 2025
- Responsável: Arquiteto de Soluções
