# Prova Prática de Ciência de Dados e Big Data

Solução completa de pipeline de dados com coleta, processamento, armazenamento e visualização de insights.

## Integrantes 

Olavo Guilherme dos Santos Tomaz  - 1624543
Vinícius Caires De Souza          - 6324613
Luis Gustavo silveira pinto       - 6324670
Pedro Kommers Medke               - 6324623

## 📋 Estrutura do Projeto

```
├── docs/                 # Documentação completa
├── src/
│   ├── ingestao/        # Scripts de coleta de dados
│   ├── processamento/    # Transformações e processamento
│   ├── api/             # API para servir dados
│   └── dashboards/      # Dashboards e visualizações
├── infrastructure/      # Docker, configs de infraestrutura
├── config/             # Arquivos de configuração
├── data/               # Camadas de armazenamento
│   ├── raw/           # Dados brutos
│   ├── bronze/        # Dados validados
│   ├── silver/        # Dados transformados
│   └── gold/          # Dados finais para análise
└── tests/             # Testes unitários
```

### Pré-requisitos
- Python 3.9+
- Docker & Docker Compose
- Git

## ------------------- Inicio Rapido -------------------------------------

Pré-requisitos
Python 3.9+
Docker & Docker Compose
Git
Instalação e Execução
Clone o repositório:
git clone <seu-repo>
cd projeto-bigdata
Configure o ambiente:
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
Configure as variáveis de ambiente:
copy .env.example .env
# Edite .env com suas configurações
Inicie a infraestrutura com Docker:
docker-compose -f infrastructure/docker-compose.yml up -d
Execute o pipeline:
python src/ingestao/main.py
python src/processamento/main.py
Acesse os dashboards:
Metabase: http://localhost:3000
API: http://localhost:5000


##  Documentação

Consulte a pasta `docs/` para:
- `01_visao_geral.md` - Problema, objetivos e escopo
- `02_arquitetura.md` - Componentes e fluxo de dados
- `03_tecnologias.md` - Stack tecnológico
- `04_dados.md` - Origem, formato e dicionário
- `05_decisoes_tecnicas.md` - Trade-offs e alternativas

##  Pipeline de Dados
[Origem] → [Ingestão] → [Validação] → [Processamento] 
    ↓          ↓             ↓              ↓
  Dados      Raw         Bronze          Silver
   Brutos                                   ↓
                                         [Gold]
                                           ↓
                                    [Dashboards/API]


##  Ferramentas Principais

- **Coleta**: Python requests + Airflow (batch)
- **Processamento**: Apache Spark (PySpark)
- **Armazenamento**: MinIO (S3-compatible)
- **Análise**: Pandas, SQL
- **Visualização**: Metabase
- **Infraestrutura**: Docker Compose

##  Configuração de Dependências

Veja `docs/06_dependencias.md` para versões completas.

##  Testes

```bash
pytest tests/ -v
pytest tests/ --cov=src  # Com cobertura
```

##  Logs e Monitoramento

Logs estão em `logs/` com rotação automática.


