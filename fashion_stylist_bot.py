from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Rate limiting
class RateLimiter:
    def __init__(self, max_calls=10, period=60):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def allow_request(self):
        now = time.time()
        self.calls = [c for c in self.calls if now - c < self.period]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

rate_limiter = RateLimiter(max_calls=10, period=60)

# Gemini API setup
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    'temperature': 0.7,
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 8192,
    'stop_sequences': None,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Translations
TRANSLATIONS = {
    'en': {
        'title': 'StyleBot 👗',
        'subtitle': 'Your AI-Powered Personal Stylist',
        'ask': 'Describe your style, occasion, or ask anything...',
        'send': 'Send',
        'trends': 'Get Fashion Trends',
        'rate_limit': 'Rate limit exceeded. Please wait a moment.',
        'error': 'Error occurred. Please try again.'
    },
    'kn': {
        'title': 'ಸ್ಟೈಲ್ಬಾಟ್ 👗',
        'subtitle': 'ನಿಮ್ಮ AI-ಚಾಲಿತ ವೈಯಕ್ತಿಕ ಸ್ಟೈಲಿಸ್ಟ್',
        'ask': 'ನಿಮ್ಮ ಶೈಲಿ, ಸಂದರ್ಭ ವಿವರಿಸಿ ಅಥವಾ ಏನನ್ನಾದರೂ ಕೇಳಿ...',
        'send': 'ಕಳುಹಿಸಿ',
        'trends': 'ಫ್ಯಾಶನ್ ಟ್ರೆಂಡ್‌ಗಳನ್ನು ಪಡೆಯಿರಿ',
        'rate_limit': 'ದರ ಮಿತಿ ಮೀರಿದೆ. ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಕಾಯಿರಿ.',
        'error': 'ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.'
    },
    'hi': {
        'title': 'स्टाइलबॉट 👗',
        'subtitle': 'आपका AI-संचालित व्यक्तिगत स्टाइलिस्ट',
        'ask': 'अपनी शैली, अवसर का वर्णन करें या कुछ भी पूछें...',
        'send': 'भेजें',
        'trends': 'फैशन ट्रेंड्स प्राप्त करें',
        'rate_limit': 'दर सीमा पार हो गई। कृपया थोड़ी देर प्रतीक्षा करें।',
        'error': 'त्रुटि हुई। कृपया पुनः प्रयास करें।'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_translations/<lang>')
def get_translations(lang):
    return jsonify(TRANSLATIONS.get(lang, TRANSLATIONS['en']))

@app.route('/style_advice', methods=['POST'])
def style_advice():
    if not rate_limiter.allow_request():
        return jsonify({'error': 'rate_limit'}), 429
    
    data = request.json
    query = data.get('query', '')
    language = data.get('language', 'en')
    
    if not query:
        return jsonify({'error': 'Please describe what you need'}), 400
    
    lang_instruction = "Respond in English" if language == 'en' else ("Respond in Kannada (ಕನ್ನಡ)" if language == 'kn' else "Respond in Hindi (हिंदी)")
    
    prompt = f"""{lang_instruction}. You are a friendly, professional fashion stylist.

User: "{query}"

Provide COMPLETE and DETAILED advice. Do not stop mid-sentence. Include:
1. Full outfit suggestions with specific items
2. Complete color combinations
3. All accessories recommendations
4. Complete styling tips

Make sure to finish all your thoughts and sentences completely."""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            
            # Check if response is complete
            if response.text and len(response.text) > 50:
                return jsonify({'advice': response.text})
            else:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return jsonify({'advice': response.text if response.text else 'Response too short, please try again.'})
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return jsonify({'error': 'Unable to connect to AI service. Please try again.'}), 500

@app.route('/fashion_trends', methods=['POST'])
def fashion_trends():
    if not rate_limiter.allow_request():
        return jsonify({'error': 'rate_limit'}), 429
    
    data = request.json
    language = data.get('language', 'en')
    
    lang_instruction = "Respond in English" if language == 'en' else ("Respond in Kannada (ಕನ್ನಡ)" if language == 'kn' else "Respond in Hindi (हिंदी)")
    prompt = f"""{lang_instruction}. List 5 current fashion trends for {datetime.now().strftime('%B %Y')} with brief styling tips."""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            
            if response.text and len(response.text) > 50:
                return jsonify({'trends': response.text})
            else:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return jsonify({'trends': response.text if response.text else 'Response too short, please try again.'})
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return jsonify({'error': 'Unable to connect to AI service. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
