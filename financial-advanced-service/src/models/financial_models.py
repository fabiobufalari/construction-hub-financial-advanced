"""
Financial Models for Construction Hub Financial Advanced Service
Enterprise-grade data models for financial analytics and risk management
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class FinancialMetric(db.Model):
    """Financial metrics and KPIs tracking"""
    __tablename__ = 'financial_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # revenue, cost, profit, ratio
    value = db.Column(db.Decimal(15, 2), nullable=False)
    currency = db.Column(db.String(3), default='CAD')
    project_id = db.Column(db.String(50))
    company_id = db.Column(db.String(50))
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    calculation_method = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RiskAssessment(db.Model):
    """Risk assessment and scoring for projects and entities"""
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # project, supplier, customer, investment
    entity_id = db.Column(db.String(50), nullable=False)
    risk_category = db.Column(db.String(50), nullable=False)  # financial, operational, market, credit
    risk_score = db.Column(db.Decimal(5, 2), nullable=False)  # 0-100 scale
    risk_level = db.Column(db.String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    risk_factors = db.Column(db.Text)  # JSON array of risk factors
    mitigation_strategies = db.Column(db.Text)  # JSON array of strategies
    probability = db.Column(db.Decimal(5, 2))  # 0-100%
    impact = db.Column(db.Decimal(15, 2))  # Financial impact in CAD
    assessment_date = db.Column(db.Date, nullable=False)
    assessor_id = db.Column(db.String(50))
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CashFlowForecast(db.Model):
    """Cash flow forecasting and predictions"""
    __tablename__ = 'cash_flow_forecasts'
    
    id = db.Column(db.Integer, primary_key=True)
    forecast_type = db.Column(db.String(50), nullable=False)  # weekly, monthly, quarterly, annual
    forecast_date = db.Column(db.Date, nullable=False)
    projected_inflow = db.Column(db.Decimal(15, 2), nullable=False)
    projected_outflow = db.Column(db.Decimal(15, 2), nullable=False)
    net_cash_flow = db.Column(db.Decimal(15, 2), nullable=False)
    cumulative_balance = db.Column(db.Decimal(15, 2))
    confidence_level = db.Column(db.Decimal(5, 2))  # 0-100%
    model_used = db.Column(db.String(50))  # ARIMA, LSTM, LINEAR_REGRESSION
    assumptions = db.Column(db.Text)  # JSON object with assumptions
    scenario = db.Column(db.String(50), default='BASE')  # BASE, OPTIMISTIC, PESSIMISTIC
    project_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectProfitability(db.Model):
    """Project profitability analysis and tracking"""
    __tablename__ = 'project_profitability'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(50), nullable=False)
    project_name = db.Column(db.String(200))
    total_revenue = db.Column(db.Decimal(15, 2), nullable=False)
    total_costs = db.Column(db.Decimal(15, 2), nullable=False)
    gross_profit = db.Column(db.Decimal(15, 2), nullable=False)
    gross_margin_percent = db.Column(db.Decimal(5, 2))
    net_profit = db.Column(db.Decimal(15, 2))
    net_margin_percent = db.Column(db.Decimal(5, 2))
    roi_percent = db.Column(db.Decimal(5, 2))
    budget_variance = db.Column(db.Decimal(15, 2))
    budget_variance_percent = db.Column(db.Decimal(5, 2))
    completion_percent = db.Column(db.Decimal(5, 2))
    estimated_completion_date = db.Column(db.Date)
    cost_per_day = db.Column(db.Decimal(10, 2))
    revenue_per_day = db.Column(db.Decimal(10, 2))
    analysis_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FinancialAlert(db.Model):
    """Financial alerts and notifications"""
    __tablename__ = 'financial_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)  # CASH_FLOW, BUDGET, RISK, PAYMENT
    severity = db.Column(db.String(20), nullable=False)  # INFO, WARNING, CRITICAL
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    entity_type = db.Column(db.String(50))  # project, supplier, customer
    entity_id = db.Column(db.String(50))
    threshold_value = db.Column(db.Decimal(15, 2))
    current_value = db.Column(db.Decimal(15, 2))
    recommended_action = db.Column(db.Text)
    is_resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FinancialReport(db.Model):
    """Generated financial reports metadata"""
    __tablename__ = 'financial_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)  # P&L, BALANCE_SHEET, CASH_FLOW, CUSTOM
    report_name = db.Column(db.String(200), nullable=False)
    report_period = db.Column(db.String(50))  # MONTHLY, QUARTERLY, ANNUAL
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    file_path = db.Column(db.String(500))
    file_format = db.Column(db.String(10))  # PDF, XLSX, CSV
    parameters = db.Column(db.Text)  # JSON object with report parameters
    generated_by = db.Column(db.String(50))
    status = db.Column(db.String(20), default='GENERATED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BankingIntegration(db.Model):
    """Banking integration and transaction tracking"""
    __tablename__ = 'banking_integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(50))  # CHECKING, SAVINGS, CREDIT_LINE
    current_balance = db.Column(db.Decimal(15, 2))
    available_balance = db.Column(db.Decimal(15, 2))
    last_sync_date = db.Column(db.DateTime)
    sync_status = db.Column(db.String(20), default='ACTIVE')
    api_endpoint = db.Column(db.String(200))
    integration_type = db.Column(db.String(50))  # API, FILE_IMPORT, MANUAL
    configuration = db.Column(db.Text)  # JSON configuration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

