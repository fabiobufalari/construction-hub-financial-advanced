"""
Reporting Routes - Advanced Financial Reporting
Enterprise-grade financial reporting and document generation
"""

from flask import Blueprint, request, jsonify, send_file
from src.services.reporting_service import ReportingService
from src.services.dashboard_service import DashboardService
from src.services.export_service import ExportService

reporting_bp = Blueprint('reporting', __name__)
reporting_service = ReportingService()
dashboard_service = DashboardService()
export_service = ExportService()

@reporting_bp.route('/health')
def health():
    """Reporting module health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'Financial Reporting',
        'capabilities': [
            'Executive Dashboards',
            'Financial Statement Generation',
            'Custom Report Builder',
            'Real-time Analytics',
            'Multi-format Export (PDF, Excel, CSV)'
        ]
    })

@reporting_bp.route('/dashboard', methods=['GET'])
def get_executive_dashboard():
    """Get executive dashboard data"""
    try:
        dashboard_type = request.args.get('type', 'executive')  # executive, operational, project
        period = request.args.get('period', 'current_month')
        
        dashboard_data = dashboard_service.generate_dashboard(dashboard_type, period)
        
        return jsonify({
            'success': True,
            'data': dashboard_data,
            'dashboard_type': dashboard_type,
            'period': period
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/financial-statements', methods=['GET'])
def get_financial_statements():
    """Generate financial statements"""
    try:
        statement_type = request.args.get('type', 'all')  # P&L, balance_sheet, cash_flow, all
        period = request.args.get('period', 'current_quarter')
        format_type = request.args.get('format', 'json')  # json, pdf, excel
        
        statements = reporting_service.generate_financial_statements(
            statement_type, period, format_type
        )
        
        if format_type in ['pdf', 'excel']:
            return send_file(statements['file_path'], as_attachment=True)
        
        return jsonify({
            'success': True,
            'data': statements,
            'statement_type': statement_type,
            'period': period
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/custom-report', methods=['POST'])
def generate_custom_report():
    """Generate custom report based on parameters"""
    try:
        data = request.get_json()
        report_config = data.get('config', {})
        
        required_fields = ['report_name', 'data_sources', 'metrics']
        if not all(field in report_config for field in required_fields):
            return jsonify({
                'success': False, 
                'error': 'Missing required fields: report_name, data_sources, metrics'
            }), 400
        
        report = reporting_service.generate_custom_report(report_config)
        
        return jsonify({
            'success': True,
            'data': report,
            'report_id': report.get('report_id')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/project-reports', methods=['GET'])
def get_project_reports():
    """Get project-specific financial reports"""
    try:
        project_id = request.args.get('project_id')
        report_type = request.args.get('type', 'summary')  # summary, detailed, variance
        
        if not project_id:
            return jsonify({'success': False, 'error': 'Project ID required'}), 400
        
        reports = reporting_service.generate_project_reports(project_id, report_type)
        
        return jsonify({
            'success': True,
            'data': reports,
            'project_id': project_id,
            'report_type': report_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/budget-variance', methods=['GET'])
def get_budget_variance_report():
    """Get budget variance analysis report"""
    try:
        scope = request.args.get('scope', 'company')  # company, project, department
        period = request.args.get('period', 'current_month')
        detail_level = request.args.get('detail', 'summary')  # summary, detailed
        
        variance_report = reporting_service.generate_budget_variance_report(
            scope, period, detail_level
        )
        
        return jsonify({
            'success': True,
            'data': variance_report,
            'scope': scope,
            'period': period
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/cash-flow-statement', methods=['GET'])
def get_cash_flow_statement():
    """Generate cash flow statement"""
    try:
        period = request.args.get('period', 'current_quarter')
        method = request.args.get('method', 'indirect')  # direct, indirect
        include_forecast = request.args.get('forecast', 'false').lower() == 'true'
        
        statement = reporting_service.generate_cash_flow_statement(
            period, method, include_forecast
        )
        
        return jsonify({
            'success': True,
            'data': statement,
            'period': period,
            'method': method,
            'includes_forecast': include_forecast
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/export', methods=['POST'])
def export_report():
    """Export report in specified format"""
    try:
        data = request.get_json()
        report_id = data.get('report_id')
        export_format = data.get('format', 'pdf')  # pdf, excel, csv
        
        if not report_id:
            return jsonify({'success': False, 'error': 'Report ID required'}), 400
        
        file_path = export_service.export_report(report_id, export_format)
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reporting_bp.route('/scheduled-reports', methods=['GET', 'POST'])
def manage_scheduled_reports():
    """Manage scheduled report generation"""
    try:
        if request.method == 'GET':
            # Get list of scheduled reports
            scheduled = reporting_service.get_scheduled_reports()
            return jsonify({
                'success': True,
                'data': scheduled
            })
        
        elif request.method == 'POST':
            # Create new scheduled report
            data = request.get_json()
            schedule_config = data.get('config', {})
            
            scheduled_report = reporting_service.create_scheduled_report(schedule_config)
            
            return jsonify({
                'success': True,
                'data': scheduled_report,
                'schedule_id': scheduled_report.get('schedule_id')
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

