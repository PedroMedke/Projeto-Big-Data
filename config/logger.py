"""
Módulo de logging centralizado
Configura logs JSON estruturados
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from config.settings import LOG_DIR, LOG_LEVEL

class JSONFormatter(logging.Formatter):
    """Formatter que emite logs em JSON"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

def get_logger(name):
    """
    Obtém logger configurado com handlers para arquivo e console
    
    Args:
        name: Nome do logger (tipicamente __name__)
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Handler para arquivo (JSON)
    log_file = LOG_DIR / f"{name.split('.')[-1]}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
