# Índice de Documentação - Prova Prática Big Data

## 📚 Estrutura Completa de Documentação

Este arquivo índice lista todos os documentos e referencia-cruzada as seções para fácil navegação.

---

## 1️⃣ **01_visao_geral.md** - Problema e Objetivos
- [x] Descrição do problema abordado
- [x] Objetivos do sistema (primários e secundários)
- [x] Justificativa técnica
- [x] Escopo da solução (incluído/não incluído)
- [x] Métricas de sucesso

**Leia se:** Precisa entender o "por quê" do projeto
**Tempo:** 10 min

---

## 2️⃣ **02_arquitetura.md** - Componentes e Fluxo
- [x] Diagrama geral de componentes
- [x] Fluxo de dados (Pipeline)
- [x] Camadas de dados (Raw/Bronze/Silver/Gold)
- [x] Descrição de infraestrutura
- [x] Formato dos dados (JSON → Parquet)
- [x] Governança e qualidade

**Leia se:** Precisa entender "como tudo se conecta"
**Tempo:** 20 min

---

## 3️⃣ **03_tecnologias.md** - Stack Técnico
- [x] Visão geral do stack
- [x] Detalhamento de cada componente
  - Apache Airflow (orquestração)
  - Apache Spark (processamento)
  - MinIO (storage)
  - PostgreSQL (metadata)
  - Flask (API)
  - Metabase (visualização)
- [x] Comparação com alternativas
- [x] Dependências críticas

**Leia se:** Precisa entender quais ferramentas e por quê
**Tempo:** 15 min

---

## 4️⃣ **04_dados.md** - Origem e Esquema
- [x] Origem dos dados (fonte, frequência, volume)
- [x] Formato e estrutura (JSON → Parquet)
- [x] Dicionário de dados completo
  - Tabela TRANSACTIONS
  - Tabela USERS
  - Tabela PRODUCTS
- [x] Validações e regras de negócio
- [x] Qualidade de dados
- [x] Particionamento e indexação
- [x] Lineage (rastreamento de origem)

**Leia se:** Precisa entender a estrutura dos dados
**Tempo:** 20 min

---

## 5️⃣ **05_decisoes_tecnicas.md** - Trade-offs
- [x] Decisão: Airflow vs alternativas
- [x] Decisão: Spark vs alternativas
- [x] Decisão: MinIO vs alternativas
- [x] Decisão: PostgreSQL vs alternativas
- [x] Decisão: Metabase vs alternativas
- [x] Decisão: Flask vs FastAPI
- [x] Decisão: Docker Compose vs Kubernetes
- [x] Decisão: Parquet vs alternativas
- [x] Estratégia de testes
- [x] Versionamento de dados

**Leia se:** Precisa justificar por que escolheu X e não Y
**Tempo:** 25 min

---

## 6️⃣ **06_dependencias.md** - Versões e Setup
- [x] Versões de linguagens e runtimes
- [x] Dependências Python (requirements.txt)
- [x] Variáveis de ambiente (.env)
- [x] Serviços Docker
- [x] Testes de conectividade
- [x] Checklist de pré-requisitos
- [x] Problemas comuns
- [x] Recomendações de performance

**Leia se:** Precisa instalar o projeto
**Tempo:** 10 min

---

## 7️⃣ **07_limitacoes.md** - Falhas e Pontos Críticos
- [x] Limitações de design
  - Batch (não streaming)
  - Single-node (não distribuído)
  - MinIO standalone (sem replicação)
  - Autenticação básica
  - Sem data catalog automático
- [x] Pontos de falha identificados (5 cenários)
- [x] Mitigation strategies
- [x] RTO e RPO
- [x] Recomendações de monitoramento

**Leia se:** Precisa conhecer os riscos
**Tempo:** 15 min

---

## 8️⃣ **08_guia_execucao.md** - Setup Passo a Passo
- [x] Pré-requisitos finais
- [x] Passo 1: Preparação
- [x] Passo 2: Virtual Environment
- [x] Passo 3: Docker
- [x] Passo 4: MinIO buckets
- [x] Passo 5: Testes
- [x] Passo 6: Pipeline manual
- [x] Passo 7: Acessar dashboards
- [x] Passo 8: Logs
- [x] Checklist de validação
- [x] Troubleshooting

**Leia se:** Está fazendo o setup inicial
**Tempo:** 40 min (execução)

---

## 9️⃣ **09_trabalho_individual.md** - Responsabilidades
- [x] Estrutura da avaliação
- [x] 5 Perfis com responsabilidades:
  - Membro A: Arquiteto
  - Membro B: Ingestão
  - Membro C: Processamento
  - Membro D: API/Analytics
  - Membro E: DevOps
- [x] Matriz RACI
- [x] Critérios de avaliação
- [x] Questões técnicas por perfil
- [x] Estrutura Git sugerida
- [x] Entregáveis finais

**Leia se:** É um membro do grupo e quer entender sua função
**Tempo:** 15 min

---

## 📂 Arquivos de Código

### src/ingestao/
- `extractors.py` - Coleta de dados via APIs
- `dags/daily_pipeline.py` - DAG Airflow para orquestração

### src/processamento/
- `transformers.py` - Transformações com Spark

### src/api/
- `app.py` - API REST com Flask

### src/dashboards/
- `create_dashboards.py` - Gráficos Plotly

### config/
- `settings.py` - Configurações centralizadas
- `logger.py` - Logging estruturado

### infrastructure/
- `docker-compose.yml` - Orquestração de containers
- `Dockerfile.api` - Imagem Python para API
- `init_db.sql` - Script de inicialização PostgreSQL

### tests/
- `test_transformers.py` - Testes Spark
- `test_api.py` - Testes Flask
- `test_integration.py` - Testes E2E

---

## 🔍 Como Navegar a Documentação

### Se você é:

**👨‍💼 Um Gestor**
→ Leia: 01, 02, 08

**🏗️ Um Arquiteto**
→ Leia: 01, 02, 03, 05, 07, 09

**🚰 Um Engenheiro de Dados (Ingestão)**
→ Leia: 01, 04, 06, 08, 09

**⚙️ Um Engenheiro de Dados (Processamento)**
→ Leia: 02, 03, 04, 05, 06, 09

**🌐 Um Engenheiro de API/Analytics**
→ Leia: 01, 03, 04, 08, 09

**🐳 Um DevOps**
→ Leia: 03, 06, 07, 08, 09

---

## 📋 Checklist de Leitura Completa

Para apresentação ou discussão aprofundada:

- [ ] 01_visao_geral.md (10 min)
- [ ] 02_arquitetura.md (20 min)
- [ ] 03_tecnologias.md (15 min)
- [ ] 04_dados.md (20 min)
- [ ] 05_decisoes_tecnicas.md (25 min)
- [ ] 06_dependencias.md (10 min)
- [ ] 07_limitacoes.md (15 min)
- [ ] 08_guia_execucao.md (40 min - prático)
- [ ] 09_trabalho_individual.md (15 min)
- **Total:** ~2h 40min de leitura

---

## 🔗 Cross-References Importantes

### Se quer entender um conceito:

**Data Lake / Camadas Raw/Bronze/Silver/Gold**
→ 02_arquitetura.md (seção "Camadas")

**Por que Spark e não Dask?**
→ 05_decisoes_tecnicas.md (seção "Processamento")

**Como dados fluem do Raw para Gold?**
→ 02_arquitetura.md (seção "Fluxo de Dados")

**O que é um ponto de falha?**
→ 07_limitacoes.md (seção "Pontos de Falha")

**Como rodar tudo?**
→ 08_guia_execucao.md

**Qual é minha responsabilidade?**
→ 09_trabalho_individual.md

---

## 📞 Suporte e Dúvidas

Se encontrar dúvidas em uma seção, consulte:

| Dúvida | Documento |
|--------|-----------|
| "Por que escolhemos X?" | 05_decisoes_tecnicas.md |
| "Como instalo?" | 06_dependencias.md + 08_guia_execucao.md |
| "O projeto é escalável?" | 07_limitacoes.md |
| "Quem faz o quê?" | 09_trabalho_individual.md |
| "Qual é a estrutura dos dados?" | 04_dados.md |
| "Como os componentes se conectam?" | 02_arquitetura.md |

---

## 📝 Versão e Histórico

- **Versão:** 1.0
- **Data:** 8 de dezembro de 2025
- **Total de documentos:** 9 markdown files
- **Total de código:** 11 arquivos Python
- **Total de configuração:** 5 arquivos (docker, .env, etc)
- **Total de testes:** 3 suítes com 30+ casos de teste

---

## 🎯 Próximos Passos

1. **Leia** o documento apropriado para seu perfil
2. **Execute** setup.py ou setup.sh para instalar
3. **Rodar** docker-compose up -d
4. **Teste** com pytest
5. **Explorar** http://localhost:5000/health

Boa sorte! 🚀

