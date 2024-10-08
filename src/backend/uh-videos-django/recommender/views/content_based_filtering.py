from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Movie, Rating
import numpy as np

def content_based_filtering(user_id):
    """
    Realiza un filtrado basado en contenido para recomendar películas a un usuario específico.

    Este método utiliza características de las películas (género, director, año de lanzamiento) para calcular
    la similitud entre las películas y el perfil de preferencias del usuario.

    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.

    Retorna:
    - content_scores (np.ndarray): Un array con las calificaciones basadas en contenido para el usuario especificado.
    - trace (dict): Un diccionario que contiene las características de las películas, el perfil del usuario, y las calificaciones basadas en contenido.
    """
    movies = Movie.objects.all()

    
    
    # Crear una matriz TF-IDF con las características de las películas
    tfidf = TfidfVectorizer(stop_words='english')
    movie_matrix = tfidf.fit_transform([f"{movie.genre} {movie.director.replace(' ', '_')} {movie.release_date.year}" for movie in movies])
    names = tfidf.get_feature_names_out()
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


def content_based_filtering_train_set(user_id, train_items, num_recommendations=10):
    """
    Genera recomendaciones basadas en contenido utilizando únicamente el conjunto de entrenamiento.

    Args:
        user_id (int): ID del usuario.
        train_items (List[int]): Lista de IDs de películas en el conjunto de entrenamiento.
        num_recommendations (int): Número de recomendaciones a generar (default=10).

    Returns:
        List[int]: Lista de IDs de películas recomendadas.
        dict: Diccionario de trazas con detalles del perfil y puntuaciones basadas en contenido.
    """
    
    # Filtrar solo las películas en el conjunto de entrenamiento
    train_movies = []
    all_movies = Movie.objects.all()
    
    for movie in all_movies:
        if movie in train_items:
            train_movies.append(movie)
        
    # Crear una matriz TF-IDF usando las características de las películas en el conjunto de entrenamiento
    tfidf = TfidfVectorizer(stop_words='english')
    train_movie_matrix = tfidf.fit_transform([f"{movie.genre} {movie.director.replace(' ', '_')} {movie.release_date.year}" for movie in train_movies])
    names = tfidf.get_feature_names_out()
    train_movie_matrix = train_movie_matrix.toarray()

    # Crear un perfil del usuario basado en sus calificaciones en el conjunto de entrenamiento
    user_ratings = Rating.objects.filter(user_id=user_id, movie_id__in=train_items)
    user_profile = np.zeros(train_movie_matrix.shape[1])
    for rating in user_ratings:
        movie_idx = list(train_movies).index(rating.movie)
        user_profile += rating.score / 5 * train_movie_matrix[movie_idx]

    # Normalizar el perfil del usuario
    user_profile = user_profile / user_ratings.count()

    # Calcular la similitud con todas las películas usando el perfil del usuario basado en el conjunto de entrenamiento
    all_movie_matrix = tfidf.transform([f"{movie.genre} {movie.director.replace(' ', '_')} {movie.release_date.year}" for movie in all_movies])
    all_movie_matrix = all_movie_matrix.toarray()
    content_scores = cosine_similarity(all_movie_matrix, user_profile.reshape(1, -1)).flatten()

    # Excluir las películas del conjunto de entrenamiento y seleccionar las mejores recomendaciones
    recommendations = [(movie.id, score) for movie, score in zip(all_movies, content_scores) if movie.id not in train_items]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:num_recommendations]
    recommended_movie_ids = [movie_id for movie_id, _ in recommendations]

    # Trazas para fines de análisis
    trace = {
        "content_based_features_train": train_movie_matrix,
        "names": names,
        "user_profile": user_profile,
        "content_scores": content_scores,
        "recommendations": recommendations
    }

    return content_scores, trace
