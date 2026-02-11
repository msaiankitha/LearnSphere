import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ============ GROQ CONFIG - FIXED ============
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    # ❌ REMOVED GROQ_BASE_URL - causes double path error
    # ✅ SDK handles URL automatically
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
    STABILITY_ENGINE = os.getenv('STABILITY_ENGINE', 'stable-diffusion-xl-1024-v1-0')
    # ============ DISABLED APIS ============
    # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    
    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    
    # Application
    APP_NAME = os.getenv('APP_NAME', 'GyanGuru')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    # Generation Settings
    TEMPERATURE = 0.7
    TOP_P = 0.95
    MAX_OUTPUT_TOKENS = 4096

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}