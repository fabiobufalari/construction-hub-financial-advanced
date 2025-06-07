"""
Audit Service - Enterprise Audit Trail System
Sistema de Auditoria Empresarial - Trilha de Auditoria

Provides comprehensive audit logging for all financial operations
Fornece registro de auditoria abrangente para todas as operações financeiras

Canadian Compliance: SOX, PIPEDA, AODA
Conformidade Canadense: SOX, PIPEDA, AODA
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import uuid
from functools import wraps
from flask import request, g

db = SQLAlchemy()

class AuditLog(db.Model):
    """
    Audit log entries for all system operations
    Entradas de log de auditoria para todas as operações do sistema
    """
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User and session information / Informações do usuário e sessão
    user_id = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100))
    session_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))  # IPv6 compatible / Compatível com IPv6
    user_agent = db.Column(db.Text)
    
    # Action details / Detalhes da ação
    action = db.Column(db.String(100), nullable=False)  # CREATE, READ, UPDATE, DELETE, LOGIN, LOGOUT
    resource_type = db.Column(db.String(50), nullable=False)  # project, payment, user, report
    resource_id = db.Column(db.String(50))
    service_name = db.Column(db.String(50), nullable=False)  # financial-advanced, accounts-payable, etc.
    
    # Request details / Detalhes da requisição
    http_method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    endpoint = db.Column(db.String(200))
    request_payload = db.Column(db.Text)  # JSON string / String JSON
    
    # Response details / Detalhes da resposta
    response_status = db.Column(db.Integer)
    response_payload = db.Column(db.Text)  # JSON string / String JSON
    
    # Data changes / Mudanças de dados
    old_values = db.Column(db.Text)  # JSON string of old values / String JSON dos valores antigos
    new_values = db.Column(db.Text)  # JSON string of new values / String JSON dos valores novos
    
    # Business context / Contexto de negócio
    business_context = db.Column(db.Text)  # Additional business information / Informações adicionais de negócio
    risk_level = db.Column(db.String(20), default='LOW')  # LOW, MEDIUM, HIGH, CRITICAL
    compliance_flags = db.Column(db.Text)  # JSON array of compliance requirements / Array JSON de requisitos de conformidade
    
    # Timing / Temporização
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processing_time_ms = db.Column(db.Integer)  # Request processing time / Tempo de processamento da requisição
    
    # Status and metadata / Status e metadados
    status = db.Column(db.String(20), default='SUCCESS')  # SUCCESS, FAILURE, WARNING
    error_message = db.Column(db.Text)
    metadata = db.Column(db.Text)  # Additional metadata as JSON / Metadados adicionais como JSON
    
    # Retention and archival / Retenção e arquivamento
    retention_period_days = db.Column(db.Integer, default=2555)  # 7 years default / 7 anos padrão
    archived = db.Column(db.Boolean, default=False)
    archived_at = db.Column(db.DateTime)

class AuditService:
    """
    Service for managing audit operations
    Serviço para gerenciar operações de auditoria
    """
    
    @staticmethod
    def log_action(action, resource_type, resource_id=None, old_values=None, new_values=None, 
                   business_context=None, risk_level='LOW', compliance_flags=None):
        """
        Log an audit action
        Registrar uma ação de auditoria
        
        Args:
            action (str): Action performed / Ação realizada
            resource_type (str): Type of resource / Tipo de recurso
            resource_id (str): ID of the resource / ID do recurso
            old_values (dict): Previous values / Valores anteriores
            new_values (dict): New values / Novos valores
            business_context (str): Business context / Contexto de negócio
            risk_level (str): Risk level / Nível de risco
            compliance_flags (list): Compliance requirements / Requisitos de conformidade
        """
        try:
            # Get request context / Obter contexto da requisição
            user_id = getattr(g, 'user_id', 'system')
            user_email = getattr(g, 'user_email', None)
            session_id = getattr(g, 'session_id', None)
            
            # Create audit log entry / Criar entrada de log de auditoria
            audit_log = AuditLog(
                user_id=user_id,
                user_email=user_email,
                session_id=session_id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                service_name='financial-advanced',
                http_method=request.method if request else None,
                endpoint=request.endpoint if request else None,
                request_payload=json.dumps(request.get_json()) if request and request.get_json() else None,
                old_values=json.dumps(old_values) if old_values else None,
                new_values=json.dumps(new_values) if new_values else None,
                business_context=business_context,
                risk_level=risk_level,
                compliance_flags=json.dumps(compliance_flags) if compliance_flags else None,
                status='SUCCESS'
            )
            
            db.session.add(audit_log)
            db.session.commit()
            
            return audit_log.id
            
        except Exception as e:
            # Log the error but don't fail the main operation
            # Registrar o erro mas não falhar a operação principal
            print(f"Audit logging failed: {str(e)}")
            return None
    
    @staticmethod
    def log_error(action, resource_type, error_message, resource_id=None):
        """
        Log an error action
        Registrar uma ação de erro
        """
        return AuditService.log_action(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            business_context=f"Error occurred: {error_message}",
            risk_level='HIGH'
        )
    
    @staticmethod
    def get_audit_trail(resource_type=None, resource_id=None, user_id=None, 
                       start_date=None, end_date=None, limit=100):
        """
        Get audit trail with filters
        Obter trilha de auditoria com filtros
        """
        query = AuditLog.query
        
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if resource_id:
            query = query.filter(AuditLog.resource_id == resource_id)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()

def audit_required(action=None, resource_type=None, risk_level='LOW'):
    """
    Decorator for automatic audit logging
    Decorador para registro automático de auditoria
    
    Usage / Uso:
    @audit_required(action='CREATE', resource_type='payment')
    def create_payment():
        pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = datetime.utcnow()
            
            try:
                # Execute the function / Executar a função
                result = f(*args, **kwargs)
                
                # Calculate processing time / Calcular tempo de processamento
                processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Log successful action / Registrar ação bem-sucedida
                AuditService.log_action(
                    action=action or f.__name__.upper(),
                    resource_type=resource_type or 'unknown',
                    business_context=f"Function {f.__name__} executed successfully",
                    risk_level=risk_level
                )
                
                return result
                
            except Exception as e:
                # Log failed action / Registrar ação falhada
                AuditService.log_error(
                    action=action or f.__name__.upper(),
                    resource_type=resource_type or 'unknown',
                    error_message=str(e)
                )
                raise
        
        return decorated_function
    return decorator

