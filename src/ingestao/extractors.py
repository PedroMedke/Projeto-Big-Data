"""
Exemplo de extrator de dados de uma API
Integrado com Airflow para orquestração
"""

import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from config.logger import get_logger

logger = get_logger(__name__)

class APIExtractor:
    """Extrator genérico de dados via API HTTP"""
    
    def __init__(self, endpoint: str, headers: Optional[Dict] = None, timeout: int = 30):
        self.endpoint = endpoint
        self.headers = headers or {}
        self.timeout = timeout
    
    def extract(self, params: Optional[Dict] = None) -> List[Dict]:
        """
        Extrai dados da API
        
        Args:
            params: Parâmetros de query (paginação, filtros)
        
        Returns:
            Lista de dicionários com dados
        
        Raises:
            requests.RequestException: Se falha na requisição
        """
        try:
            logger.info(f"Extrating data from {self.endpoint}")
            
            response = requests.get(
                self.endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully extracted {len(data)} records")
            
            return data if isinstance(data, list) else [data]
        
        except requests.RequestException as e:
            logger.error(f"Failed to extract from API: {e}")
            raise
    
    def extract_paginated(self, page_param: str = 'page', per_page: int = 100, 
                          max_pages: Optional[int] = None) -> List[Dict]:
        """
        Extrai dados com suporte a paginação
        
        Args:
            page_param: Nome do parâmetro de página
            per_page: Registros por página
            max_pages: Número máximo de páginas (None = todas)
        
        Returns:
            Lista com todos os registros
        """
        all_data = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            try:
                params = {page_param: page, 'per_page': per_page}
                data = self.extract(params)
                
                if not data:
                    break
                
                all_data.extend(data)
                page += 1
                logger.info(f"Fetched page {page-1}, total records: {len(all_data)}")
            
            except requests.RequestException as e:
                logger.warning(f"Failed at page {page}, continuing with {len(all_data)} records")
                break
        
        return all_data

def extract_users_example():
    """
    Exemplo: Extrai usuários de uma API fictícia
    
    Fluxo de ingestão:
    1. Conecta na API
    2. Extrai dados paginados
    3. Retorna lista para processamento
    """
    extractor = APIExtractor(
        endpoint='https://api.example.com/v1/users',
        headers={'Authorization': 'Bearer token123'},
    )
    
    users = extractor.extract_paginated(max_pages=10)
    logger.info(f"Extracted {len(users)} users total")
    
    return users

def extract_transactions_example():
    """
    Exemplo: Extrai transações
    Aplicado a dados de e-commerce/fintech
    """
    extractor = APIExtractor(
        endpoint='https://api.example.com/v1/transactions',
        headers={'API-Key': 'your-api-key'}
    )
    
    # Extrai últimas 24h
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    
    transactions = extractor.extract({
        'start_date': yesterday,
        'end_date': datetime.now().isoformat()
    })
    
    logger.info(f"Extracted {len(transactions)} transactions")
    return transactions

if __name__ == '__main__':
    # Teste local
    print("Module: API Extractor (use com Airflow DAGs)")
