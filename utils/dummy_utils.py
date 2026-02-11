
# utils/dummy_utils.py
class DummyGemini:
    def generate_text_explanation(self, topic, complexity="Comprehensive"):
        return f"# {topic}\n\nThis is dummy content. Add OpenAI API key."

    def generate_code(self, algorithm, complexity="Detailed"):
        return f'print("Dummy code for {algorithm}")'

    def generate_audio_script(self, topic, length="Brief"):
        return f"Audio script about {topic}."

    def generate_image_prompts(self, concept):
        return "1. Diagram 1\n2. Diagram 2\n3. Diagram 3"

def extract_code(text):
    import re
    match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text