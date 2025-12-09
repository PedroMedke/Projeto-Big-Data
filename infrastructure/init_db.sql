-- Inicialização do banco de dados PostgreSQL
-- Este script é executado automaticamente pelo postgres no startup

-- Criar tabela de catalogo de datasets
CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    owner VARCHAR(100),
    layer VARCHAR(20),  -- raw, bronze, silver, gold
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_quality_score FLOAT,
    row_count BIGINT,
    size_bytes BIGINT
);

-- Tabela de histórico de execuções
CREATE TABLE IF NOT EXISTS execution_history (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(255) NOT NULL,
    status VARCHAR(20),  -- success, failed, running, skipped
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INT,
    records_processed INT,
    records_failed INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de configurações
CREATE TABLE IF NOT EXISTS configs (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL UNIQUE,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_datasets_layer ON datasets(layer);
CREATE INDEX IF NOT EXISTS idx_execution_status ON execution_history(status);
CREATE INDEX IF NOT EXISTS idx_execution_job ON execution_history(job_name);

-- Dados iniciais
INSERT INTO configs (key, value, description) VALUES 
    ('pipeline_schedule', '0 2 * * *', 'Agendamento do pipeline diário'),
    ('data_retention_days', '90', 'Retenção de dados em dias'),
    ('quality_threshold', '0.95', 'Limiar mínimo de qualidade'),
    ('max_retry_attempts', '3', 'Número máximo de retentativas')
ON CONFLICT (key) DO NOTHING;

-- View para últimas execuções
CREATE OR REPLACE VIEW v_latest_executions AS
SELECT 
    job_name,
    status,
    start_time,
    end_time,
    EXTRACT(EPOCH FROM (end_time - start_time)) as duration_seconds,
    records_processed,
    error_message
FROM execution_history
ORDER BY start_time DESC
LIMIT 50;

GRANT SELECT ON v_latest_executions TO PUBLIC;
