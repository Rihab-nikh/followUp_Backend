"""
Global error handler middleware
"""

from flask import jsonify, current_app
import traceback

def init_error_handler(app):
    """Initialize global error handler."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'status': 404
        }), 404
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'status': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            'success': False,
            'error': 'Unauthorized access',
            'status': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            'success': False,
            'error': 'Access forbidden',
            'status': 403
        }), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        # Log the error
        current_app.logger.error(f"Internal server error: {error}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'status': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log unexpected errors
        current_app.logger.error(f"Unhandled exception: {error}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'status': 500
        }), 500
