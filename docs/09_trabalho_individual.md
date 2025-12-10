### 1️⃣ **MEMBRO Pedro Medke: Arquiteto / DevOps / Infraestrutura**


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






### 2️⃣ **MEMBRO Olavo Tomaz : Engenheiro de Dados (Ingestão)**


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


### 3️⃣ **MEMBRO Vinícius Caires: Engenheiro de Dados (Processamento)**


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


### 4️⃣ **MEMBRO Luis Gustavo: Engenheiro de API / Analytics**


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
