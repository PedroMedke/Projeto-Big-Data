"""
Arquivo de configuração centralizado para todo o projeto
Carrega variáveis do .env e fornece defaults
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# AMBIENTE
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEBUG = ENVIRONMENT == 'development'

# MinIO / S3
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER', 'minioadmin')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', MINIO_ROOT_USER)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', MINIO_ROOT_PASSWORD)
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Database
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'bigdata_project')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))
API_DEBUG = DEBUG

# Metabase
METABASE_PORT = int(os.getenv('METABASE_PORT', 3000))

# Data Paths
RAW_DATA_PATH = os.getenv('RAW_DATA_PATH', 's3://raw-data/')
BRONZE_DATA_PATH = os.getenv('BRONZE_DATA_PATH', 's3://bronze-data/')
SILVER_DATA_PATH = os.getenv('SILVER_DATA_PATH', 's3://silver-data/')
GOLD_DATA_PATH = os.getenv('GOLD_DATA_PATH', 's3://gold-data/')

# Logging
LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

print(f"✅ Config loaded: ENVIRONMENT={ENVIRONMENT}, DB={DB_HOST}:{DB_PORT}")
