import openai
from config import Config
import re
import time

class OpenAIUtils:
    def __init__(self):
        """Initialize OpenAI with API key"""
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        
    def generate_text_explanation(self, topic, complexity="Comprehensive"):
        """Generate educational text explanation for ML concepts"""
        prompts = {
            "Brief": f"Explain {topic} in machine learning briefly in 2-3 paragraphs. Include key concepts and a simple example.",
            "Detailed": f"Provide a detailed explanation of {topic} in machine learning with examples and applications.",
            "Comprehensive": f"""Create a comprehensive educational guide about {topic} in machine learning with:
1. Learning objectives
2. Core concepts and mathematical foundations
3. Step-by-step explanation
4. Practical applications
5. Common challenges and solutions
6. Key takeaways

Format with clear headings and bullet points."""
        }
        
        prompt = prompts.get(complexity, prompts["Comprehensive"])
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert machine learning educator. Create clear, accurate, and educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_OUTPUT_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def generate_code(self, algorithm, complexity="Detailed"):
        """Generate Python code for ML algorithms"""
        prompt = f"""Write production-ready Python code for {algorithm} in machine learning.

Requirements:
- Complete, runnable implementation
- Detailed comments explaining each step
- Include necessary imports
- Add error handling
- Include example usage
- Add visualization where applicable

Code should be for: {complexity} implementation level
Format the code with proper indentation and docstrings."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer specializing in machine learning. Write clean, efficient, well-documented code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent code
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating code: {str(e)}"
    
    def generate_audio_script(self, topic, length="Brief"):
        """Generate conversational script for audio learning"""
        prompts = {
            "Brief": f"Create a 1-minute conversational audio script explaining {topic} in machine learning. Use natural, spoken language. Start with 'Welcome to GyanGuru...'",
            "Detailed": f"Create a 3-minute educational audio script about {topic} in machine learning. Include examples and speak directly to the learner. Make it engaging and conversational."
        }
        
        prompt = prompts.get(length, prompts["Brief"])
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a friendly, engaging audio educator. Create conversational scripts that are easy to listen to and understand."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    def generate_image_prompts(self, concept):
        """Generate optimized prompts for image generation"""
        prompt = f"""Create 3 detailed image generation prompts for visualizing {concept} in machine learning.

Each prompt should:
1. Describe a clear educational diagram
2. Include visual elements, labels, and colors
3. Specify style (technical diagram, educational illustration)
4. Be detailed enough for DALL-E or Stable Diffusion to generate

Return as numbered list with clear descriptions."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating detailed image generation prompts for educational diagrams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating prompts: {str(e)}"
    
    def generate_with_retry(self, prompt, max_retries=3):
        """Generate content with automatic retry on rate limits"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert machine learning educator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_OUTPUT_TOKENS
                )
                return response.choices[0].message.content
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = 20 * (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise e
        return None


# ============= EXTRACT CODE FUNCTION =============
def extract_code(text):
    """
    Extract Python code from markdown response
    """
    import re
    
    # Try to find Python code blocks
    code_pattern = r'```python\n(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    # Try without language specifier
    code_pattern = r'```\n(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    # Try to find any code block
    code_pattern = r'```(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    # If no code blocks found, return the original text
    return text