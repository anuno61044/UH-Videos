from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Movie, Rating
from sklearn.metrics.pairwise import cosine_similarity
from .collaborative_filtering import collaborative_filtering
import numpy as np

def content_based_filtering_with_collaborative(user_id):
    movies = Movie.objects.all()
    collaborative_scores = collaborative_filtering(user_id)[0]
    
    tfidf = TfidfVectorizer(stop_words='english')
    movie_matrix = tfidf.fit_transform([f"{movie.genre} {movie.director}" for movie in movies])
    
    augmented_matrix = np.hstack([movie_matrix.toarray(), collaborative_scores.reshape(-1, 1)])  # Augmentación de características
    
    user_ratings = Rating.objects.filter(user_id=user_id)
    
    user_profile = np.zeros(augmented_matrix.shape[1])
    for rating in user_ratings:
        movie_idx = list(movies).index(rating.movie)
        user_profile += rating.score * augmented_matrix[movie_idx]
    
    user_profile = user_profile / user_ratings.count()
    
    content_scores = cosine_similarity(augmented_matrix, user_profile.reshape(1, -1)).flatten()
    
    trace = {
        "collaborative_scores": collaborative_scores,
        "content_based_features": augmented_matrix,
        "user_profile": user_profile,
        "content_scores": content_scores
    }
    
    return content_scores, trace
