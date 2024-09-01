from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie, Rating
import numpy as np

def content_based_filtering(user_id):
    """
    Realiza un filtrado basado en contenido para recomendar películas a un usuario específico.

    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.

    Retorna:
    - content_scores (np.ndarray): Un array con las calificaciones basadas en contenido para el usuario especificado.
    - trace (dict): Un diccionario que contiene las características y calificaciones basadas en contenido.
    """
    movies = Movie.objects.all()

    
    
    # Crear una matriz TF-IDF con las características de las películas
    tfidf = TfidfVectorizer(stop_words='english')
    movie_matrix = tfidf.fit_transform([f"{movie.genre} {movie.director.replace(' ', '_')} {movie.release_date.year}" for movie in movies])
    names = tfidf.get_feature_names_out()
    # print(names)
    movie_matrix = movie_matrix.toarray()

    # Crear un perfil del usuario basado en sus calificaciones
    user_ratings = Rating.objects.filter(user_id=user_id)
    user_profile = np.zeros(movie_matrix.shape[1])
    for rating in user_ratings:
        movie_idx = list(movies).index(rating.movie)
        user_profile += rating.score/5 * movie_matrix[movie_idx]

    user_profile = user_profile / user_ratings.count()

    # Calcular las calificaciones basadas en la similitud con el perfil del usuario
    content_scores = cosine_similarity(movie_matrix, user_profile.reshape(1, -1)).flatten()

    trace = {
        "content_based_features": movie_matrix,
        "names" : names,
        "user_profile": user_profile,
        "content_scores": content_scores
    }

    return content_scores, trace