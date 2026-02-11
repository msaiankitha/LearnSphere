from flask import Flask, render_template
from config import config
from routes.content_routes import content_bp  # ✅ This must be here
import os

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload directories exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'audio'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'code'), exist_ok=True)
    
    # ✅ THIS LINE IS CRITICAL - Register the blueprint
    app.register_blueprint(content_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', app_name=app.config['APP_NAME']), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html', app_name=app.config['APP_NAME']), 500
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)