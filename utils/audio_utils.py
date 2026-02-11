from gtts import gTTS
import os
from datetime import datetime
from config import Config
import uuid

class AudioUtils:
    def __init__(self):
        self.upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'audio')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def text_to_speech(self, text, topic):
        """
        Convert text to speech and save as MP3
        """
        try:
            # Clean text for better TTS
            clean_text = text.replace('*', '').replace('#', '').replace('`', '')
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{topic.replace(' ', '_')}_{timestamp}_{unique_id}.mp3"
            filepath = os.path.join(self.upload_folder, filename)
            
            # Create TTS
            tts = gTTS(text=clean_text, lang='en', slow=False)
            tts.save(filepath)
            
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'url': f'/static/uploads/audio/{filename}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def cleanup_old_files(self, hours=24):
        """Remove audio files older than specified hours"""
        import time
        current_time = time.time()
        
        for filename in os.listdir(self.upload_folder):
            filepath = os.path.join(self.upload_folder, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getctime(filepath)
                if file_age > (hours * 3600):
                    os.remove(filepath)