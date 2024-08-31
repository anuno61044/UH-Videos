from .models import User, Movie, Rating
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def collaborative_filtering(user_id):
    """
    Realiza un filtrado colaborativo basado en la similitud de usuarios para recomendar películas a un usuario específico.

    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.

    Retorna:
    - weighted_ratings (np.ndarray): Un array con las calificaciones ponderadas de películas para el usuario especificado.
    - trace (dict): Un diccionario que contiene las puntuaciones de similitud del usuario y las calificaciones ponderadas.
    """
    # Obtener todas las calificaciones, usuarios y películas desde la base de datos
    ratings = Rating.objects.all()
    users = User.objects.all()
    movies = Movie.objects.all()

    # Crear una matriz de usuarios contra películas, inicialmente llena de ceros
    user_movie_matrix = np.zeros((users.count(), movies.count()))

    # Poblar la matriz con las calificaciones existentes
    for rating in ratings:
        user_idx = list(users).index(rating.user)  # Encontrar el índice del usuario
        movie_idx = list(movies).index(rating.movie)  # Encontrar el índice de la película
        user_movie_matrix[user_idx][movie_idx] = rating.score  # Asignar la calificación a la matriz

    # Calcular la similitud entre usuarios utilizando la similitud coseno
    user_similarity = cosine_similarity(user_movie_matrix)

    # Encontrar el índice del usuario para el cual se generarán las recomendaciones
    user_idx = list(users).index(User.objects.get(id=user_id))

    # Calcular las calificaciones ponderadas utilizando la similitud de usuarios
    weighted_ratings = user_similarity[user_idx].dot(user_movie_matrix) / np.array([np.abs(user_similarity[user_idx]).sum()])

    # Guardar las trazas para seguimiento y explicabilidad
    trace = {
        "user_similarity_scores": user_similarity[user_idx],  # Similitud del usuario con otros usuarios
        "weighted_ratings": weighted_ratings  # Calificaciones ponderadas para cada película
    }

    return weighted_ratings, trace