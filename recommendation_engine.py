# recommendation_engine.py
from flask import jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def prepare_dataframe(articles):
    df = pd.DataFrame(articles)
    df['title'] = df['title'].fillna('')
    df['description'] = df['description'].fillna('')
    df['source_id'] = df['source_id'].fillna('')
    #we have combined title + description of each article and created a new columns called combine.
    #This will help us getting more information while related text analysis.
    df['combine'] = df['title'] + ' '+ df['description'] + ' ' + df['source_id']
    return df

def vectorize_text(df):
    tfInit = TfidfVectorizer(stop_words='english')
    #fit_transform is used when you have the initial dataset and you want to train the vectorizer on it.
    tfidf_matrix = tfInit.fit_transform(df['combine'])
    return tfidf_matrix, tfInit

#TF-IDF vectorizer (tfInit) needs to be fitted with the training data before it can transform new input data.
def fit_new_input(text, tfInit):
    # transform It is used when you have new data and you want to transform it into the same feature space as the training data.
    input_vector = tfInit.transform([text])
    return input_vector;

def get_recommendations(keyword, data):
    # Prepare the DataFrame from the raw articles data
    df = prepare_dataframe(data)
    
    # Convert raw data into TF-IDF matrix and fit the TF-IDF vectorizer with training data
    tfidf_matrix, tfidf_vectorizer = vectorize_text(df)
    
    # Transform the new input data (keyword) into the TF-IDF matrix format
    input_vector = fit_new_input(keyword, tfidf_vectorizer)
    
    # Find cosine similarity between the input vector and the TF-IDF matrix
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()
    
    # Sort the indices of the similarity scores in descending order
    similar_indices = cosine_sim.argsort()[::-1][1:]
    
    # Generate recommendations including MongoDB ID (converted to string)
    similar_articles = [{
        '_id': str(df.iloc[i]['_id']),  # Ensure '_id' is converted to string
        'title': df.iloc[i]['title'],
        'description': df.iloc[i]['description'],
        'link': df.iloc[i]['link'],
        'image_url': df.iloc[i]['image_url'],
        'similarity_score': cosine_sim[i]
    } for i in similar_indices]
    
    # Return the top 5 recommendations as JSON
    return similar_articles[:5]
