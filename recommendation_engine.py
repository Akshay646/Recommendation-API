# recommendation_engine.py

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
    #preparing data frame from articles
    df = prepare_dataframe(data)
    
    #convert raw data into TF-IDF matrix and fitting Tf-IDF vectorizer with training data. 
    tfidf_matrix, tfInit = vectorize_text(df);
    
    #now tfInit is fitted with the training data and is ready to transform the new data.
    input_vector = fit_new_input(keyword, tfInit);
    
    #finding cosine similarity between TF-IDF matrix of input data and TF-IDF matrix for whole response.
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()

    # Sorting it descendingly using argsort, which sorts the collection while maintaining the original index
    similar_indices = cosine_sim.argsort()[::-1][1:]
    similar_articles = [(df.iloc[i]['title'], cosine_sim[i]) for i in similar_indices]
    
    #returning only top 5 recommendations
    return similar_articles[:5]
