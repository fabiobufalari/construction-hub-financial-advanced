"""
Construction Hub Financial Advanced Service
Enterprise Financial Analytics and Risk Management Platform
Plataforma Empresarial de Análise Financeira e Gerenciamento de Riscos

This service provides advanced financial analytics, risk management,
and reporting capabilities specifically designed for construction companies.
Este serviço fornece análises financeiras avançadas, gerenciamento de riscos,
e capacidades de relatórios especificamente projetadas para empresas de construção.

Features / Funcionalidades:
- Advanced Financial Analytics Engine / Motor de Análise Financeira Avançada
- Risk Management System / Sistema de Gerenciamento de Riscos
- Financial Reporting Advanced / Relatórios Financeiros Avançados
- Integration Hub for all microservices / Hub de Integração para todos os microserviços
- Real-time financial monitoring / Monitoramento financeiro em tempo real
- Predictive analytics for cash flow / Análises preditivas para fluxo de caixa
- Project profitability analysis / Análise de rentabilidade de projetos
- Canadian banking integration / Integração bancária canadense

Canadian Compliance / Conformidade Canadense:
- SOX (Sarbanes-Oxley Act)
- PIPEDA (Personal Information Protection and Electronic Documents Act)
- AODA (Accessibility for Ontarians with Disabilities Act)
- FINTRAC (Financial Transactions and Reports Analysis Centre of Canada)
"""

import os
import sys
# DON'T CHANGE THIS !!! / NÃO ALTERE ISSO !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, g, request
from flask_cors import CORS
from src.models.financial_models import db
from src.services.audit_service import AuditService, audit_required
from src.services.config_service import ConfigService
from src.routes.analytics import analytics_bp
from src.routes.risk_management import risk_bp
from src.routes.reporting import reporting_bp
from src.routes.integration import integration_bp
import logging
from datetime import datetime

# Initialize Flask application / Inicializar aplicação Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = ConfigService.SECURITY_CONFIG['jwt_secret_key']

# Enable CORS for all routes with frontend URL / Habilitar CORS para todas as rotas com URL do frontend
CORS(app, origins=[
    ConfigService.FRONTEND_BASE_URL,
    "http://localhost:3000",  # Development / Desenvolvimento
    "http://localhost:8081"   # Alternative port / Porta alternativa
])

# Configure logging / Configurar logging
logging.basicConfig(
    level=getattr(logging, ConfigService.LOGGING_CONFIG['level']),
    format=ConfigService.LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

# Register blueprints / Registrar blueprints
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(risk_bp, url_prefix='/api/risk')
app.register_blueprint(reporting_bp, url_prefix='/api/reporting')
app.register_blueprint(integration_bp, url_prefix='/api/integration')

# Database configuration / Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = ConfigService.get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': ConfigService.DATABASE_CONFIG['pool_size'],
    'pool_timeout': ConfigService.DATABASE_CONFIG['pool_timeout'],
    'pool_recycle': ConfigService.DATABASE_CONFIG['pool_recycle']
}

# Initialize database / Inicializar banco de dados
db.init_app(app)

# Create tables / Criar tabelas
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully / Tabelas do banco de dados criadas com sucesso")
    except Exception as e:
        logger.error(f"Failed to create database tables / Falha ao criar tabelas do banco de dados: {str(e)}")

@app.before_request
def before_request():
    """
    Pre-request processing for audit and security
    Processamento pré-requisição para auditoria e segurança
    """
    # Set request start time for performance monitoring
    # Definir tempo de início da requisição para monitoramento de performance
    g.request_start_time = datetime.utcnow()
    
    # Extract user information from headers (set by authentication service)
    # Extrair informações do usuário dos cabeçalhos (definido pelo serviço de autenticação)
    g.user_id = request.headers.get('X-User-ID', 'anonymous')
    g.user_email = request.headers.get('X-User-Email')
    g.session_id = request.headers.get('X-Session-ID')
    
    # Log request if audit is enabled / Registrar requisição se auditoria estiver habilitada
    if ConfigService.is_audit_enabled() and ConfigService.AUDIT_CONFIG['log_all_requests']:
        logger.info(f"Request: {request.method} {request.endpoint} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """
    Post-request processing for audit and performance monitoring
    Processamento pós-requisição para auditoria e monitoramento de performance
    """
    # Calculate request processing time / Calcular tempo de processamento da requisição
    if hasattr(g, 'request_start_time'):
        processing_time = (datetime.utcnow() - g.request_start_time).total_seconds() * 1000
        response.headers['X-Processing-Time-Ms'] = str(int(processing_time))
    
    # Add security headers / Adicionar cabeçalhos de segurança
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Add frontend URL to response headers for client configuration
    # Adicionar URL do frontend aos cabeçalhos de resposta para configuração do cliente
    response.headers['X-Frontend-Base-URL'] = ConfigService.FRONTEND_BASE_URL
    
    return response

@app.route('/health')
@audit_required(action='HEALTH_CHECK', resource_type='system', risk_level='LOW')
def health_check():
    """
    Health check endpoint with comprehensive system status
    Endpoint de verificação de saúde com status abrangente do sistema
    """
    try:
        # Check database connectivity / Verificar conectividade do banco de dados
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
        logger.error(f"Database health check failed / Verificação de saúde do banco de dados falhou: {str(e)}")
    
    health_data = {
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'service': 'Construction Hub Financial Advanced Service',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'frontend_base_url': ConfigService.FRONTEND_BASE_URL,
        'database_status': db_status,
        'features': [
            'Advanced Financial Analytics / Análise Financeira Avançada',
            'Risk Management System / Sistema de Gerenciamento de Riscos',
            'Financial Reporting Advanced / Relatórios Financeiros Avançados',
            'Integration Hub / Hub de Integração',
            'Real-time Monitoring / Monitoramento em Tempo Real',
            'Canadian Banking Integration / Integração Bancária Canadense',
            'Audit Trail System / Sistema de Trilha de Auditoria'
        ],
        'supported_languages': ConfigService.get_supported_languages(),
        'compliance': ConfigService.AUDIT_CONFIG['compliance_requirements'],
        'endpoints': {
            'analytics': '/api/analytics/*',
            'risk_management': '/api/risk/*',
            'reporting': '/api/reporting/*',
            'integration': '/api/integration/*'
        }
    }
    
    return jsonify(health_data)

@app.route('/config/frontend-urls')
@audit_required(action='GET_CONFIG', resource_type='configuration', risk_level='LOW')
def get_frontend_urls():
    """
    Get frontend URL configuration for client applications
    Obter configuração de URL do frontend para aplicações cliente
    """
    return jsonify({
        'success': True,
        'data': {
            'base_url': ConfigService.FRONTEND_BASE_URL,
            'endpoints': ConfigService.API_ENDPOINTS
        }
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve static files or API information
    Servir arquivos estáticos ou informações da API
    """
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({
            'message': 'Construction Hub Financial Advanced Service API',
            'service': 'financial-advanced',
            'version': '1.0.0',
            'frontend_url': ConfigService.FRONTEND_BASE_URL,
            'documentation': f"{ConfigService.FRONTEND_BASE_URL}/api/docs",
            'endpoints': {
                'health': '/health',
                'frontend_config': '/config/frontend-urls',
                'analytics': '/api/analytics/*',
                'risk_management': '/api/risk/*',
                'reporting': '/api/reporting/*',
                'integration': '/api/integration/*'
            },
            'supported_languages': ConfigService.get_supported_languages(),
            'compliance': 'SOX, PIPEDA, AODA, FINTRAC compliant'
        })

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Redirect to frontend application / Redirecionar para aplicação frontend
            return jsonify({
                'redirect_to': ConfigService.FRONTEND_BASE_URL,
                'message': 'Please access the application through the frontend URL',
                'frontend_url': ConfigService.FRONTEND_BASE_URL
            })

if __name__ == '__main__':
    logger.info(f"Starting Financial Advanced Service / Iniciando Serviço Financeiro Avançado")
    logger.info(f"Frontend URL configured: {ConfigService.FRONTEND_BASE_URL}")
    logger.info(f"Audit logging enabled: {ConfigService.is_audit_enabled()}")
    
    app.run(
        host='0.0.0.0', 
        port=5002, 
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )

