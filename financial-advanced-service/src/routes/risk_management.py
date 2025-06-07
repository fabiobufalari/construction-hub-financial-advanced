"""
Risk Management Routes - Advanced Risk Assessment and Management
Comprehensive risk management system for construction financial operations
"""

from flask import Blueprint, request, jsonify
from src.services.risk_service import RiskService
from src.services.credit_service import CreditService
from src.services.portfolio_risk_service import PortfolioRiskService

risk_bp = Blueprint('risk', __name__)
risk_service = RiskService()
credit_service = CreditService()
portfolio_risk_service = PortfolioRiskService()

@risk_bp.route('/health')
def health():
    """Risk management module health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'Risk Management',
        'capabilities': [
            'Project Risk Assessment',
            'Credit Risk Scoring',
            'Portfolio Risk Analysis',
            'Risk Mitigation Strategies',
            'Predictive Risk Modeling'
        ]
    })

@risk_bp.route('/assess-project', methods=['POST'])
def assess_project_risk():
    """Comprehensive project risk assessment"""
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        assessment_type = data.get('type', 'comprehensive')  # financial, operational, market
        
        if not project_id:
            return jsonify({'success': False, 'error': 'Project ID required'}), 400
        
        assessment = risk_service.assess_project_risk(project_id, assessment_type)
        
        return jsonify({
            'success': True,
            'data': assessment,
            'project_id': project_id,
            'assessment_type': assessment_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/credit-score', methods=['POST'])
def calculate_credit_score():
    """Calculate credit score for suppliers/customers"""
    try:
        data = request.get_json()
        entity_id = data.get('entity_id')
        entity_type = data.get('entity_type')  # supplier, customer
        
        if not entity_id or not entity_type:
            return jsonify({'success': False, 'error': 'Entity ID and type required'}), 400
        
        score = credit_service.calculate_credit_score(entity_id, entity_type)
        
        return jsonify({
            'success': True,
            'data': score,
            'entity_id': entity_id,
            'entity_type': entity_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/portfolio-analysis', methods=['GET'])
def get_portfolio_risk_analysis():
    """Get comprehensive portfolio risk analysis"""
    try:
        analysis_type = request.args.get('type', 'overall')  # overall, by_category, by_project
        include_scenarios = request.args.get('scenarios', 'true').lower() == 'true'
        
        analysis = portfolio_risk_service.analyze_portfolio_risk(
            analysis_type, include_scenarios
        )
        
        return jsonify({
            'success': True,
            'data': analysis,
            'analysis_type': analysis_type,
            'includes_scenarios': include_scenarios
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/risk-alerts', methods=['GET'])
def get_risk_alerts():
    """Get current risk alerts and warnings"""
    try:
        severity = request.args.get('severity', 'all')  # INFO, WARNING, CRITICAL
        category = request.args.get('category', 'all')  # financial, operational, market
        
        alerts = risk_service.get_risk_alerts(severity, category)
        
        return jsonify({
            'success': True,
            'data': alerts,
            'severity_filter': severity,
            'category_filter': category
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/mitigation-strategies', methods=['GET'])
def get_mitigation_strategies():
    """Get risk mitigation strategies"""
    try:
        risk_type = request.args.get('risk_type')
        risk_level = request.args.get('risk_level')
        
        strategies = risk_service.get_mitigation_strategies(risk_type, risk_level)
        
        return jsonify({
            'success': True,
            'data': strategies,
            'risk_type': risk_type,
            'risk_level': risk_level
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/stress-test', methods=['POST'])
def perform_stress_test():
    """Perform financial stress testing"""
    try:
        data = request.get_json()
        scenarios = data.get('scenarios', ['recession', 'interest_rate_rise', 'material_cost_spike'])
        severity = data.get('severity', 'moderate')  # mild, moderate, severe
        
        results = risk_service.perform_stress_test(scenarios, severity)
        
        return jsonify({
            'success': True,
            'data': results,
            'scenarios': scenarios,
            'severity': severity
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/risk-matrix', methods=['GET'])
def get_risk_matrix():
    """Get risk matrix visualization data"""
    try:
        scope = request.args.get('scope', 'all')  # all, active_projects, portfolio
        
        matrix = risk_service.generate_risk_matrix(scope)
        
        return jsonify({
            'success': True,
            'data': matrix,
            'scope': scope
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@risk_bp.route('/predictive-analysis', methods=['POST'])
def get_predictive_risk_analysis():
    """Get predictive risk analysis using ML models"""
    try:
        data = request.get_json()
        prediction_horizon = data.get('horizon', '6months')  # 3months, 6months, 1year
        risk_categories = data.get('categories', ['financial', 'operational'])
        
        predictions = risk_service.predict_future_risks(prediction_horizon, risk_categories)
        
        return jsonify({
            'success': True,
            'data': predictions,
            'prediction_horizon': prediction_horizon,
            'categories': risk_categories
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

