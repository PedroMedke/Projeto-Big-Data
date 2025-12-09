"""
Testes unitários para API Flask
"""

import pytest
import json
from src.api.app import app

@pytest.fixture
def client():
    """Fixture: cliente de teste Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthCheck:
    """Testes de health check"""
    
    def test_health_check(self, client):
        """Testa endpoint de saúde"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'OK'
        assert 'timestamp' in data
        assert 'version' in data

class TestUserEndpoints:
    """Testes de endpoints de usuários"""
    
    def test_get_users(self, client):
        """Testa listagem de usuários"""
        response = client.get('/api/v1/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
        assert 'user_id' in data[0]
        assert 'user_name' in data[0]
    
    def test_get_users_with_pagination(self, client):
        """Testa paginação"""
        response = client.get('/api/v1/users?limit=10&offset=0')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_user_detail(self, client):
        """Testa detalhes de um usuário"""
        response = client.get('/api/v1/users/1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user_id'] == 1
        assert 'user_name' in data
        assert 'email' in data

class TestTransactionEndpoints:
    """Testes de endpoints de transações"""
    
    def test_get_transactions(self, client):
        """Testa listagem de transações"""
        response = client.get('/api/v1/transactions')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_transactions_with_filter(self, client):
        """Testa filtro por data"""
        response = client.get(
            '/api/v1/transactions?'
            'start_date=2025-01-01&end_date=2025-01-31'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_transactions_by_user(self, client):
        """Testa filtro por usuário"""
        response = client.get('/api/v1/transactions?user_id=1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

class TestAnalyticsEndpoints:
    """Testes de endpoints de análise"""
    
    def test_get_summary(self, client):
        """Testa resumo de KPIs"""
        response = client.get('/api/v1/analytics/summary')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_transactions' in data
        assert 'total_revenue' in data
        assert 'avg_transaction' in data
        assert 'active_users' in data
    
    def test_get_top_categories(self, client):
        """Testa categorias principais"""
        response = client.get('/api/v1/analytics/top-categories?limit=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'categories' in data
        assert isinstance(data['categories'], list)

class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_404_not_found(self, client):
        """Testa erro 404"""
        response = client.get('/api/v1/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_api_documentation(self, client):
        """Testa documentação Swagger"""
        response = client.get('/api/docs')
        
        assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
