# app.py

from flask import Flask, jsonify, request
import sqlite3
from recommendation_engine import prepare_dataframe, vectorize_text, get_recommendations
import requests
import json
from config import DevelopmentConfig  # Import the appropriate config class
from Filters import Locations

app = Flask(__name__)

# Load configurations
app.config.from_object(DevelopmentConfig);
news_api_key = app.config['NEWS_API_KEY']

#providing the news based on the users location
location = Locations.get_user_country();
print(location)


#It fetches everything about the provided keyword
@app.route('/api/news/fetch', methods=['GET'])
def fetch_news():
    keyword = request.args.get('q')
    if not keyword:
        return jsonify({'error': 'Missing query parameter "q"'}), 400

    url = f'https://newsdata.io/api/1/latest?q={keyword}&country={location}&apikey={news_api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad response status

        data = response.json()
        articles = data.get('articles', [])

        # Extract relevant information from articles if needed
        extracted_articles = [{'title': article['title'], 'description': article['description']} for article in articles]
        return jsonify({'articles': data}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

#When the user inputs a keyword, such as "Indian politics," 
#the function first searches for all articles related to this keyword.
#Then, within those retrieved articles, it recommends the top 5 articles most relevant to the keyword.
@app.route('/api/news/recommendations', methods=['GET'])
def get_recommendations_route():
    keyword = request.args.get('keyword');
    if not keyword:
        return jsonify({'error': 'Query parameter "keyword" is required'}), 400
    url = f'https://newsdata.io/api/1/latest?q={keyword}&country={location}&apikey={news_api_key}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad response status
    data = response.json()
    articles = data.get('results', [])
    print(articles)
    
    recommendations = get_recommendations(keyword, articles)
    return jsonify(recommendations), 200
