# utils/groq_utils.py
from groq import Groq
from config import Config  # ✅ THIS WAS MISSING!
import re
import time

class GroqUtils:
    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(
            api_key=Config.GROQ_API_KEY  # ✅ Now Config is defined
        )
        self.model = Config.GROQ_MODEL  # ✅ Now Config is defined
    
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
                temperature=0.3,
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
        """Generate PROFESSIONAL educational diagram prompts"""
        prompt = f"""Create 3 professional educational diagram prompts for visualizing {concept} in machine learning.

    CRITICAL REQUIREMENTS - MUST FOLLOW:
    1. NO generic "h1, h2, h3" labels - use MEANINGFUL terms (Input Gate, Forget Gate, Cell State, Hidden State)
    2. SPECIFIC architecture: show exact gates, data flow, and mathematical operations
    3. STYLE: clean academic illustration, vector graphics style, white background
    4. DETAIL: include labels, arrows, and color coding
    5. EDUCATIONAL: must accurately represent {concept} for teaching

    Example GOOD prompt for LSTM:
    "Professional LSTM cell diagram showing:
    - Input Gate (σ) with xt and ht-1 inputs
    - Forget Gate (σ) with xt and ht-1
    - Cell State (Ct) horizontal line running through top
    - Hidden State (ht) output
    - Tanh activation functions
    - Pointwise multiplication operations
    - Color coded: gates in blue, cell state in green, hidden state in orange
    - Clean lines, academic style, white background"

    Return ONLY the 3 numbered prompts, each with detailed specifications."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating professional educational diagrams for ML/AI textbooks and courses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,  # Lower temperature for more consistent results
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
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = 20 * (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise e
        return None


def extract_code(text):
    """Extract Python code from markdown response"""
    import re
    code_pattern = r'```python\n(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    code_pattern = r'```\n(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    code_pattern = r'```(.*?)```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    return text