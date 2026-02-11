# utils/image_generator.py
import os
import uuid
from datetime import datetime
from config import Config
import requests
import base64
from PIL import Image
from io import BytesIO

class ImageGenerator:
    def __init__(self):
        """Initialize image generator with Stability AI"""
        self.api_key = Config.STABILITY_API_KEY
        self.engine = Config.STABILITY_ENGINE
        self.upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'images')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def generate_image(self, prompt, negative_prompt="", steps=30, guidance_scale=7.0):
        """
        Generate actual image using Stability AI
        
        Args:
            prompt: str - The image description
            negative_prompt: str - What NOT to generate (prevents garbage)
            steps: int - Number of diffusion steps (higher = better quality, slower)
            guidance_scale: float - How closely to follow prompt (7.0-8.5 is good)
        
        Returns: dict with image info or placeholder
        """
        try:
            # Stability AI API endpoint
            url = f"https://api.stability.ai/v1/generation/{self.engine}/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Build the request body
            body = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1.0
                    }
                ],
                "cfg_scale": guidance_scale,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": steps,
            }
            
            # Add negative prompt if provided (prevents bad generations)
            if negative_prompt:
                body["text_prompts"].append({
                    "text": negative_prompt,
                    "weight": -1.0
                })
            
            print(f"🎨 Generating image for: {prompt[:50]}...")
            print(f"⚙️ Steps: {steps}, CFG Scale: {guidance_scale}")
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save the generated image
                for i, image in enumerate(data["artifacts"]):
                    img_data = base64.b64decode(image["base64"])
                    img = Image.open(BytesIO(img_data))
                    
                    # Generate filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_id = str(uuid.uuid4())[:8]
                    filename = f"stability_{timestamp}_{unique_id}.png"
                    filepath = os.path.join(self.upload_folder, filename)
                    
                    # Save image
                    img.save(filepath)
                    print(f"✅ Image saved: {filename}")
                    
                    return {
                        'success': True,
                        'filename': filename,
                        'filepath': filepath,
                        'url': f'/static/uploads/images/{filename}',
                        'prompt': prompt,
                        'negative_prompt': negative_prompt,
                        'steps': steps,
                        'guidance_scale': guidance_scale
                    }
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return self._create_placeholder(prompt, f"API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return self._create_placeholder(prompt, str(e))
    
    def generate_multiple_images(self, prompts, max_images=3, negative_prompt=""):
        """
        Generate multiple images from prompts
        
        Args:
            prompts: list - List of image prompts
            max_images: int - Maximum number of images to generate
            negative_prompt: str - What to avoid in ALL generations
        """
        images = []
        for i, prompt in enumerate(prompts[:max_images]):
            print(f"\n📸 Generating image {i+1}/{min(len(prompts), max_images)}")
            
            # Use different parameters for different images
            if i == 0:
                # First image - standard quality
                result = self.generate_image(prompt, negative_prompt, steps=30, guidance_scale=7.0)
            elif i == 1:
                # Second image - higher quality, more creative
                result = self.generate_image(prompt, negative_prompt, steps=40, guidance_scale=7.5)
            else:
                # Third image - highest quality
                result = self.generate_image(prompt, negative_prompt, steps=50, guidance_scale=8.0)
                
            images.append(result)
        return images
    
    def generate_with_improved_prompt(self, concept, detailed_prompt):
        """
        Generate image with pre-crafted professional prompt
        This ensures high-quality educational diagrams
        """
        # Professional educational diagram prompt template
        base_prompt = f"""Professional educational diagram of {concept}, 
machine learning textbook style, clean vector illustration, 
white background, precise technical labels, color-coded components, 
data flow arrows, academic publication quality, 4K resolution, 
detailed architecture visualization, sharp lines, clear typography"""

        # Strong negative prompt to avoid garbage
        negative = """blurry, low quality, distorted, deformed, 
watermark, signature, text errors, wrong labels, h1 h2 h3, 
generic labels, unlabeled, chaotic, messy, hand-drawn, 
sketch, doodle, photograph, realistic, 3D render, low resolution, 
pixelated, bad anatomy, extra limbs, extra features"""
        
        return self.generate_image(
            prompt=base_prompt + " " + detailed_prompt,
            negative_prompt=negative,
            steps=50,
            guidance_scale=8.0
        )
    
    def _create_placeholder(self, prompt, error_msg=""):
        """Create placeholder when image generation fails"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"placeholder_{timestamp}_{unique_id}.txt"
        filepath = os.path.join(self.upload_folder, filename)
        
        content = f"""⚠️ IMAGE GENERATION FAILED

Prompt: {prompt}
Error: {error_msg}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

To fix this:
1. Check your STABILITY_API_KEY in .env file
2. Make sure you have credits at https://platform.stability.ai
3. Try again later

Example working prompts for LSTM:
--------------------------------
✓ "Professional LSTM cell diagram showing input gate, forget gate, output gate, cell state Ct, hidden state ht, tanh activations, pointwise multiplication, color-coded: input gate blue, forget gate red, output gate green, cell state purple, clean academic style"

✓ "LSTM architecture visualization with data flow from left to right, xt input at bottom, ht-1 recurrent connection, Ct horizontal cell state line, sigmoid and tanh functions, labeled equations, vector graphics, white background"
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            'success': False,
            'filename': filename,
            'filepath': filepath,
            'url': None,
            'is_placeholder': True,
            'content': content,
            'error': error_msg,
            'prompt': prompt
        }