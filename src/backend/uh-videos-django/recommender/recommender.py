from .content_based_filtering import content_based_filtering_with_collaborative
from .generate_explanation import generate_explanation
from .models import User, Movie, Rating

def get_recommendations(user_id):
    trace = {}
    
    # Filtrado basado en contenido con augmentación de características
    content_scores = content_based_filtering_with_collaborative(user_id)
    trace['content_scores'] = content_scores

    # Ordenar películas por la puntuación final
    movies = Movie.objects.all()
    recommended_movies = sorted(list(movies), key=lambda x: content_scores[list(movies).index(x)], reverse=True)
    
    # Generar explicación
    trace['explanation'] = generate_explanation(trace)
    
    return recommended_movies, trace
