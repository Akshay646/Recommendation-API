
from flask import Flask, jsonify, request
from recommendation_engine import prepare_dataframe, vectorize_text, get_recommendations
import requests
import json
from config import DevelopmentConfig  # Import the appropriate config class
from Filters import Locations
from urllib.parse import urlencode
from pymongo import MongoClient


app = Flask(__name__)

# Load configurations
app.config.from_object(DevelopmentConfig)
news_api_key = app.config['NEWS_API_KEY']
base_url = app.config['BASE_URL']

# MongoDB Configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['News']
collection = db['DataSet']

# Recommend top 5 articles most relevant to the keyword within the retrieved articles
@app.route('/api/news/recommendations', methods=['POST'])  # Changed to POST to handle body data
def get_recommendations_route():
    # Extract the 'description' from the request body
    request_data = request.get_json()
    description = request_data.get('description')
    
    # Fetch data from MongoDB
    articles = list(collection.find())  # Convert MongoDB cursor to list
    
    # Get recommendations based on the description
    recommendations = get_recommendations(description, articles)
    
    # Return the recommendations as JSON
    return jsonify(recommendations), 200

def fetch_all_pages(url, query_params):
    all_results = []
    num_pages = int(query_params.get('page', 1))  # Default to 1 if not provided
    current_page = 1
    next_page = None
    
    while current_page <= num_pages:
        # Construct the URL for the current request
        if next_page:
            url = f"{url}&page={next_page}"
        else:
            url = f"{url}"
        
        print(url)  # For debugging purposes
        
        response = requests.get(url)
        if response.status_code == 429:
            print("Rate limit exceeded. Please try again later.")
            break
        
        response.raise_for_status()  # Raise an error for bad response status
        
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)
        
        # Get the nextPage value
        next_page = data.get('nextPage')
        
        # Break if there are no more pages
        if not next_page:
            break
        
        # Move to the next page
        current_page += 1
    
    return all_results

if __name__ == "__main__":
    app.run(debug=True)
