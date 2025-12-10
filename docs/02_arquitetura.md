# 2. Arquitetura - Componentes e Fluxo de Dados

## Diagrama Geral de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA DO PIPELINE                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   FONTES    │    │   INGESTÃO   │    │  VALIDAÇÃO   │
│             │───▶│              │───▶│              │
│ • APIs      │    │ • Airflow    │    │ • Schema     │
│ • Arquivos  │    │ • Python     │    │ • Rules      │
│ • BD        │    │ • Schedule   │    │ • Quality    │
└─────────────┘    └──────────────┘    └──────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
              ┌──────────────┐         ┌──────────────┐       ┌──────────────┐
              │     RAW      │         │  PROCESSAMENTO│      │  ARMAZENAGEM  │
              │   (Bronze)   │         │              │       │   (MinIO)     │
              │              │         │ • Spark      │       │               │
              │ Dados Brutos │        │ • SQL        │       │ Camadas:     │
              │              │────────▶│ • Pandas     │──────▶│ Raw/Bronze   │
              │ Parquet      │         │ • Agregações │       │ Silver/Gold  │
              └──────────────┘         │              │       │              │
                                        └──────────────┘       └──────────────┘
                                                                      │
                        ┌─────────────────────────────────────────────┤
                        │                                             │
                        ▼                                             ▼
                   ┌──────────────┐                           ┌──────────────┐
                   │  DASHBOARDS  │◀──────API REST───────────│  BANCO DADOS │
                   │              │                           │              │
                   │ • Metabase   │                           │ PostgreSQL   │
                   │ • KPIs       │                           │ Metadata     │
                   │ • Relatórios │                           │              │
                   └──────────────┘                           └──────────────┘
```

## Fluxo de Dados (Pipeline)

```
1. INGESTÃO (Batch)
   ├─ Agenda: Diariamente às 2:00 AM (configurável)
   ├─ Fonte: APIs públicas, arquivos CSV, BD externo
   ├─ Formato: JSON → Parquet (compressão Snappy)
   └─ Destino: s3://raw-data/<ano>/<mes>/<dia>/

2. VALIDAÇÃO
   ├─ Verificar schema esperado
   ├─ Validar tipos de dados
   ├─ Detectar duplicatas
   ├─ Remover nulos críticos
   └─ Registrar erros em log

3. TRANSFORMAÇÃO (Spark)
   ├─ Limpeza: remove espaços, padroniza valores
   ├─ Enriquecimento: joins com dados de referência
   ├─ Agregações: cálculos de totais e médias
   ├─ Feature Engineering: cria novas colunas
   └─ Salva em Silver (dados prontos p/ análise)

4. AGREGAÇÃO FINAL (Gold)
   ├─ Views consolidadas
   ├─ KPIs calculados
   ├─ Dimensionalidade reduzida
   └─ Pronto para BI/API

5. VISUALIZAÇÃO
   ├─ Dashboard Metabase (público)
   ├─ API REST (filtros customizados)
   └─ Relatórios automatizados
```

## Camadas da Arquitetura de Dados

### 1️⃣ **Raw Layer** (Ingestão)
- **Objetivo**: Armazenar dados brutos, sem modificações
- **Formato**: Parquet (eficiência de armazenamento)
- **Retenção**: 90 dias
- **Localização**: `s3://raw-data/`
- **Exemplo**: 
  ```
  raw-data/
  ├── 2025/
  │   ├── 01/
  │   │   ├── 01/
  │   │   │   ├── api_v1_users_20250101.parquet
  │   │   │   └── api_v1_transactions_20250101.parquet
  ```

### 2️⃣ **Bronze Layer** (Validado)
- **Objetivo**: Dados validados mas ainda próximos do original
- **Transformações**: Remoção de nulos, conversão de tipos
- **Qualidade**: Schema validado
- **Localização**: `s3://bronze-data/`

### 3️⃣ **Silver Layer** (Limpo)
- **Objetivo**: Dados limpos, enriquecidos e prontos para análise
- **Transformações**: Joins, agregações, feature engineering
- **Qualidade**: Sem duplicatas, sem outliers óbvios
- **Localização**: `s3://silver-data/`
- **Exemplo**:
  ```parquet
  users_silver
  ├── user_id (PK)
  ├── name (cleaned)
  ├── created_at (standardized)
  ├── total_transactions
  ├── avg_transaction_value
  └── last_updated (timestamp)
  ```

### 4️⃣ **Gold Layer** (Análise)
- **Objetivo**: Dados finais otimizados para BI e relatórios
- **Formato**: Star schema (fatos e dimensões)
- **Localização**: `s3://gold-data/`
- **Exemplo**:
  ```
  gold-data/
  ├── facts/
  │   └── fact_transactions/
  │       └── transactions_2025.parquet
  ├── dimensions/
  │   ├── dim_users.parquet
  │   ├── dim_time.parquet
  │   └── dim_products.parquet
  ```

## Descrição da Infraestrutura

### Componentes Containerizados

```yaml
Serviços Docker:
├── minio          # Storage S3-compatible
├── postgres       # Metadata database
├── spark-master   # Orchestração Spark
├── spark-worker   # Processamento distribuído
├── metabase       # Dashboards
├── api-server     # Flask API
└── airflow        # Scheduler de jobs
```

### Especificação de Recursos

| Serviço | CPU | RAM | Disco |
|---------|-----|-----|-------|
| MinIO | 1 core | 2GB | 50GB |
| PostgreSQL | 1 core | 2GB | 20GB |
| Spark Master | 2 cores | 4GB | 10GB |
| Spark Worker | 2 cores | 4GB | 10GB |
| Metabase | 1 core | 1GB | 5GB |
| API | 1 core | 1GB | 5GB |
| **Total** | **8 cores** | **14GB** | **100GB** |

## Formato dos Dados

### Entrada (Raw)
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-01T10:30:00Z",
  "status": "active"
}
```

### Intermediário (Bronze/Silver)
```parquet
user_id    | name      | email              | created_date | is_active | _loaded_at
-----------|-----------|------------------|--------------|-----------|-------------------
123        | John Doe  | john@example.com | 2025-01-01   | true      | 2025-01-02 14:30:00
```

### Final (Gold)
```parquet
user_id | user_name | registration_year | total_orders | avg_order_value
--------|-----------|------------------|--------------|------------------
123     | John Doe  | 2025             | 42           | 150.50
```

## Governança e Qualidade de Dados

### Catalogação
- Todas as tabelas registradas no PostgreSQL com:
  - Propriedário (responsável)
  - Data de criação
  - Descrição e documentação
  - SLA de atualização

### Validação
```python
# Schema Validation
- Tipos corretos (int, string, date)
- Campos obrigatórios preenchidos
- Valores dentro de ranges válidos

# Quality Rules
- Duplicatas detectadas
- Nulos > 10% → alerta
- Outliers estatísticos identificados
```

### Versionamento
```
silver/transactions/v1/ → v2/ → v3/
Cada versão mantém histórico de mudanças
Rollback possível se necessário
```

### Lineage (Rastreamento)
```
users_raw → users_bronze → users_silver → fact_users
   ↓            ↓               ↓              ↓
 schema1      schema2        schema3      star_schema
```

---

**Documento de Referência**
- Versão: 1.0
