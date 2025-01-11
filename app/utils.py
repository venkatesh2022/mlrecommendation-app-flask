import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def load_data(data_path='data/'):
    """Load datasets from the given data path."""
    movies = pd.read_csv(f'{data_path}movies.csv')
    ratings = pd.read_csv(f'{data_path}ratings.csv')
    tags = pd.read_csv(f'{data_path}tags.csv')
    return movies, ratings, tags

def preprocess_data(movies, ratings):
    # Ensure the 'genres' column exists and fill missing values
    movies['genres'] = movies['genres'].fillna('')

    # If 'tags' is not used anymore, create metadata based on genres only
    movies['metadata'] = movies['genres']

    # Merge ratings with movies
    merged_data = pd.merge(ratings, movies, on='movieId', how='left')
    print("Columns after merging ratings with movies:", merged_data.columns)

    # Check if 'title' exists before pivot
    if 'title' not in merged_data.columns:
        raise ValueError("The column 'title' is missing in the merged data. Check the 'movies' dataset.")

    # Create the user-movie rating matrix
    user_movie_matrix = merged_data.pivot_table(
        index='userId', columns='title', values='rating', aggfunc='mean'
    ).fillna(0)

    return user_movie_matrix, movies

def train_nmf(metadata, n_components=20):
    """Train an NMF model for content-based recommendations."""
    # Generate TF-IDF features from metadata
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(metadata)

    # Train the NMF model
    nmf_model = NMF(n_components=n_components, random_state=42)
    movie_factors = nmf_model.fit_transform(tfidf_matrix)

    return movie_factors

def initialize_recommender():
    from app.recommender import HybridRecommender

    # Load data
    movies = pd.read_csv('data/movies.csv')
    ratings = pd.read_csv('data/ratings.csv')

    # Preprocess data
    user_movie_matrix, movies = preprocess_data(movies, ratings)

    # Train NMF model on metadata
    movie_factors = train_nmf(movies['metadata'])

    # Initialize the hybrid recommender
    recommender = HybridRecommender(user_movie_matrix, movie_factors)
    return recommender
