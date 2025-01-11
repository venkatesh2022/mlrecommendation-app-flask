import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, similarity_matrix):
        self.similarity_matrix = similarity_matrix
        self.model = TruncatedSVD(n_components= 50, random_state=42)
    
    def train_model(self):
        self.user_factors = self.model.fit_transform(self.similarity_matrix)
        self.item_factors = self.model.components_
        
    def recommend(self, user_id, top_n = 10):
        scores = np.dot(self.user_factors[user_id], self.item_factors[user_id])
        top_recommendations = np.argsort(-scores)[:top_n]
        return top_recommendations
    
class HybridRecommender:
    def __init__(self, user_movie_matrix, movie_factors):
        self.user_movie_matrix = user_movie_matrix
        self.movie_factors = movie_factors
        self.similarity_matrix = cosine_similarity(self.user_movie_matrix)

    def recommend(self, user_id, top_n=10):
        user_sim_scores = self.similarity_matrix[user_id - 1]
        similar_users = np.argsort(-user_sim_scores)[1:6]
        collaborative_recommendations = []

        for sim_user in similar_users:
            user_ratings = self.user_movie_matrix.iloc[sim_user]
            top_rated = user_ratings[user_ratings > 4].index.tolist()
            collaborative_recommendations.extend(top_rated)

        collaborative_recommendations = list(set(collaborative_recommendations))[:top_n]
        content_scores = self.movie_factors[user_id - 1]
        content_recommendations = np.argsort(-content_scores)[:top_n]
        hybrid_recommendations = list(set(collaborative_recommendations + content_recommendations))[:top_n]
        return hybrid_recommendations