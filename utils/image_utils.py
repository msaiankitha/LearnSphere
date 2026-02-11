import os
import uuid
from datetime import datetime
from config import Config

class ImageUtils:
    def __init__(self):
        """Initialize image utilities - NO GEMINI"""
        self.upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'images')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def generate_with_gemini(self, prompt):
        """This function is deprecated - using placeholder instead"""
        return self.save_placeholder_diagram(prompt)
    
    def save_placeholder_diagram(self, concept):
        """Create placeholder with concept explanation"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"diagram_{timestamp}_{unique_id}.txt"
            filepath = os.path.join(self.upload_folder, filename)
            
            content = f"""Educational Diagram: {concept}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is a placeholder for an AI-generated diagram description.
We're using OpenAI for text generation, but image generation is handled separately.

Diagram Description for {concept}:
===================================

A clear educational visualization showing the key components of {concept}
with labeled elements and data flow.

Educational Value:
This diagram helps learners understand the structure and flow of {concept}
in an intuitive visual manner."""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'url': f'/static/uploads/images/{filename}',
                'is_placeholder': True,
                'content': content
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}