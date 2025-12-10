# 8. Guia de Execução - Do Zero ao Funcionamento

## ⏱️ Tempo Estimado: 30-45 minutos

## Pré-requisitos Finais

```bash
# Verificar instalações
python --version          # >= 3.9
docker --version          # >= 20.10
docker-compose --version  # >= 2.0
git --version            # (opcional)
```

## Passo 1: Preparação do Ambiente (5 min)

### 1.1 Clone ou acesse a pasta do projeto
```bash
git clone https://github.com/PedroMedke/Projeto-Big-Data.git
```

### 1.2 Copiar arquivo de configuração
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 1.3 Editar `.env` se necessário
```bash
# Valores padrão já estão definidos, apenas customize se precisar
# ENVIRONMENT=development
# MINIO_ROOT_PASSWORD=minioadmin
# DB_PASSWORD=postgres
```

## Passo 2: Configurar Virtual Environment Python (5 min)

```bash
# Criar virtual environment
python -m venv venv

# Ativar
venv\Scripts\activate     # Windows PowerShell

# Instalar dependências
pip install -r requirements.txt

# Verificar
pip list | findstr -E "airflow|spark|flask"
```

## Passo 3: Iniciar Infraestrutura Docker (10 min)

### 3.1 Construir imagem da API (opcional, docker-compose faz isso)
```bash
# Ficar no diretório raiz do projeto
docker-compose -f infrastructure/docker-compose.yml build
```

### 3.2 Iniciar todos os serviços
```bash
# Inicia em background
docker-compose -f infrastructure/docker-compose.yml up -d

# Verificar status
docker-compose -f infrastructure/docker-compose.yml ps

# Aguardar 30-60 segundos para todos ficarem "healthy"
```

### 3.3 Verificar connectividade

```bash
# Testar MinIO
aws s3 --endpoint-url http://localhost:9000 ls

# Testar PostgreSQL
psql -h localhost -U postgres -d bigdata_project -c "SELECT 1"

# Testar API
curl http://localhost:5000/health

# Testar Spark
curl http://localhost:8080

# Testar Metabase
curl http://localhost:3000
```

## Passo 4: Criar Buckets MinIO (2 min)

```bash
# Usar AWS CLI com endpoint MinIO
# (ou acessar UI em http://localhost:9001)

aws s3 \
  --endpoint-url http://localhost:9000 \
  mb s3://raw-data

aws s3 \
  --endpoint-url http://localhost:9000 \
  mb s3://bronze-data

aws s3 \
  --endpoint-url http://localhost:9000 \
  mb s3://silver-data

aws s3 \
  --endpoint-url http://localhost:9000 \
  mb s3://gold-data

# Verificar
aws s3 --endpoint-url http://localhost:9000 ls
```

## Passo 5: Rodar Testes (5 min)

```bash
# Ativar venv se não ativado
venv\Scripts\activate

# Rodar todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src --cov-report=html

# Ver relatório
# Abrir htmlcov/index.html no navegador
```

## Passo 6: Executar Pipeline Manualmente (3 min)

### 6.1 Teste rápido de ingestão
```bash
# Executar DAG manualmente (sem Airflow scheduler)
python src/ingestao/dags/daily_pipeline.py

# Ou com Python direto
python -c "
from src.ingestao.extractors import APIExtractor
extractor = APIExtractor('https://api.example.com/users')
print('Extrator configurado OK')
"
```

### 6.2 Teste rápido de transformação
```bash
python -c "
from src.processamento.transformers import SparkTransformer
transformer = SparkTransformer('test')
print('✅ Spark configurado OK')
"
```

## Passo 7: Acessar Dashboards e APIs (2 min)

### 7.1 Metabase (Visualização)
```
URL: http://localhost:3000
Acesso: admin / admin (padrão)

Passos:
1. Conectar database PostgreSQL
2. Criar dashboards
3. Adicionar gráficos
```

### 7.2 Spark Master UI (Monitoramento)
```
URL: http://localhost:8080
Vê status dos jobs Spark
```

### 7.3 Airflow Web UI (Orquestração)
```
URL: http://localhost:8888
Usuário: admin
Senha: admin

Ativar DAG: daily_ingestao_pipeline
```

### 7.4 API REST
```bash
# Health check
curl http://localhost:5000/health

# Listar usuários
curl http://localhost:5000/api/v1/users

# Documentação Swagger
# Acesse: http://localhost:5000/api/docs
```

### 7.5 MinIO Console
```
URL: http://localhost:9001
Usuário: minioadmin
Senha: minioadmin

Vê e gerencia buckets de dados
```

## Passo 8: Visualizar Logs (Troubleshooting)

```bash
# Logs da API
docker-compose -f infrastructure/docker-compose.yml logs -f api

# Logs do Spark
docker-compose -f infrastructure/docker-compose.yml logs -f spark-master

# Logs do PostgreSQL
docker-compose -f infrastructure/docker-compose.yml logs -f postgres

# Logs locais (Python)
tail -f logs/*.log
```

## Passo 9: Parar Infraestrutura (1 min)

```bash
# Parar todos os containers
docker-compose -f infrastructure/docker-compose.yml down

# Parar e remover volumes (limpa dados)
docker-compose -f infrastructure/docker-compose.yml down -v
```

---

## Checklist de Validação

```
✅ Python 3.9+ instalado
✅ Docker rodando
✅ Virtual environment ativado
✅ Dependências instaladas (pip list)
✅ docker-compose up -d executado
✅ Todos containers "healthy"
✅ MinIO buckets criados
✅ Tests passando (pytest)
✅ API respondendo em /health
✅ Metabase acessível
✅ Airflow UI acessível
```

## Troubleshooting Rápido

### "Port 9000 already in use"
```bash
# Encontrar processo
netstat -ano | findstr :9000

# Matar processo (Windows)
taskkill /PID <PID> /F
```

### "Cannot connect to docker daemon"
```bash
# Iniciar Docker Desktop (Windows)
# Ou: systemctl start docker (Linux)
```

### "PostgreSQL connection refused"
```bash
# Aguardar initialization (até 30s)
docker-compose -f infrastructure/docker-compose.yml logs postgres

# Forçar reinicialização
docker-compose -f infrastructure/docker-compose.yml restart postgres
```

### "pyspark not found"
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

---

## Performance & Otimizações

```
Se containers estão lentos:

1. Aumentar alocação de RAM Docker:
   - Docker Desktop → Preferences → Resources
   - Mínimo: 8GB
   - Recomendado: 12GB+

2. Limpar containers/images dangling:
   docker system prune -a

3. Desativar serviços não usados:
   - Comentar em docker-compose.yml
```

---

**Documento de Referência**
- Versão: 1.0

