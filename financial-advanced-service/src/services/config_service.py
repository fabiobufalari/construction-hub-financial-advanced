"""
Configuration Service - Application Configuration Management
Serviço de Configuração - Gerenciamento de Configuração da Aplicação

Manages all application configurations including external URLs and environment settings
Gerencia todas as configurações da aplicação incluindo URLs externas e configurações de ambiente

Canadian Standards: Follows Canadian government IT standards
Padrões Canadenses: Segue padrões de TI do governo canadense
"""

import os
from typing import Dict, Any

class ConfigService:
    """
    Centralized configuration management
    Gerenciamento centralizado de configuração
    """
    
    # Frontend Configuration / Configuração do Frontend
    FRONTEND_BASE_URL = "http://buildingteste.ddns.net:8081"
    
    # API Endpoints / Endpoints da API
    API_ENDPOINTS = {
        # Authentication / Autenticação
        'auth_login': f"{FRONTEND_BASE_URL}/auth/login",
        'auth_logout': f"{FRONTEND_BASE_URL}/auth/logout",
        'auth_register': f"{FRONTEND_BASE_URL}/auth/register",
        'auth_reset_password': f"{FRONTEND_BASE_URL}/auth/reset-password",
        
        # Dashboard / Painel de Controle
        'dashboard_executive': f"{FRONTEND_BASE_URL}/dashboard/executive",
        'dashboard_financial': f"{FRONTEND_BASE_URL}/dashboard/financial",
        'dashboard_projects': f"{FRONTEND_BASE_URL}/dashboard/projects",
        
        # Financial Management / Gerenciamento Financeiro
        'accounts_payable': f"{FRONTEND_BASE_URL}/financial/accounts-payable",
        'accounts_receivable': f"{FRONTEND_BASE_URL}/financial/accounts-receivable",
        'cash_flow': f"{FRONTEND_BASE_URL}/financial/cash-flow",
        'financial_reports': f"{FRONTEND_BASE_URL}/financial/reports",
        
        # Project Management / Gerenciamento de Projetos
        'projects_list': f"{FRONTEND_BASE_URL}/projects",
        'project_details': f"{FRONTEND_BASE_URL}/projects/{{project_id}}",
        'project_financials': f"{FRONTEND_BASE_URL}/projects/{{project_id}}/financials",
        
        # Risk Management / Gerenciamento de Riscos
        'risk_dashboard': f"{FRONTEND_BASE_URL}/risk/dashboard",
        'risk_assessments': f"{FRONTEND_BASE_URL}/risk/assessments",
        'risk_alerts': f"{FRONTEND_BASE_URL}/risk/alerts",
        
        # Analytics / Análises
        'analytics_overview': f"{FRONTEND_BASE_URL}/analytics/overview",
        'analytics_trends': f"{FRONTEND_BASE_URL}/analytics/trends",
        'analytics_forecasts': f"{FRONTEND_BASE_URL}/analytics/forecasts",
        
        # Administration / Administração
        'admin_users': f"{FRONTEND_BASE_URL}/admin/users",
        'admin_settings': f"{FRONTEND_BASE_URL}/admin/settings",
        'admin_audit': f"{FRONTEND_BASE_URL}/admin/audit",
    }
    
    # Microservices Configuration / Configuração dos Microserviços
    MICROSERVICES = {
        'accounts-payable': {
            'url': 'http://localhost:5000',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'accounts-receivable': {
            'url': 'http://localhost:5001',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'data-analytics': {
            'url': 'http://localhost:5001',
            'health_endpoint': '/health',
            'timeout': 60
        },
        'financial-advanced': {
            'url': 'http://localhost:5002',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'project-management': {
            'url': 'http://localhost:5003',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'cash-flow': {
            'url': 'http://localhost:5004',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'financial-reports': {
            'url': 'http://localhost:5005',
            'health_endpoint': '/health',
            'timeout': 45
        },
        'communication': {
            'url': 'http://localhost:5006',
            'health_endpoint': '/health',
            'timeout': 15
        },
        'authentication': {
            'url': 'http://localhost:5007',
            'health_endpoint': '/health',
            'timeout': 15
        },
        'company': {
            'url': 'http://localhost:5008',
            'health_endpoint': '/health',
            'timeout': 20
        },
        'create-people': {
            'url': 'http://localhost:5009',
            'health_endpoint': '/health',
            'timeout': 20
        },
        'employee-costs': {
            'url': 'http://localhost:5010',
            'health_endpoint': '/health',
            'timeout': 25
        },
        'supplier': {
            'url': 'http://localhost:5011',
            'health_endpoint': '/health',
            'timeout': 20
        },
        'bank-integration': {
            'url': 'http://localhost:5012',
            'health_endpoint': '/health',
            'timeout': 45
        },
        'calculation-materials': {
            'url': 'http://localhost:5013',
            'health_endpoint': '/health',
            'timeout': 30
        },
        'integrations': {
            'url': 'http://localhost:5014',
            'health_endpoint': '/health',
            'timeout': 30
        }
    }
    
    # Database Configuration / Configuração do Banco de Dados
    DATABASE_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'username': os.getenv('DB_USERNAME', 'root'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'database': os.getenv('DB_NAME', 'construction_hub_financial'),
        'charset': 'utf8mb4',
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600
    }
    
    # Security Configuration / Configuração de Segurança
    SECURITY_CONFIG = {
        'jwt_secret_key': os.getenv('JWT_SECRET_KEY', 'financial_advanced_jwt_secret_2024'),
        'jwt_expiration_hours': 24,
        'password_min_length': 8,
        'password_require_special': True,
        'max_login_attempts': 5,
        'lockout_duration_minutes': 30,
        'session_timeout_minutes': 120
    }
    
    # Audit Configuration / Configuração de Auditoria
    AUDIT_CONFIG = {
        'enabled': True,
        'log_all_requests': True,
        'log_request_body': True,
        'log_response_body': False,  # For performance / Para performance
        'retention_days': 2555,  # 7 years / 7 anos
        'high_risk_actions': [
            'DELETE', 'TRANSFER_FUNDS', 'APPROVE_PAYMENT', 
            'MODIFY_BUDGET', 'CHANGE_PERMISSIONS'
        ],
        'compliance_requirements': [
            'SOX',  # Sarbanes-Oxley Act
            'PIPEDA',  # Personal Information Protection and Electronic Documents Act
            'AODA',  # Accessibility for Ontarians with Disabilities Act
            'FINTRAC'  # Financial Transactions and Reports Analysis Centre of Canada
        ]
    }
    
    # Logging Configuration / Configuração de Logging
    LOGGING_CONFIG = {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file_path': os.getenv('LOG_FILE_PATH', '/var/log/construction-hub/financial-advanced.log'),
        'max_file_size_mb': 100,
        'backup_count': 10,
        'enable_console': True
    }
    
    # Canadian Banking Configuration / Configuração Bancária Canadense
    CANADIAN_BANKING = {
        'supported_banks': [
            'RBC',  # Royal Bank of Canada
            'TD',   # Toronto-Dominion Bank
            'BMO',  # Bank of Montreal
            'Scotiabank',  # Bank of Nova Scotia
            'CIBC'  # Canadian Imperial Bank of Commerce
        ],
        'payment_methods': [
            'INTERAC',
            'WIRE_TRANSFER',
            'ACH',
            'CHEQUE',
            'CREDIT_CARD'
        ],
        'currencies': ['CAD', 'USD'],
        'default_currency': 'CAD',
        'business_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'banking_holidays': [
            '2024-01-01',  # New Year's Day
            '2024-02-19',  # Family Day (Ontario)
            '2024-03-29',  # Good Friday
            '2024-05-20',  # Victoria Day
            '2024-07-01',  # Canada Day
            '2024-08-05',  # Civic Holiday (Ontario)
            '2024-09-02',  # Labour Day
            '2024-10-14',  # Thanksgiving Day
            '2024-11-11',  # Remembrance Day
            '2024-12-25',  # Christmas Day
            '2024-12-26'   # Boxing Day
        ]
    }
    
    # Performance Configuration / Configuração de Performance
    PERFORMANCE_CONFIG = {
        'cache_enabled': True,
        'cache_ttl_seconds': 300,  # 5 minutes / 5 minutos
        'rate_limit_per_minute': 1000,
        'max_concurrent_requests': 100,
        'request_timeout_seconds': 30,
        'bulk_operation_batch_size': 1000
    }
    
    @classmethod
    def get_frontend_url(cls, endpoint_key: str, **kwargs) -> str:
        """
        Get frontend URL for specific endpoint
        Obter URL do frontend para endpoint específico
        
        Args:
            endpoint_key (str): Key for the endpoint / Chave para o endpoint
            **kwargs: Parameters to format the URL / Parâmetros para formatar a URL
        
        Returns:
            str: Formatted URL / URL formatada
        """
        url = cls.API_ENDPOINTS.get(endpoint_key)
        if url and kwargs:
            url = url.format(**kwargs)
        return url
    
    @classmethod
    def get_microservice_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for specific microservice
        Obter configuração para microserviço específico
        """
        return cls.MICROSERVICES.get(service_name, {})
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Get database connection URL
        Obter URL de conexão do banco de dados
        """
        config = cls.DATABASE_CONFIG
        return (f"mysql+pymysql://{config['username']}:{config['password']}"
                f"@{config['host']}:{config['port']}/{config['database']}"
                f"?charset={config['charset']}")
    
    @classmethod
    def is_audit_enabled(cls) -> bool:
        """
        Check if audit logging is enabled
        Verificar se o log de auditoria está habilitado
        """
        return cls.AUDIT_CONFIG.get('enabled', True)
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """
        Get list of supported languages
        Obter lista de idiomas suportados
        """
        return ['en-CA', 'pt-BR', 'en-US', 'fr-CA']  # Canadian English, Portuguese, US English, Canadian French

