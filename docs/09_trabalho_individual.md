# 9. Trabalho Individual - Responsabilidades por Membro

## Estrutura da Avaliação

```
┌────────────────────────────────────────────┐
│ AVALIAÇÃO INDIVIDUAL (mesmo projeto grupo) │
├────────────────────────────────────────────┤
│ ✅ Todos trabalham no mesmo repositório    │
│ ✅ Mesmo código-fonte compartilhado       │
│ ⚠️ Cada um é responsável por 1 setor      │
│ 🔍 Questões específicas para cada membro   │
│ 📊 Demonstração individual de conhecimento │
└────────────────────────────────────────────┘
```

---

## Responsabilidades por Perfil

### 1️⃣ **MEMBRO A: Arquiteto / Lead Técnico**

**Responsabilidades:**

| Aspecto | Detalhes |
|---------|----------|
| **Infraestrutura** | Setup Docker Compose, networking |
| **Arquitetura** | Diagrama de componentes, fluxo de dados |
| **Decisões** | Trade-offs, alternativas (doc 05) |
| **Governança** | Data catalog, metadata, versionamento |
| **Monitoramento** | Health checks, logs, alertas |

**Conhecimentos Esperados:**
- Arquitetura de Big Data (Raw/Bronze/Silver/Gold)
- Docker & Kubernetes concepts
- Padrões de design (ETL, ELT)
- Lineage tracking & data governance

**Questões Específicas (Prova Oral):**
1. Explique a arquitetura em 3 camadas do pipeline
2. Por que escolheu Spark em vez de Dask?
3. Como você garantiria escalabilidade horizontal?
4. Descreva 2 pontos de falha e como mitigaria

**Entregáveis:**
- ✅ Diagrama de componentes (arquivo visual)
- ✅ Documentação de arquitetura (02_arquitetura.md)
- ✅ Decisões técnicas justificadas (05_decisoes_tecnicas.md)
- ✅ docker-compose.yml funcional

---

### 2️⃣ **MEMBRO B: Engenheiro de Dados (Ingestão)**

**Responsabilidades:**

| Aspecto | Detalhes |
|---------|----------|
| **Coleta** | Extractors, APIs, batch jobs |
| **Orquestração** | DAGs Airflow, scheduling |
| **Validação** | Schema validation, quality checks |
| **Rastreamento** | Logs, auditoria, erro handling |
| **Documentação** | Origem dos dados, dicionário (doc 04) |

**Conhecimentos Esperados:**
- Apache Airflow (DAGs, operators, triggers)
- REST APIs & HTTP requests
- Data ingestion patterns
- Error handling & retries

**Questões Específicas (Prova Oral):**
1. Como você implementaria retry automático em caso de falha de API?
2. Explique o padrão de paginação que você usou
3. Como detecta e trata duplicatas na ingestão?
4. Qual é a diferença entre batch e streaming?

**Entregáveis:**
- ✅ DAG Airflow funcional (src/ingestao/dags/)
- ✅ Extractors para múltiplas fontes
- ✅ Documentação de dados (04_dados.md)
- ✅ Validadores e quality checks

---

### 3️⃣ **MEMBRO C: Engenheiro de Dados (Processamento)**

**Responsabilidades:**

| Aspecto | Detalhes |
|---------|----------|
| **Transformação** | PySpark jobs, limpeza, enriquecimento |
| **Agregação** | Cálculos, business logic, KPIs |
| **Particionamento** | Estratégia de partição, indexação |
| **Performance** | Otimizações Spark, shuffle tuning |
| **Testes** | Unit tests para transformações |

**Conhecimentos Esperados:**
- Apache Spark (RDD, DataFrame, SQL)
- DataFrame operations (join, group by, aggregations)
- Pandas & NumPy
- Performance tuning
- Pytest & unit testing

**Questões Específicas (Prova Oral):**
1. Como você otimizaria um join entre DataFrames grandes?
2. Explique sua estratégia de particionamento
3. Como você lidaria com dados nulos em agregações?
4. Qual é a diferença entre cache() e persist()?

**Entregáveis:**
- ✅ Transformers Spark funcional (src/processamento/transformers.py)
- ✅ Testes unitários (tests/test_transformers.py)
- ✅ Documentação de transformações
- ✅ Relatório de qualidade de dados

---

### 4️⃣ **MEMBRO D: Engenheiro de API / Analytics**

**Responsabilidades:**

| Aspecto | Detalhes |
|---------|----------|
| **API REST** | Endpoints, autenticação, validação |
| **Visualização** | Metabase dashboards, queries |
| **Business Logic** | KPIs, métricas, relatórios |
| **Documentação** | Swagger/OpenAPI, user guide |
| **Testes** | Tests de API, integração |

**Conhecimentos Esperados:**
- Flask & Flask-RESTX
- RESTful API design
- SQL queries & optimization
- Metabase configuration
- API testing & mocking

**Questões Específicas (Prova Oral):**
1. Descreva os 3 principais endpoints e seus use cases
2. Como você implementaria paginação?
3. Qual é a diferença entre query parameter e path parameter?
4. Como você testaria um endpoint?

**Entregáveis:**
- ✅ API com 8+ endpoints (src/api/app.py)
- ✅ Testes de API (tests/test_api.py)
- ✅ 5+ dashboards Metabase
- ✅ Documentação Swagger automática

---

### 5️⃣ **MEMBRO E: DevOps / Infraestrutura**

**Responsabilidades:**

| Aspecto | Detalhes |
|---------|----------|
| **Containerização** | Dockerfiles, images, registry |
| **Orquestração** | Docker Compose, networking |
| **CI/CD** | Scripts de automação, testing |
| **Deployment** | Ambiente dev/prod, config management |
| **Monitoramento** | Logs, health checks, alertas |

**Conhecimentos Esperados:**
- Docker & Docker Compose
- Linux / Shell scripting
- Networking & DNS
- Environment management
- Health checks & monitoring

**Questões Específicas (Prova Oral):**
1. Como você estruturaria docker-compose.yml?
2. Explique healthchecks e dependências entre serviços
3. Como você gerenciaria secrets (.env)?
4. Como monitoraria a saúde do pipeline?

**Entregáveis:**
- ✅ docker-compose.yml completo e funcional
- ✅ Dockerfiles para cada serviço
- ✅ Scripts de setup & tear-down
- ✅ Guia de execução (08_guia_execucao.md)

---

## Matriz RACI

```
┌─────────────────────┬───┬───┬───┬───┬───┐
│ Tarefa              │ A │ B │ C │ D │ E │
├─────────────────────┼───┼───┼───┼───┼───┤
│ Arquitetura geral   │ R │ I │ I │ I │ A │
│ Ingestão dados      │ A │ R │ C │ - │ C │
│ Transformação Spark │ A │ I │ R │ - │ I │
│ API REST            │ - │ - │ - │ R │ C │
│ Dashboards          │ - │ - │ - │ R │ I │
│ Docker/Deploy       │ A │ I │ I │ I │ R │
│ Testes             │ - │ C │ R │ C │ I │
│ Documentação       │ R │ A │ A │ A │ A │
├─────────────────────┼───┼───┼───┼───┼───┤
│ Legenda:            │   │   │   │   │   │
│ R = Responsável     │   │   │   │   │   │
│ A = Accountable     │   │   │   │   │   │
│ I = Informed        │   │   │   │   │   │
│ C = Consulted       │   │   │   │   │   │
└─────────────────────┴───┴───┴───┴───┴───┘
```

---

## Avaliação Individual

### Critérios Comuns
- ✅ Código funcional e bem estruturado (25%)
- ✅ Documentação clara e completa (25%)
- ✅ Testes e cobertura (20%)
- ✅ Resposta a questões técnicas (20%)
- ✅ Colaboração e organização (10%)

### Ponderação por Papel
```
Arquiteto (A):         Arquitetura (40%) > Docs (30%) > Testes (20%)
Ingestão (B):          DAGs/Extract (40%) > Docs (30%) > Testes (20%)
Processamento (C):     Spark (40%) > Testes (30%) > Docs (20%)
API/Analytics (D):     Endpoints (40%) > Dashboards (30%) > Testes (20%)
DevOps (E):            Docker (40%) > Scripts (30%) > Docs (20%)
```

---

## Exemplo: Questão Técnica Membro B (Ingestão)

**Pergunta:**

> "Você tem uma API que retorna 50.000 transações por dia. Seu DAG Airflow começa a falhar às 6 AM porque o processamento anterior ainda não terminou. Como você resolveria?"

**Resposta Esperada:**

```
1. Identificar raiz (timeout, volume crescente)
2. Soluções:
   - Aumentar limite de tempo (default_task_call_timeout)
   - Paralelizar extractors (2+ tasks)
   - Implementar backpressure (processamento incremental)
   - Alertar se > 30min (SLA)

3. Implementação:
   - Modificar DAG para split por data/category
   - Adicionar retry com backoff exponencial
   - Registrar em DB quando terminar

4. Monitoramento:
   - Prometheus para duração de task
   - Alerta se toma > 30 min
```

---

## Repositório Git - Sugestão de Estrutura

```
main (branch principal)
├── develop (código em desenvolvimento)
├── feature/member-a-architecture (A trabalha aqui)
├── feature/member-b-ingestion (B trabalha aqui)
├── feature/member-c-processing (C trabalha aqui)
├── feature/member-d-api (D trabalha aqui)
└── feature/member-e-devops (E trabalha aqui)

Merge para main = código pronto para produção
Code review obrigatório
```

---

## Entrega Final

### Documentação (50% da nota)
- [ ] Visão geral & objetivos
- [ ] Arquitetura completa (diagramas)
- [ ] Descrição de tecnologias
- [ ] Dicionário de dados
- [ ] Decisões técnicas
- [ ] Dependências & setup
- [ ] Guia de execução
- [ ] Limitações & pontos de falha

### Código (40% da nota)
- [ ] Ingestão funcional
- [ ] Processamento funcional
- [ ] API com 8+ endpoints
- [ ] Testes (cobertura > 80%)
- [ ] Docker Compose funcional
- [ ] Logs estruturados

### Apresentação (10% da nota)
- [ ] Demonstração ao vivo (5 min por membro)
- [ ] Responde questões técnicas
- [ ] Conhecimento do seu setor

---

**Documento de Referência**
- Versão: 1.0
- Última atualização: 8 de dezembro de 2025
- Total de responsabilidades: 5 membros (até 5 participantes máximo)
