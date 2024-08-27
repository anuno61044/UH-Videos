from .models import User, Movie, Rating
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def collaborative_filtering(user_id):
    ratings = Rating.objects.all()
    users = User.objects.all()
    movies = Movie.objects.all()
    
    user_movie_matrix = np.zeros((users.count(), movies.count()))
    
    for rating in ratings:
        user_idx = list(users).index(rating.user)
        movie_idx = list(movies).index(rating.movie)
        user_movie_matrix[user_idx][movie_idx] = rating.score

    user_similarity = cosine_similarity(user_movie_matrix)
    
    user_idx = list(users).index(User.objects.get(id=user_id))
    
    weighted_ratings = user_similarity[user_idx].dot(user_movie_matrix) / np.array([np.abs(user_similarity[user_idx]).sum()])
    
    trace = {
        "user_similarity_scores": user_similarity[user_idx],
        "weighted_ratings": weighted_ratings
    }
    
    return weighted_ratings, trace
