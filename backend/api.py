from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import math
from textblob import TextBlob
from tweetgenerator import AdvancedTweetGenerator

app = Flask(__name__)
CORS(app)

# Load prediction model and encoders
model = joblib.load('like_predictor.pkl')
le_company = joblib.load('le_company.pkl')
le_username = joblib.load('le_username.pkl')
le_day = joblib.load('le_day.pkl')

generator = AdvancedTweetGenerator()

def safe_label_transform(le, value):
    if value in le.classes_:
        return le.transform([value])[0]
    else:
        return -1

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Basic error handling
    content = data.get('content', "").strip()
    if not content:
        return jsonify({
            'success': False,
            'error': "Content (tweet text) cannot be empty! ✍️"
        }), 400

    try:
        has_media = int(bool(data.get('has_media', False)))
        hour = int(data.get('hour', 12))
        day = data.get('day', 'Monday')
        username = data.get('username', 'AnonymousUser')
        company = data.get('company', 'UnknownCompany')

        word_count = len(content.split())
        char_count = len(content)
        sentiment = TextBlob(content).sentiment.polarity

        company_encoded = safe_label_transform(le_company, company)
        username_encoded = safe_label_transform(le_username, username)
        day_encoded = safe_label_transform(le_day, day)

        features = np.array([
            has_media,
            hour,
            word_count,
            char_count,
            sentiment,
            company_encoded,
            username_encoded,
            day_encoded
        ]).reshape(1, -1)

        log_likes = model.predict(features)[0]
        predicted_likes = int(round(math.exp(log_likes)))

        # Emoji badges
        if predicted_likes >= 1000:
            popularity = "🔥 Viral Alert!"
        elif predicted_likes >= 100:
            popularity = "🚀 Trending Soon"
        else:
            popularity = "📈 Growing Reach"

        return jsonify({
            'success': True,
            'predicted_likes': predicted_likes,
            'popularity_estimate': popularity,
            'details': {
                'word_count': word_count,
                'sentiment': f"{sentiment:.2f}",
                'company': company,
                'username': username,
                'day': day,
                'hour_of_posting': hour,
                'has_media': bool(has_media)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json(force=True)

        message = data.get('message', '').strip()
        if not message:
            return jsonify({
                'success': False,
                'error': "Please provide a message to base the tweet on! 📝"
            }), 400

        company = data.get('company', 'Our Company')
        industry = data.get('industry', 'general')
        brand_voice = data.get('brand_voice', 'casual')
        word_count_target = int(data.get('word_count_target', 25))
        sentiment_target = float(data.get('sentiment_target', 0.0))
        has_media = bool(data.get('has_media', False))

        generated_tweet = generator.generate_smart_tweet(
            company=company,
            industry=industry,
            brand_voice=brand_voice,
            message=message,
            word_count_target=word_count_target,
            sentiment_target=sentiment_target,
            has_media=has_media
        )

        return jsonify({
            'success': True,
            'generated_tweet': generated_tweet,
            'description': "🎉 Here's your AI-crafted tweet! 🚀",
            'info': {
                'brand_voice': brand_voice,
                'industry': industry,
                'word_goal': word_count_target,
                'sentiment_goal': sentiment_target
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
