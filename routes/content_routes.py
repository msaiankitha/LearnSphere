from flask import Blueprint, render_template, request, jsonify, send_file
from config import Config
import os
import re
# ============ CREATE BLUEPRINT ============
content_bp = Blueprint('content', __name__)
# ==========================================

# ============ USE GROQ (FREE TIER) ============
if Config.GROQ_API_KEY and Config.GROQ_API_KEY.startswith('gsk_'):
    try:
        # ✅ IMPORTANT: Capital 'U' in GroqUtils
        from utils.groq_utils import GroqUtils as AIUtils
        from utils.groq_utils import extract_code
        print("✅ Using Groq API (FREE TIER - 1000 requests/day!)")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        from utils.dummy_utils import DummyGemini as AIUtils
        from utils.dummy_utils import extract_code
        print("⚠️ Falling back to DUMMY mode")
else:
    from utils.dummy_utils import DummyGemini as AIUtils
    from utils.dummy_utils import extract_code
    print("⚠️ Using DUMMY mode - Add GROQ_API_KEY to .env for real AI")
# ==============================================

from utils.audio_utils import AudioUtils
from utils.image_utils import ImageUtils
from utils.code_utils import CodeUtils

# Initialize utilities
ai_utils = AIUtils()
audio_utils = AudioUtils()
image_utils = ImageUtils()
code_utils = CodeUtils()

# Cleanup old audio files on startup
audio_utils.cleanup_old_files()

# ============ HOME ROUTE ============
@content_bp.route('/')
def index():
    return render_template('index.html', app_name=Config.APP_NAME)

@content_bp.route('/text')
def text_page():
    return render_template('text.html', app_name=Config.APP_NAME)

@content_bp.route('/code')
def code_page():
    return render_template('code.html', app_name=Config.APP_NAME)

@content_bp.route('/audio')
def audio_page():
    return render_template('audio.html', app_name=Config.APP_NAME)

@content_bp.route('/images')
def images_page():
    return render_template('images.html', app_name=Config.APP_NAME)

@content_bp.route('/about')
def about_page():
    return render_template('about.html', app_name=Config.APP_NAME)

# ============ API ROUTES ============
@content_bp.route('/api/generate/text', methods=['POST'])
def generate_text():
    try:
        data = request.json
        topic = data.get('topic', '')
        complexity = data.get('complexity', 'Comprehensive')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        explanation = ai_utils.generate_text_explanation(topic, complexity)
        
        return jsonify({
            'success': True,
            'explanation': explanation,
            'topic': topic,
            'complexity': complexity
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/api/generate/code', methods=['POST'])
def generate_code():
    try:
        data = request.json
        algorithm = data.get('algorithm', '')
        complexity = data.get('complexity', 'Detailed')
        
        if not algorithm:
            return jsonify({'error': 'Algorithm/topic is required'}), 400
        
        generated = ai_utils.generate_code(algorithm, complexity)
        code = extract_code(generated)
        
        result = code_utils.save_code_file(code, algorithm)
        
        return jsonify({
            'success': True,
            'code': code,
            'full_response': generated,
            'file_info': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/api/generate/audio', methods=['POST'])
def generate_audio():
    try:
        data = request.json
        topic = data.get('topic', '')
        length = data.get('length', 'Brief')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        script = ai_utils.generate_audio_script(topic, length)
        audio_result = audio_utils.text_to_speech(script, topic)
        
        return jsonify({
            'success': True,
            'script': script,
            'audio': audio_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/api/generate/images', methods=['POST'])
def generate_images():
    """API endpoint for ACTUAL image generation with improved prompts"""
    try:
        data = request.json
        concept = data.get('concept', '')
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        # Generate professional prompts using Groq
        print(f"🤖 Generating professional prompts for: {concept}")
        prompts_text = ai_utils.generate_image_prompts(concept)
        
        # Parse and clean prompts
        prompts = []
        for line in prompts_text.split('\n'):
            line = line.strip()
            if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                # Remove the numbering
                clean_line = re.sub(r'^[\d\.\s]+', '', line)
                if clean_line and len(clean_line) > 30:  # Only use detailed prompts
                    prompts.append(clean_line)
        
        # Fallback prompts if Groq fails
        if not prompts:
            prompts = [
                f"Professional LSTM cell diagram with input gate, forget gate, output gate, cell state Ct, hidden state ht, sigmoid and tanh activations, labeled components, color-coded, vector graphics, academic style",
                f"{concept} architecture visualization showing data flow, recurrent connections, gates operations, precise technical labels, clean lines, white background",
                f"Educational diagram of {concept} for machine learning textbook, detailed components, arrows showing information flow, publication quality"
            ]
        
        # Initialize image generator
        from utils.image_generator import ImageGenerator
        img_gen = ImageGenerator()
        
        # Strong negative prompt to avoid garbage
        negative_prompt = "blurry, low quality, distorted, deformed, watermark, signature, text errors, wrong labels, h1 h2 h3, generic labels, unlabeled, chaotic, messy, hand-drawn, sketch, photograph"
        
        # Generate images with improved settings
        images = []
        for i, prompt in enumerate(prompts[:3]):
            print(f"\n🎨 Generating image {i+1}/3")
            
            # Progressive quality settings
            if i == 0:
                result = img_gen.generate_image(prompt, negative_prompt, steps=40, guidance_scale=7.5)
            elif i == 1:
                result = img_gen.generate_image(prompt, negative_prompt, steps=45, guidance_scale=7.8)
            else:
                result = img_gen.generate_image(prompt, negative_prompt, steps=50, guidance_scale=8.0)
            
            images.append(result)
        
        return jsonify({
            'success': True,
            'concept': concept,
            'prompts': prompts[:3],
            'images': images
        })
        
    except Exception as e:
        print(f"❌ Error in generate_images: {str(e)}")
        return jsonify({'error': str(e)}), 500

@content_bp.route('/api/download/<file_type>/<filename>')
def download_file(file_type, filename):
    try:
        folder_map = {
            'code': 'code',
            'audio': 'audio',
            'image': 'images'
        }
        
        folder = folder_map.get(file_type)
        if not folder:
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(Config.UPLOAD_FOLDER, folder, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500