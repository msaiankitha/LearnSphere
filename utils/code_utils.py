import ast
import re
from datetime import datetime
import os
from config import Config
import uuid

class CodeUtils:
    def __init__(self):
        self.upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'code')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def detect_dependencies(self, code):
        """
        Parse Python code and detect required dependencies
        """
        dependencies = set()
        
        # Common ML library mappings
        lib_mapping = {
            'sklearn': 'scikit-learn',
            'tensorflow': 'tensorflow',
            'torch': 'pytorch',
            'keras': 'keras',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
            'cv2': 'opencv-python',
            'PIL': 'pillow',
            'xgboost': 'xgboost',
            'lightgbm': 'lightgbm',
            'transformers': 'transformers'
        }
        
        # Parse imports
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base = alias.name.split('.')[0]
                        if base in lib_mapping:
                            dependencies.add(lib_mapping[base])
                        else:
                            dependencies.add(base)
                elif isinstance(node, ast.ImportFrom):
                    base = node.module.split('.')[0] if node.module else ''
                    if base in lib_mapping:
                        dependencies.add(lib_mapping[base])
                    elif base:
                        dependencies.add(base)
        except:
            # Fallback to regex
            import_pattern = r'(?:from|import)\s+([a-zA-Z0-9_]+)'
            matches = re.findall(import_pattern, code)
            for match in matches:
                base = match.split('.')[0]
                if base in lib_mapping:
                    dependencies.add(lib_mapping[base])
                elif base not in ['os', 'sys', 'time', 'datetime', 'math', 'random']:
                    dependencies.add(base)
        
        return list(dependencies)
    
    def save_code_file(self, code, topic):
        """
        Save generated code to file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{topic.replace(' ', '_')}_{timestamp}_{unique_id}.py"
        filepath = os.path.join(self.upload_folder, filename)
        
        # Detect dependencies
        dependencies = self.detect_dependencies(code)
        
        # Add header with instructions
        header = f'''"""
===============================================================================
ML Learning Assistant - Generated Code
Topic: {topic}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DEPENDENCIES:
{chr(10).join(['pip install ' + dep for dep in dependencies]) if dependencies else 'No external dependencies required'}

INSTRUCTIONS:
1. Install required dependencies using pip
2. Run this script in your Python environment
3. For Google Colab: Copy and paste directly
===============================================================================
"""

'''
        
        full_code = header + code
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_code)
        
        return {
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'url': f'/static/uploads/code/{filename}',
            'dependencies': dependencies,
            'code': full_code
        }
    
    def generate_colab_link(self, code):
        """
        Generate Google Colab link with pre-filled code
        """
        import base64
        from urllib.parse import quote
        
        # Simple colab link (opens new notebook)
        colab_url = "https://colab.research.google.com/#create=true"
        
        return {
            'colab_url': colab_url,
            'instructions': 'Click to create new Colab notebook, then paste the code'
        }