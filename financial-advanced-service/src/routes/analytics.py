"""
Analytics Routes - Advanced Financial Analytics
Provides comprehensive financial analytics and insights for construction companies
"""

from flask import Blueprint, request, jsonify
from src.services.analytics_service import AnalyticsService
from src.services.profitability_service import ProfitabilityService
from src.services.kpi_service import KPIService

analytics_bp = Blueprint('analytics', __name__)
analytics_service = AnalyticsService()
profitability_service = ProfitabilityService()
kpi_service = KPIService()

@analytics_bp.route('/health')
def health():
    """Analytics module health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'Financial Analytics',
        'capabilities': [
            'Financial KPI Calculation',
            'Project Profitability Analysis',
            'Revenue Trend Analysis',
            'Cost Analysis',
            'Performance Benchmarking'
        ]
    })

@analytics_bp.route('/kpis', methods=['GET'])
def get_financial_kpis():
    """Get comprehensive financial KPIs"""
    try:
        period = request.args.get('period', 'monthly')
        project_id = request.args.get('project_id')
        
        kpis = kpi_service.calculate_financial_kpis(period, project_id)
        
        return jsonify({
            'success': True,
            'data': kpis,
            'period': period,
            'project_id': project_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/profitability', methods=['GET'])
def get_profitability_analysis():
    """Get detailed profitability analysis"""
    try:
        project_id = request.args.get('project_id')
        include_forecast = request.args.get('include_forecast', 'false').lower() == 'true'
        
        analysis = profitability_service.analyze_project_profitability(
            project_id, include_forecast
        )
        
        return jsonify({
            'success': True,
            'data': analysis,
            'project_id': project_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/revenue-trends', methods=['GET'])
def get_revenue_trends():
    """Get revenue trend analysis"""
    try:
        period = request.args.get('period', '12months')
        granularity = request.args.get('granularity', 'monthly')
        
        trends = analytics_service.analyze_revenue_trends(period, granularity)
        
        return jsonify({
            'success': True,
            'data': trends,
            'period': period,
            'granularity': granularity
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/cost-analysis', methods=['GET'])
def get_cost_analysis():
    """Get comprehensive cost analysis"""
    try:
        analysis_type = request.args.get('type', 'category')  # category, project, time
        period = request.args.get('period', '6months')
        
        analysis = analytics_service.analyze_costs(analysis_type, period)
        
        return jsonify({
            'success': True,
            'data': analysis,
            'analysis_type': analysis_type,
            'period': period
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/performance-metrics', methods=['GET'])
def get_performance_metrics():
    """Get performance metrics and benchmarks"""
    try:
        metric_type = request.args.get('type', 'all')  # efficiency, quality, financial
        benchmark = request.args.get('benchmark', 'industry')
        
        metrics = analytics_service.calculate_performance_metrics(metric_type, benchmark)
        
        return jsonify({
            'success': True,
            'data': metrics,
            'metric_type': metric_type,
            'benchmark': benchmark
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/cash-flow-analysis', methods=['GET'])
def get_cash_flow_analysis():
    """Get cash flow analysis and patterns"""
    try:
        period = request.args.get('period', '12months')
        include_forecast = request.args.get('include_forecast', 'true').lower() == 'true'
        
        analysis = analytics_service.analyze_cash_flow(period, include_forecast)
        
        return jsonify({
            'success': True,
            'data': analysis,
            'period': period,
            'includes_forecast': include_forecast
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/project-comparison', methods=['POST'])
def compare_projects():
    """Compare multiple projects across various metrics"""
    try:
        data = request.get_json()
        project_ids = data.get('project_ids', [])
        metrics = data.get('metrics', ['profitability', 'efficiency', 'timeline'])
        
        if not project_ids:
            return jsonify({'success': False, 'error': 'Project IDs required'}), 400
        
        comparison = analytics_service.compare_projects(project_ids, metrics)
        
        return jsonify({
            'success': True,
            'data': comparison,
            'projects_compared': len(project_ids),
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analytics_bp.route('/financial-ratios', methods=['GET'])
def get_financial_ratios():
    """Get comprehensive financial ratios"""
    try:
        ratio_category = request.args.get('category', 'all')  # liquidity, profitability, efficiency
        period = request.args.get('period', 'current')
        
        ratios = analytics_service.calculate_financial_ratios(ratio_category, period)
        
        return jsonify({
            'success': True,
            'data': ratios,
            'category': ratio_category,
            'period': period
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

