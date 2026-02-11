# utils/google_image_search.py
import requests
from config import Config
import os
import uuid
from datetime import datetime
import urllib.parse

class GoogleImageSearch:
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.cx = Config.GOOGLE_CX_ID
        self.upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'images')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def search_images(self, query, num=5):
        """
        Search for REAL educational images from Google
        """
        try:
            # Encode query for URL
            encoded_query = urllib.parse.quote(query)
            
            # Google Custom Search JSON API endpoint
            url = f"https://www.googleapis.com/customsearch/v1"
            
            params = {
                'key': self.api_key,
                'cx': self.cx,
                'q': query,
                'searchType': 'image',
                'num': min(num, 10),  # Max 10 per request
                'imgSize': 'large',
                'imgType': 'photo',
                'safe': 'active',
                'fields': 'items(title,link,displayLink,image/thumbnailLink,image/contextLink)'
            }
            
            print(f"🔍 Searching Google Images for: {query}")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                results = []
                for item in items[:num]:
                    # Download the actual image
                    img_url = item['link']
                    img_data = self._download_image(img_url)
                    
                    if img_data:
                        filename = self._save_image(img_data, query)
                        results.append({
                            'success': True,
                            'filename': filename,
                            'filepath': f'/static/uploads/images/{filename}',
                            'title': item.get('title', ''),
                            'source': item.get('displayLink', ''),
                            'context': item.get('image', {}).get('contextLink', ''),
                            'is_real': True,
                            'query': query
                        })
                
                print(f"✅ Found {len(results)} real images")
                return results
            else:
                print(f"❌ Google API Error: {response.status_code}")
                return self._create_educational_placeholder(query)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._create_educational_placeholder(query)
    
    def _download_image(self, url):
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.content
        except:
            pass
        return None
    
    def _save_image(self, image_data, query):
        """Save downloaded image"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        clean_query = query.replace(' ', '_')[:30]
        filename = f"google_{clean_query}_{timestamp}_{unique_id}.jpg"
        filepath = os.path.join(self.upload_folder, filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filename
    
    def _create_educational_placeholder(self, query):
        """Fallback when Google fails"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"fallback_{timestamp}_{unique_id}.txt"
        filepath = os.path.join(self.upload_folder, filename)
        
        content = f"""🔍 EDUCATIONAL IMAGE SEARCH: {query}

To get REAL images:
1. Get Google API Key: https://developers.google.com/custom-search/v1/introduction
2. Get CX ID: https://programmablesearchengine.google.com/
3. Add to .env:
   GOOGLE_API_KEY=your_key_here
   GOOGLE_CX_ID=your_cx_here

Example search URLs for {query}:
- https://en.wikipedia.org/wiki/{query.replace(' ', '_')}
- https://www.researchgate.net/search?q={query.replace(' ', '+')}
- https://scholar.google.com/scholar?q={query.replace(' ', '+')}+diagram
"""
        with open(filepath, 'w') as f:
            f.write(content)
        
        return [{
            'success': False,
            'filename': filename,
            'filepath': f'/static/uploads/images/{filename}',
            'is_placeholder': True,
            'content': content,
            'query': query
        }]