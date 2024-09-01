from .models import User, Movie, Rating
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def collaborative_filtering(user_id):
    """
    Realiza un filtrado colaborativo basado en la similitud de usuarios para recomendar películas a un usuario específico.

    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.

    Retorna:
    - normalized_ratings (np.ndarray): Un array con las calificaciones ponderadas normalizadas de películas para el usuario especificado.
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
    
    # Encontrar el índice del usuario para el cual se generarán las recomendaciones
    user_idx = list(users).index(User.objects.get(id=user_id))

    # Inicializar un array para almacenar las similitudes entre el usuario objetivo y los demás
    user_similarity = np.zeros(users.count())

    # Calcular la similitud entre el usuario objetivo y los demás usuarios
    for i in range(users.count()):
        if i != user_idx:
            common_ratings = (user_movie_matrix[user_idx] > 0) 
            user_similarity[i] = cosine_similarity(
                [user_movie_matrix[user_idx][common_ratings]],
                [user_movie_matrix[i][common_ratings]]
            )[0, 0]

    # Calcular las calificaciones ponderadas utilizando la similitud de usuarios
    weighted_ratings = user_similarity.dot(user_movie_matrix) / np.array([np.abs(user_similarity).sum()])

    # Normalizar las calificaciones ponderadas para que estén entre 0 y 1
    min_rating = weighted_ratings.min()
    max_rating = weighted_ratings.max()
    normalized_ratings = (weighted_ratings - min_rating) / (max_rating - min_rating)

    # Guardar las trazas para seguimiento y explicabilidad
    trace = {
        "user_similarity_scores": user_similarity,  # Similitud del usuario con otros usuarios
        "weighted_ratings": normalized_ratings,  # Calificaciones ponderadas normalizadas
        "rating_matrix" : user_movie_matrix # Calificaciones de los usuarios a las peliculas
    }

    return normalized_ratings, trace
