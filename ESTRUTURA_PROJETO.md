# 📁 ESTRUTURA DO PROJETO - Visual Guide

```
Projeto/
│
├── 📄 Documentação Raiz
│   ├── README.md                       [Quick Start Guide]
│   ├── ENTREGA_COMPLETA.md             [Resumo Completo da Entrega]
│   ├── SUMARIO_EXECUTIVO.txt           [Executive Summary]
│   ├── requirements.txt                [Dependências Python]
│   ├── .env.example                    [Template de Configuração]
│   ├── .gitignore                      [Git Configuration]
│   ├── setup.py                        [Inicialização Windows]
│   ├── setup.sh                        [Inicialização Linux/Mac]
│   └── cleanup.py                      [Limpeza da Infraestrutura]
│
├── 📚 docs/                            [DOCUMENTAÇÃO COMPLETA]
│   ├── INDEX.md                        ← COMEÇAR AQUI
│   ├── 01_visao_geral.md               [Problema, Objetivos, Escopo]
│   ├── 02_arquitetura.md               [Componentes, Fluxo, Camadas]
│   ├── 03_tecnologias.md               [Stack Técnico, Alternativas]
│   ├── 04_dados.md                     [Origem, Schema, Dicionário]
│   ├── 05_decisoes_tecnicas.md         [Trade-offs, Justificativas]
│   ├── 06_dependencias.md              [Versões, Setup, Troubleshooting]
│   ├── 07_limitacoes.md                [Pontos de Falha, Mitigação]
│   ├── 08_guia_execucao.md             [Passo-a-Passo (40min)]
│   └── 09_trabalho_individual.md       [Responsabilidades por Membro]
│
├── 💻 src/                             [CÓDIGO-FONTE]
│   ├── __init__.py
│   │
│   ├── ingestao/                       [Coleta de Dados]
│   │   ├── __init__.py
│   │   ├── extractors.py               [APIs, Web Scraping]
│   │   └── dags/
│   │       └── daily_pipeline.py       [DAG Airflow]
│   │
│   ├── processamento/                  [Transformação]
│   │   ├── __init__.py
│   │   └── transformers.py             [Spark Jobs, Limpeza]
│   │
│   ├── api/                            [REST API]
│   │   ├── __init__.py
│   │   └── app.py                      [Flask + RESTX]
│   │
│   └── dashboards/                     [Visualização]
│       └── create_dashboards.py        [Plotly Graphs]
│
├── ⚙️ config/                          [CONFIGURAÇÕES]
│   ├── __init__.py
│   ├── settings.py                     [Config Centralizadas]
│   └── logger.py                       [Logging JSON]
│
├── 🧪 tests/                           [TESTES AUTOMATIZADOS]
│   ├── __init__.py
│   ├── test_transformers.py            [Unit Tests Spark]
│   ├── test_api.py                     [Unit Tests Flask]
│   └── test_integration.py             [Integration Tests]
│
├── 🐳 infrastructure/                  [INFRAESTRUTURA]
│   ├── docker-compose.yml              [Orquestração 7 Serviços]
│   ├── Dockerfile.api                  [Imagem Python]
│   └── init_db.sql                     [Schema PostgreSQL]
│
├── 💾 data/                            [CAMADAS DE DADOS]
│   ├── raw/                            [Dados Brutos]
│   │   └── .gitkeep
│   ├── bronze/                         [Dados Validados]
│   │   └── .gitkeep
│   ├── silver/                         [Dados Limpos]
│   │   └── .gitkeep
│   └── gold/                           [Dados Agregados]
│       └── .gitkeep
│
└── 📊 logs/                            [Logs da Aplicação]
    └── (criado em runtime)

```

---

## 📊 Visão Rápida do Conteúdo

### DOCUMENTAÇÃO (docs/)
```
01_visao_geral.md          10 min  Problema, objetivos, por quê?
02_arquitetura.md          20 min  Como tudo se conecta?
03_tecnologias.md          15 min  Quais ferramentas?
04_dados.md                20 min  Qual é a estrutura dos dados?
05_decisoes_tecnicas.md    25 min  Por que X e não Y?
06_dependencias.md         10 min  Como instalar?
07_limitacoes.md           15 min  Quais são os riscos?
08_guia_execucao.md        40 min  Como rodar? (PRÁTICO)
09_trabalho_individual.md  15 min  Qual é meu papel?
────────────────────────────────────
TOTAL: 130 min de documentação
```

### CÓDIGO (src/)
```
ingestao/
  ├─ extractors.py        Coleta via API (200 linhas)
  └─ dags/daily_pipeline.py Orquestração Airflow (50 linhas)

processamento/
  └─ transformers.py      Spark jobs (300 linhas)

api/
  └─ app.py               Flask REST (350 linhas)

dashboards/
  └─ create_dashboards.py Gráficos Plotly (150 linhas)

config/
  ├─ settings.py          Configurações (80 linhas)
  └─ logger.py            Logging (60 linhas)
────────────────────────────────────
TOTAL: ~1.200 linhas de código
```

### TESTES (tests/)
```
test_transformers.py       8 test cases     Spark
test_api.py                10 test cases    Flask
test_integration.py        7 test cases     E2E
────────────────────────────────────
TOTAL: 25+ test cases
Cobertura: >80%
```

### INFRAESTRUTURA (infrastructure/)
```
docker-compose.yml         Coordena 7 containers
├─ MinIO                   Storage
├─ PostgreSQL              Database
├─ Spark Master/Worker     Processing
├─ Metabase                Visualization
├─ API                     REST Service
└─ Airflow                 Orchestration

Dockerfile.api             Imagem Python
init_db.sql                Schema inicial
```

---

## 🎯 Como Usar Esta Estrutura

### Se quer COMEÇAR
1. Abra: `README.md`
2. Execute: `setup.py`
3. Leia: `docs/08_guia_execucao.md`

### Se quer ENTENDER TUDO
1. Leia: `docs/INDEX.md` (navigation)
2. Leia: `docs/01-09` (ordem sequencial)
3. Execute: `tests/` (validar)

### Se quer CONTRIBUIR
1. Entenda: `docs/09_trabalho_individual.md` (seu papel)
2. Modifique: `src/` (seu componente)
3. Teste: `pytest tests/` (validar)
4. Commit: `git commit` (versionar)

### Se tem PROBLEMA
1. Consulte: `docs/06_dependencias.md` (troubleshooting)
2. Consulte: `docs/07_limitacoes.md` (conhecidos)
3. Veja: `logs/` (diagnóstico)

---

## 🗂️ Tamanho dos Arquivos (Aproximado)

```
Documentação:
  docs/             ~120 KB   (9 arquivos markdown)
  README.md         ~20 KB
  ENTREGA_*.md      ~30 KB
  ────────────────────────────
  Total Docs:       ~170 KB

Código:
  src/              ~25 KB    (14 arquivos python)
  config/           ~8 KB
  tests/            ~15 KB
  ────────────────────────────
  Total Code:       ~48 KB

Infraestrutura:
  infrastructure/   ~10 KB    (3 arquivos)

Configuração:
  requirements.txt  ~2 KB
  .env*             ~2 KB
  ────────────────────────────
  Total Config:     ~4 KB

TOTAL do Projeto:  ~232 KB (comprimido: ~60 KB)
```

---

## 🔄 Fluxo de Trabalho Recomendado

```
1. PREPARAÇÃO (5 min)
   └─→ setup.py / setup.sh
       └─→ Cria venv, instala deps

2. DOCKER (5 min)
   └─→ docker-compose up -d
       └─→ 7 containers iniciam

3. VALIDAÇÃO (5 min)
   └─→ pytest tests/ -v
       └─→ 25+ testes passam

4. EXPLORAÇÃO (30 min)
   ├─→ API: http://localhost:5000/api/docs
   ├─→ Metabase: http://localhost:3000
   ├─→ Spark: http://localhost:8080
   └─→ MinIO: http://localhost:9001

5. APRENDIZADO
   └─→ Leia docs/ conforme precisar

6. CUSTOMIZAÇÃO
   ├─→ Adicione seus dados em src/
   ├─→ Modifique transformações
   ├─→ Crie novos dashboards
   └─→ Faça testes

7. ENTREGA
   └─→ git push para Bitbucket/GitHub
```

---

## 📝 Convenções do Projeto

### Nomenclatura

```
Python files:      snake_case (transformers.py)
Classes:           PascalCase (SparkTransformer)
Functions:         snake_case (extract_data)
Variables:         snake_case (raw_data)
Constants:         UPPER_CASE (DB_HOST)

Documentos:        01_tema.md (numerado)
Diretórios:        lowercase (src/, docs/, config/)
SQL scripts:       snake_case.sql (init_db.sql)
Docker files:      Dockerfile.* (Dockerfile.api)
```

### Padrões

```
Logging:           JSON estruturado (config/logger.py)
Testes:            Pytest (tests/test_*.py)
API:               RESTful com Flask-RESTX
Docker:            docker-compose.yml (único)
Versionamento:     SemVer (1.0.0)
Encoding:          UTF-8 em tudo
```

---

## ✨ Arquivos Especiais

### 📌 COMECE POR:
- `docs/INDEX.md` - Mapa de navegação
- `README.md` - Quick start
- `setup.py` - Inicialização

### 🎯 REFERÊNCIA:
- `docs/04_dados.md` - Entender dados
- `docs/09_trabalho_individual.md` - Seu papel
- `ENTREGA_COMPLETA.md` - Completo resumo

### 🔧 IMPLEMENTAÇÃO:
- `src/api/app.py` - Endpoints
- `src/processamento/transformers.py` - Lógica
- `infrastructure/docker-compose.yml` - Setup

### 🧪 VALIDAÇÃO:
- `tests/test_api.py` - Testar API
- `tests/test_transformers.py` - Testar Spark
- `pytest` - Executar tudo

---

## 🚀 Próximas Ações

1. **Esta semana:**
   - [ ] Execute setup.py
   - [ ] Rode docker-compose
   - [ ] Teste tudo (pytest)
   - [ ] Leia docs/

2. **Próxima semana:**
   - [ ] Customize com seus dados
   - [ ] Crie novos endpoints
   - [ ] Adicione transformações
   - [ ] Expanda dashboards

3. **Produção:**
   - [ ] Deploy em cloud
   - [ ] CI/CD pipeline
   - [ ] Escalabilidade
   - [ ] Monitoring

---

**Última atualização: 8 de dezembro de 2025**

