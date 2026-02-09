# Fashion Stylist Bot 👗

An interactive AI-powered fashion stylist that provides personalized outfit suggestions, styling tips, and fashion trends in English and Kannada.

## Features

✨ **Multilingual Support**: Switch between English and Kannada (ಕನ್ನಡ)
🌤️ **Weather-Based Suggestions**: Get outfits suitable for current weather
🎉 **Occasion-Specific Styling**: Recommendations for casual, formal, party, wedding, work
💅 **Personal Style Preferences**: Modern, traditional, bohemian, minimalist, vintage
📈 **Fashion Trends**: Stay updated with current fashion trends
🤖 **AI-Powered**: Uses Google Gemini API for intelligent suggestions

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment
Create a `.env` file:
```bash
GEMINI_API_KEY=your-actual-api-key-here
```

Or set it directly in the code (line 21 of fashion_stylist_bot.py)

### 4. Run the Application
```bash
python fashion_stylist_bot.py
```

### 5. Open in Browser
Navigate to: `http://localhost:5000`

## Usage

1. **Select Context** (optional):
   - Choose weather condition
   - Select occasion type
   - Pick your style preference

2. **Ask Questions**:
   - "What should I wear for a summer wedding?"
   - "Suggest casual outfits for rainy weather"
   - "Give me minimalist work outfit ideas"

3. **Get Trends**:
   - Click "Get Current Fashion Trends" button

4. **Switch Language**:
   - Click "EN / ಕನ್ನಡ" button in top-right

## Limitations & Rate Limits

### API Rate Limiting
- **10 requests per minute** per user
- Prevents API quota exhaustion
- Shows friendly error message when limit exceeded

### Gemini API Free Tier Limits
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**

### Best Practices
- Use specific queries for better results
- Combine weather/occasion/style for targeted advice
- Wait a minute if rate limit is reached

## Technical Details

### Architecture
- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **AI Model**: Google Gemini Pro
- **Rate Limiting**: In-memory time-based limiter

### File Structure
```
fashion_stylist_bot.py    # Main Flask application
templates/
  └── index.html          # Frontend UI
requirements.txt          # Python dependencies
.env.example             # Environment template
README.md                # Documentation
```

### API Endpoints
- `GET /` - Main application page
- `GET /get_translations/<lang>` - Get UI translations
- `POST /style_advice` - Get styling recommendations
- `POST /fashion_trends` - Get current fashion trends

## Customization

### Add More Languages
Edit `TRANSLATIONS` dictionary in `fashion_stylist_bot.py`:
```python
TRANSLATIONS = {
    'en': {...},
    'kn': {...},
    'hi': {...}  # Add Hindi
}
```

### Adjust Rate Limits
Modify `RateLimiter` initialization:
```python
rate_limiter = RateLimiter(max_calls=20, period=60)  # 20 per minute
```

### Change AI Model
Update model initialization:
```python
model = genai.GenerativeModel('gemini-pro-vision')  # For image support
```

## Troubleshooting

### "Rate limit exceeded"
Wait 60 seconds before making new requests.

### "API key not valid"
Ensure your Gemini API key is correctly set in `.env` or code.

### "Module not found"
Run `pip install -r requirements.txt` again.

### No response from AI
Check your internet connection and API key validity.

## Future Enhancements

- 🖼️ Visual outfit mockups using Gemini Pro Vision
- 📱 Mobile app version
- 💾 User preference saving
- 🌐 More language support
- 🎨 Fashion mood board generation
- 👤 User authentication

## License

MIT License - Feel free to modify and use for your projects!

## Credits

Built with ❤️ using Google Gemini API
