# 4. Dados - Origem, Formato e Dicionário

## Origem dos Dados

### Fonte Principal
- **Nome**: [Adicione nome real]
- **Tipo**: API REST / Arquivo / Banco de Dados
- **URL/Endpoint**: https://api.example.com/v1/data
- **Frequência**: Diária (2 AM UTC)
- **Volume**: ~10.000 registros/dia (estimado)
- **Autenticação**: Bearer Token (refresh a cada 24h)

### Exemplo Real (Dados Fictícios)
```
API de E-commerce (https://api.ecommerce.example.com/v1)
├── /products       → Lista produtos
├── /users          → Lista usuários
├── /transactions   → Lista transações
└── /reviews        → Reviews de produtos
```

## Formato e Estrutura

### 1. Formato de Entrada (JSON)

```json
{
  "transaction_id": "TXN-2025-001234",
  "user_id": 5678,
  "product_id": "PROD-9012",
  "product_name": "Laptop XYZ",
  "category": "Electronics",
  "quantity": 1,
  "unit_price": 1299.99,
  "total_amount": 1299.99,
  "currency": "USD",
  "payment_method": "credit_card",
  "transaction_status": "completed",
  "transaction_date": "2025-01-15T14:30:45Z",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "user_country": "United States",
  "customer_since": "2020-06-01",
  "is_premium_member": true
}
```

### 2. Formato de Armazenamento (Parquet)

Mesmo dados acima, persistidos em Parquet (binário, comprimido):

```
File: transactions_20250115.parquet
├── Compression: Snappy
├── Row Groups: 100k rows each
├── Columns:
│   ├── transaction_id (STRING)
│   ├── user_id (INT32)
│   ├── product_id (STRING)
│   ├── quantity (INT32)
│   ├── unit_price (DECIMAL(10,2))
│   ├── total_amount (DECIMAL(10,2))
│   ├── transaction_date (TIMESTAMP)
│   ├── user_country (STRING)
│   ├── is_premium_member (BOOLEAN)
│   └── _loaded_at (TIMESTAMP - metadata)
```

**Vantagens do Parquet:**
- Compressão: 80-90% redução vs JSON
- Query-friendly: colunar, índices
- Schema enforced
- Interoperável (Spark, Pandas, Presto)

## Dicionário de Dados

### Tabela: TRANSACTIONS (Fato)

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|-------|------|-----------|---------|------------|
| transaction_id | STRING | ID único da transação | TXN-2025-001234 | ✅ |
| user_id | INT | Referência ao usuário | 5678 | ✅ |
| product_id | STRING | Referência ao produto | PROD-9012 | ✅ |
| quantity | INT | Quantidade de itens | 1 | ✅ |
| unit_price | DECIMAL(10,2) | Preço unitário | 1299.99 | ✅ |
| total_amount | DECIMAL(10,2) | Valor total (qty × price) | 1299.99 | ✅ |
| currency | STRING | Moeda ISO 4217 | USD, BRL | ✅ |
| payment_method | STRING | Método de pagamento | credit_card, pix, boleto | ✅ |
| transaction_status | STRING | Status da transação | completed, pending, failed | ✅ |
| transaction_date | TIMESTAMP | Data/hora da transação | 2025-01-15T14:30:45Z | ✅ |
| is_premium_member | BOOLEAN | Flag de membro premium | true, false | ❌ |
| _loaded_at | TIMESTAMP | Quando foi carregado | 2025-01-16T02:30:00Z | ✅ |

### Tabela: USERS (Dimensão)

| Campo | Tipo | Descrição | Exemplo | Valores Válidos |
|-------|------|-----------|---------|-----------------|
| user_id | INT | ID único | 5678 | 1-999999 |
| user_name | STRING | Nome completo | John Doe | 1-100 chars |
| user_email | STRING | Email | john@ex.com | RFC 5322 |
| user_country | STRING | País | United States | ISO 3166-1 |
| customer_since | DATE | Data cadastro | 2020-06-01 | YYYY-MM-DD |
| is_premium_member | BOOLEAN | Premium? | true | true/false |
| last_purchase_date | DATE | Última compra | 2025-01-15 | YYYY-MM-DD |
| total_spent | DECIMAL(12,2) | Total gasto | 15234.50 | >= 0 |
| account_status | STRING | Status | active | active/inactive/suspended |

### Tabela: PRODUCTS (Dimensão)

| Campo | Tipo | Descrição | Exemplo | Domínio |
|-------|------|-----------|---------|--------|
| product_id | STRING | ID único | PROD-9012 | PROD-XXXX |
| product_name | STRING | Nome | Laptop XYZ | 1-200 chars |
| category | STRING | Categoria | Electronics | predefinido |
| sub_category | STRING | Subcategoria | Computers | predefinido |
| unit_price | DECIMAL(10,2) | Preço | 1299.99 | > 0 |
| currency | STRING | Moeda | USD | ISO 4217 |
| stock_quantity | INT | Estoque | 50 | >= 0 |
| supplier | STRING | Fornecedor | TechCorp | 1-100 chars |

## Validações e Regras

### Validação de Schema (Raw → Bronze)

```python
# Tipos esperados
schema = {
    'transaction_id': 'string',
    'user_id': 'integer',
    'total_amount': 'decimal',
    'transaction_date': 'timestamp',
    'is_premium_member': 'boolean'
}

# Verificações automáticas
validations = [
    {
        'field': 'transaction_id',
        'rule': 'not_null',
        'action': 'reject_row'
    },
    {
        'field': 'total_amount',
        'rule': 'positive_value',
        'action': 'reject_row'
    },
    {
        'field': 'transaction_date',
        'rule': 'not_future',
        'action': 'flag_warning'
    }
]
```

### Regras de Negócio

```
1. Transações duplicadas (mesmo ID, user_id, timestamp)
   → Manter primeira ocorrência

2. Valores negativos em total_amount
   → Rejeitar ou converter para retorno

3. Datas inválidas (futuro > 1 dia)
   → Flag como possível erro de entrada

4. User_id não existe em dim_users
   → Rejeitar ou marcar como orphan

5. Total_amount != quantity × unit_price
   → Flag como discrepância
```

## Qualidade de Dados

### Métricas de Qualidade

| Métrica | Alvo | Ação se falhar |
|---------|------|--------|
| Completude (não-nulos) | > 95% | Investigar e pausar |
| Duplicatas | < 0.1% | Remover duplicadas |
| Schema compliance | 100% | Rejeitar batch |
| Atrasado > 1h | Alerta | Notificar time |

### Exemplo de Relatório de Qualidade

```
╔════════════════════════════════════════════════════╗
║ RELATÓRIO DE QUALIDADE - 2025-01-15               ║
╠════════════════════════════════════════════════════╣
║ Dataset: transactions                              ║
║ Período: 2025-01-15 (1 dia)                       ║
╠════════════════════════════════════════════════════╣
║ Registros totais: 8,942                           ║
║ ✅ Válidos: 8,850 (98.97%)                        ║
║ ❌ Inválidos: 92 (1.03%)                          ║
║ ⚠️ Nulos: 12 campos                               ║
║                                                    ║
║ Detalhes:                                         ║
║ - transaction_id nulo: 0                          ║
║ - total_amount negativo: 8                        ║
║ - Duplicatas: 45                                  ║
║ - Datas futuras: 0                                ║
║                                                    ║
║ Ações: Remove 92 inválidas + 45 duplicatas       ║
║ Resultado final: 8,805 registros processados      ║
╚════════════════════════════════════════════════════╝
```

## Particionamento e Indexação

### Estratégia de Particionamento

```
s3://silver-data/
├── transactions/
│   ├── year=2025/
│   │   ├── month=01/
│   │   │   ├── day=15/
│   │   │   │   ├── part-00000.parquet
│   │   │   │   └── part-00001.parquet
│   │   │   └── day=16/
│   │   │       └── ...
```

**Benefícios:**
- Queries filtradas por data são 10x mais rápidas
- Fácil deletar dados antigos (dropoff de partições)
- Processamento paralelo por partição

### Índices (PostgreSQL - tabelas agregadas)

```sql
-- Índices em Gold (para queries rápidas)
CREATE INDEX idx_users_country 
  ON dim_users(user_country);

CREATE INDEX idx_transactions_date 
  ON fact_transactions(transaction_date);

CREATE INDEX idx_products_category 
  ON dim_products(category);
```

## Lineage (Rastreamento de Origem)

```
Entrada (Raw)
    ↓
[Validação]
    ↓
Bronze Layer
    ├── transactions_raw.parquet
    │   └── _metadata.json
    │       {
    │         "source_api": "https://api.example.com",
    │         "loaded_at": "2025-01-16T02:00:00Z",
    │         "row_count": 10000,
    │         "quality_score": 98.5
    │       }
    ↓
[Transformação]
    ↓
Silver Layer
    ├── transactions_clean.parquet
    │   └── transformations.log
    │       [2025-01-16] Removed 45 duplicates
    │       [2025-01-16] Standardized currencies
    │       [2025-01-16] Joined with users dim
    ↓
[Agregação]
    ↓
Gold Layer
    ├── fact_transactions.parquet
    │   └── hash: abc123def456
    ↓
[Consumidor Final]
    └── Metabase Dashboard / API
```

---

**Documento de Referência**
- Versão: 1.0

