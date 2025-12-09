"""
DAG do Airflow para orquestar pipeline diário de ingestão
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
from pathlib import Path

# Adiciona src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configuração padrão
default_args = {
    'owner': 'bigdata-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['admin@example.com'],
}

# Definição da DAG
dag = DAG(
    'daily_ingestao_pipeline',
    default_args=default_args,
    description='Pipeline diário de ingestão de dados',
    schedule_interval='0 2 * * *',  # 2 AM todo dia
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['ingestao', 'batch', 'producao'],
)

def task_extract():
    """Task 1: Extrai dados das fontes"""
    print("✅ Iniciando extração de dados...")
    # Implementação de extração aqui
    return {'status': 'success', 'records': 10000}

def task_validate():
    """Task 2: Valida qualidade dos dados"""
    print("✅ Validando dados...")
    return {'valid': 9950, 'invalid': 50}

def task_save_raw():
    """Task 3: Salva em Raw Layer"""
    print("✅ Salvando em s3://raw-data/...")
    return {'location': 's3://raw-data/2025/01/15/'}

# Tasks
extract = PythonOperator(
    task_id='extract_data',
    python_callable=task_extract,
    dag=dag,
)

validate = PythonOperator(
    task_id='validate_data',
    python_callable=task_validate,
    dag=dag,
)

save_raw = PythonOperator(
    task_id='save_raw_layer',
    python_callable=task_save_raw,
    dag=dag,
)

notify_success = BashOperator(
    task_id='notify_success',
    bash_command='echo "✅ Ingestão completada com sucesso!"',
    dag=dag,
)

# Define dependencies
extract >> validate >> save_raw >> notify_success

if __name__ == '__main__':
    print("DAG: daily_ingestao_pipeline")
    print("Schedule: 0 2 * * * (2 AM daily)")
