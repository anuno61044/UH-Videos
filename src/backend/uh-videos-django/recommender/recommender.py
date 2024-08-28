from .content_based_filtering import content_based_filtering_with_collaborative
from .generate_explanation import generate_explanation
from .collaborative_filtering import collaborative_filtering
from .models import Movie, Rating

def get_recommendations(user_id):
    trace = {}
    
    # Obtener las películas que el usuario no ha visto
    unseen_movies = get_unseen_movies(user_id)
    unseen_movie_ids = [movie.id for movie in unseen_movies]
    
    # Filtrado Colaborativo con trazas, filtrando solo películas no vistas
    collaborative_scores, collaborative_trace = collaborative_filtering(user_id)
    trace['collaborative_filtering'] = collaborative_trace

    # Filtrado basado en contenido con augmentación de características y trazas, filtrando solo películas no vistas
    content_scores, content_trace = content_based_filtering_with_collaborative(user_id)
    trace['content_based_filtering'] = content_trace

    # Filtrar y ordenar películas no vistas por la puntuación final
    recommended_movies = [movie for movie in Movie.objects.all() if movie.id in unseen_movie_ids]
    recommended_movies = sorted(recommended_movies, key=lambda x: collaborative_scores[list(Movie.objects.all()).index(x)], reverse=True)
    recommended_movies = recommended_movies[:5]

    # Generar explicación en lenguaje natural
    explanations = []
    for recommended_movie in recommended_movies:
        movie_idx = list(Movie.objects.all()).index(recommended_movie)
        explanations.append(generate_explanation(trace, movie_idx, Movie.objects.all(), user_id))

    return recommended_movies, explanations

def get_unseen_movies(user_id):
    seen_movies = Rating.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    unseen_movies = Movie.objects.exclude(id__in=seen_movies)
    return unseen_movies
