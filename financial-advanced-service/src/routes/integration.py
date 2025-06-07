"""
Integration Routes - Microservices Integration Hub
Central integration point for all Construction Hub microservices
"""

from flask import Blueprint, request, jsonify
from src.services.integration_service import IntegrationService
from src.services.data_sync_service import DataSyncService
from src.services.api_gateway_service import APIGatewayService

integration_bp = Blueprint('integration', __name__)
integration_service = IntegrationService()
data_sync_service = DataSyncService()
api_gateway_service = APIGatewayService()

@integration_bp.route('/health')
def health():
    """Integration module health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'Integration Hub',
        'capabilities': [
            'Microservices Communication',
            'Data Synchronization',
            'API Gateway Functions',
            'Real-time Data Streaming',
            'Cross-service Analytics'
        ]
    })

@integration_bp.route('/microservices/status', methods=['GET'])
def get_microservices_status():
    """Get status of all connected microservices"""
    try:
        status = integration_service.get_all_microservices_status()
        
        return jsonify({
            'success': True,
            'data': status,
            'total_services': len(status),
            'healthy_services': len([s for s in status if s.get('status') == 'healthy'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/sync/financial-data', methods=['POST'])
def sync_financial_data():
    """Synchronize financial data across all microservices"""
    try:
        data = request.get_json()
        sync_type = data.get('type', 'incremental')  # full, incremental
        services = data.get('services', 'all')  # specific services or 'all'
        
        sync_result = data_sync_service.sync_financial_data(sync_type, services)
        
        return jsonify({
            'success': True,
            'data': sync_result,
            'sync_type': sync_type,
            'services_synced': sync_result.get('services_count', 0)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/aggregate/financial-summary', methods=['GET'])
def get_aggregated_financial_summary():
    """Get aggregated financial summary from all microservices"""
    try:
        period = request.args.get('period', 'current_month')
        include_forecasts = request.args.get('forecasts', 'true').lower() == 'true'
        
        summary = integration_service.aggregate_financial_summary(period, include_forecasts)
        
        return jsonify({
            'success': True,
            'data': summary,
            'period': period,
            'includes_forecasts': include_forecasts
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/cross-service/analytics', methods=['POST'])
def perform_cross_service_analytics():
    """Perform analytics across multiple microservices"""
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'correlation')  # correlation, trend, variance
        services = data.get('services', [])
        metrics = data.get('metrics', [])
        
        if not services or not metrics:
            return jsonify({
                'success': False, 
                'error': 'Services and metrics required'
            }), 400
        
        analytics = integration_service.perform_cross_service_analytics(
            analysis_type, services, metrics
        )
        
        return jsonify({
            'success': True,
            'data': analytics,
            'analysis_type': analysis_type,
            'services_analyzed': len(services)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/data-flow/monitor', methods=['GET'])
def monitor_data_flow():
    """Monitor real-time data flow between microservices"""
    try:
        time_window = request.args.get('window', '1hour')  # 15min, 1hour, 24hour
        service_filter = request.args.get('service')
        
        flow_data = integration_service.monitor_data_flow(time_window, service_filter)
        
        return jsonify({
            'success': True,
            'data': flow_data,
            'time_window': time_window,
            'service_filter': service_filter
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/api-gateway/route', methods=['POST'])
def route_api_request():
    """Route API request through the gateway"""
    try:
        data = request.get_json()
        target_service = data.get('service')
        endpoint = data.get('endpoint')
        method = data.get('method', 'GET')
        payload = data.get('payload', {})
        
        if not target_service or not endpoint:
            return jsonify({
                'success': False, 
                'error': 'Target service and endpoint required'
            }), 400
        
        response = api_gateway_service.route_request(
            target_service, endpoint, method, payload
        )
        
        return jsonify({
            'success': True,
            'data': response,
            'target_service': target_service,
            'endpoint': endpoint
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/webhooks/register', methods=['POST'])
def register_webhook():
    """Register webhook for real-time notifications"""
    try:
        data = request.get_json()
        webhook_config = data.get('config', {})
        
        required_fields = ['url', 'events', 'service']
        if not all(field in webhook_config for field in required_fields):
            return jsonify({
                'success': False, 
                'error': 'Missing required fields: url, events, service'
            }), 400
        
        webhook = integration_service.register_webhook(webhook_config)
        
        return jsonify({
            'success': True,
            'data': webhook,
            'webhook_id': webhook.get('webhook_id')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@integration_bp.route('/data-consistency/check', methods=['GET'])
def check_data_consistency():
    """Check data consistency across microservices"""
    try:
        scope = request.args.get('scope', 'financial')  # financial, projects, users
        fix_inconsistencies = request.args.get('fix', 'false').lower() == 'true'
        
        consistency_report = integration_service.check_data_consistency(
            scope, fix_inconsistencies
        )
        
        return jsonify({
            'success': True,
            'data': consistency_report,
            'scope': scope,
            'auto_fixed': fix_inconsistencies
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

