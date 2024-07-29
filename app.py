
from flask import Flask, jsonify, request
from recommendation_engine import prepare_dataframe, vectorize_text, get_recommendations
import requests
import json
from config import DevelopmentConfig  # Import the appropriate config class
from Filters import Locations
from urllib.parse import urlencode

app = Flask(__name__)

# Load configurations
app.config.from_object(DevelopmentConfig)
news_api_key = app.config['NEWS_API_KEY']

# Provide the news based on the user's location
location = Locations.get_user_country()

# Fetch news based on provided query parameters including categories
@app.route('/api/news/search', methods=['GET'])
def fetch_news():
    query_params = request.args.to_dict()

    query_params['apikey'] = news_api_key

    if 'location' not in query_params:
        query_params['country'] = location

    url = f"https://newsdata.io/api/1/latest?{urlencode(query_params)}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad response status

        data = response.json()
        articles = data.get('results', [])

        # Extract relevant information from articles if needed
        #extracted_articles = [{'title': article['title'], 'description': article['description']} for article in articles]
        return jsonify({'articles': articles}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

# Recommend top 5 articles most relevant to the keyword within the retrieved articles
@app.route('/api/news/recommendations', methods=['GET'])
def get_recommendations_route():
    query_params = request.args.to_dict()

    if 'q' not in query_params:
        return jsonify({'error': 'Query parameter "keyword" is required'}), 400

    query_params['apikey'] = news_api_key

    url = f"https://newsdata.io/api/1/latest?{urlencode(query_params)}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad response status
    data = response.json()
    articles = data.get('results', [])
    recommendations = get_recommendations(query_params['q'], articles)
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True)
