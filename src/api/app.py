"""
API REST com Flask para servir dados processados
Endpoints para consultas, filtros e downloads
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
import logging
from datetime import datetime
from config.logger import get_logger
from config.settings import API_HOST, API_PORT, DEBUG

logger = get_logger(__name__)

app = Flask(__name__)
CORS(app)

# API com Swagger automático
api = Api(
    app,
    version='1.0',
    title='BigData Pipeline API',
    description='API para acesso aos dados processados',
    doc='/api/docs'
)

# Namespace
ns = api.namespace('api/v1', description='v1 endpoints')

# Modelos para documentação Swagger
user_model = api.model('User', {
    'user_id': fields.Integer(description='User ID'),
    'user_name': fields.String(description='Full name'),
    'email': fields.String(description='Email address'),
    'total_purchases': fields.Integer(description='Total purchases')
})

transaction_model = api.model('Transaction', {
    'transaction_id': fields.String(description='Transaction ID'),
    'user_id': fields.Integer(description='User ID'),
    'amount': fields.Float(description='Transaction amount'),
    'transaction_date': fields.String(description='Date (ISO format)'),
    'status': fields.String(description='Status')
})

# ===== HEALTH CHECK =====
@app.route('/health')
def health_check():
    """Health check simples"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0'
    }), 200

# ===== USERS ENDPOINTS =====
@ns.route('/users')
class UserList(Resource):
    @ns.doc('get_users')
    @ns.expect(ns.parser()
        .add_argument('limit', type=int, default=100)
        .add_argument('offset', type=int, default=0)
        .add_argument('country', type=str, help='Filter by country')
    )
    @ns.marshal_list_with(user_model)
    def get(self):
        """
        Retorna lista de usuários com paginação
        
        Query parameters:
        - limit: Número máximo de registros (default: 100)
        - offset: Deslocamento (default: 0)
        - country: Filtro por país (opcional)
        """
        args = request.args
        limit = int(args.get('limit', 100))
        offset = int(args.get('offset', 0))
        country = args.get('country')
        
        logger.info(f"GET /users - limit={limit}, offset={offset}, country={country}")
        
        # Implementação: Query database
        # users = db.query(User).offset(offset).limit(limit).all()
        
        # Mock response
        return [
            {
                'user_id': 1,
                'user_name': 'John Doe',
                'email': 'john@example.com',
                'total_purchases': 42
            },
            {
                'user_id': 2,
                'user_name': 'Jane Smith',
                'email': 'jane@example.com',
                'total_purchases': 15
            }
        ], 200

@ns.route('/users/<int:user_id>')
class UserDetail(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Retorna detalhes de um usuário específico"""
        logger.info(f"GET /users/{user_id}")
        
        # Mock response
        return {
            'user_id': user_id,
            'user_name': 'John Doe',
            'email': 'john@example.com',
            'total_purchases': 42
        }, 200

# ===== TRANSACTIONS ENDPOINTS =====
@ns.route('/transactions')
class TransactionList(Resource):
    @ns.doc('get_transactions')
    @ns.expect(ns.parser()
        .add_argument('start_date', type=str, help='ISO date: 2025-01-01')
        .add_argument('end_date', type=str, help='ISO date: 2025-01-31')
        .add_argument('user_id', type=int)
        .add_argument('limit', type=int, default=1000)
    )
    @ns.marshal_list_with(transaction_model)
    def get(self):
        """
        Retorna transações com filtros
        
        Query parameters:
        - start_date: Data inicial (ISO format)
        - end_date: Data final (ISO format)
        - user_id: ID do usuário (opcional)
        - limit: Máximo de registros (default: 1000)
        """
        args = request.args
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        user_id = args.get('user_id', type=int)
        limit = int(args.get('limit', 1000))
        
        logger.info(f"GET /transactions - start={start_date}, end={end_date}, user={user_id}")
        
        # Implementação: Query database
        # transactions = db.query(Transaction).filter(...).limit(limit).all()
        
        # Mock response
        return [
            {
                'transaction_id': 'TXN-001',
                'user_id': user_id or 1,
                'amount': 299.99,
                'transaction_date': '2025-01-15T14:30:00Z',
                'status': 'completed'
            }
        ], 200

# ===== ANALYTICS ENDPOINTS =====
@ns.route('/analytics/summary')
class AnalyticsSummary(Resource):
    @ns.doc('get_summary')
    def get(self):
        """
        Retorna resumo de KPIs
        """
        logger.info("GET /analytics/summary")
        
        return {
            'total_transactions': 1245890,
            'total_revenue': 5234567.89,
            'avg_transaction': 4199.50,
            'active_users': 45280,
            'date_range': {
                'start': '2025-01-01',
                'end': '2025-01-31'
            }
        }, 200

@ns.route('/analytics/top-categories')
class TopCategories(Resource):
    @ns.doc('get_top_categories')
    @ns.expect(ns.parser().add_argument('limit', type=int, default=10))
    def get(self):
        """Retorna categorias com maior volume de vendas"""
        limit = request.args.get('limit', 10, type=int)
        logger.info(f"GET /analytics/top-categories - limit={limit}")
        
        return {
            'categories': [
                {'category': 'Electronics', 'revenue': 1234567, 'count': 2345},
                {'category': 'Clothing', 'revenue': 987654, 'count': 5678},
                {'category': 'Books', 'revenue': 456789, 'count': 3456}
            ]
        }, 200

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ===== MAIN =====
if __name__ == '__main__':
    logger.info(f"Starting API on {API_HOST}:{API_PORT}")
    logger.info(f"Swagger docs: http://{API_HOST}:{API_PORT}/api/docs")
    
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=DEBUG,
        use_reloader=False
    )
