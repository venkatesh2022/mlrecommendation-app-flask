import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

# Load data
movies = pd.read_csv('../data/movies.csv')  # Adjust path if necessary
ratings = pd.read_csv('../data/ratings.csv')

# Merge datasets
data = pd.merge(ratings, movies, on='movieId')

# Create user-item interaction matrix
user_movie_matrix = data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Apply Singular Value Decomposition (SVD) for dimensionality reduction
svd = TruncatedSVD(n_components=50, random_state=42)
reduced_matrix = svd.fit_transform(user_movie_matrix)

# Compute cosine similarity between users
similarity_matrix = cosine_similarity(reduced_matrix)

# Save the matrix to a file
np.save('../model/similarity_matrix.npy', similarity_matrix)  # Save in 'model' folder

print("Similarity matrix saved successfully!")
