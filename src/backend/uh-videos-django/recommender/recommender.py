import random
from .content_based_filtering import content_based_filtering
from .generate_explanation import generate_explanation
from .collaborative_filtering import collaborative_filtering
from .models import Movie, Rating

def get_recommendations(user_id):
    """
    Genera recomendaciones de películas para un usuario específico utilizando una combinación de filtrado colaborativo
    y filtrado basado en contenido. Selecciona el paradigma predominante para generar explicaciones.

    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.

    Retorna:
    - recommended_movies (list): Una lista de las películas recomendadas.
    - explanations (list): Una lista de explicaciones en lenguaje natural sobre por qué se recomendaron las películas.
    """
    trace = {}

    # Obtener las películas que el usuario no ha visto
    unseen_movies, seen_movies = get_labeled_movies(user_id)

    if len(seen_movies) == 0:
        return [random.choice(unseen_movies) for _ in range(5)], ["Esta película fue recomendada aleatoriamente" for _ in range(5)]

    unseen_movie_ids = [movie.id for movie in unseen_movies]

    # Filtrado Colaborativo con trazas, filtrando solo películas no vistas
    collaborative_scores, collaborative_trace = collaborative_filtering(user_id)
    trace['collaborative_filtering'] = collaborative_trace

    # Filtrado basado en contenido con trazas, filtrando solo películas no vistas
    content_scores, content_trace = content_based_filtering(user_id)
    trace['content_based_filtering'] = content_trace

    # Combinación de ambos enfoques (Feature Combination)
    print(collaborative_scores)
    print(content_scores)
    final_scores = 0.5 * collaborative_scores + 0.5 * content_scores

    # Filtrar y ordenar películas no vistas por la puntuación final
    recommended_movies = [movie for movie in Movie.objects.all() if movie.id in unseen_movie_ids]
    recommended_movies = sorted(recommended_movies, key=lambda x: final_scores[list(Movie.objects.all()).index(x)], reverse=True)
    recommended_movies = recommended_movies[:5]  # Limitar a las 5 mejores recomendaciones

    # Generar explicación en lenguaje natural
    explanations = []
    for recommended_movie in recommended_movies:
        movie_idx = list(Movie.objects.all()).index(recommended_movie)
        explanations.append(generate_explanation(trace, movie_idx, Movie.objects.all(), user_id, collaborative_scores, content_scores))

    return recommended_movies, explanations

def get_labeled_movies(user_id):
    """
    Obtiene una lista de películas que un usuario específico no ha visto y otra con las que sí.

    Parámetros:
    - user_id (int): El ID del usuario.

    Retorna:
    - unseen_movies (QuerySet): Un QuerySet de películas que el usuario no ha visto.
    - seen_movies (QuerySet): Un QuerySet de películas que el usuario ya ha visto.
    """
    seen_movies = Rating.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    unseen_movies = Movie.objects.exclude(id__in=seen_movies)
    return unseen_movies, seen_movies