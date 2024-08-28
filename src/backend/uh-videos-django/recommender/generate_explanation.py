from .models import Rating

def generate_explanation(trace, recommended_movie_idx, movies, user_id):
    explanations = []

    # Explicación del Filtrado Colaborativo
    explanations.append(collaborative_explanation(trace, user_id))

    # Explicación del Filtrado Basado en Contenido
    explanations.append(content_based_explanation(trace, recommended_movie_idx, movies, user_id))

    # Explicación Combinada
    explanations.append(combined_explanation(trace, user_id))
    
    return " ".join(explanations)




def collaborative_explanation(trace, user_id):
    similar_users = [i + 1 for i, score in enumerate(trace['collaborative_filtering']['user_similarity_scores']) if score > 0.8 and (i + 1) != user_id]
    similar_users = sorted(similar_users, reverse=True)
    if similar_users:
        return f"Te recomendamos esta película porque los usuarios con ids:{similar_users} vieron películas similares a las tuyas y las calificaron bien."
    return "Te recomendamos esta película basada en las preferencias de usuarios similares a ti."

def content_based_explanation(trace, recommended_movie_idx, movies, user_id):
    seen_movies = Rating.objects.filter(user_id=user_id).values_list('movie__title', flat=True)
    similar_movies = []
    characteristics = set()  # Usar un conjunto para evitar duplicados
    for idx, score in enumerate(trace['content_based_filtering']['content_scores']):
        if idx != recommended_movie_idx and score > 0.5 and movies[idx].title not in seen_movies:
            similar_movies.append(movies[idx].title)
            if 'genre' in trace['content_based_filtering']['content_based_features'][idx]:
                characteristics.add('género')
            if 'director' in trace['content_based_filtering']['content_based_features'][idx]:
                characteristics.add('director')

    if similar_movies and characteristics:
        return f"Esta película es similar a otras que te han gustado como {similar_movies} en cuanto al {', '.join(characteristics)}."
    return "Esta película se basa en tus preferencias de género y director."

def combined_explanation(trace, user_id):
    similar_users = [i + 1 for i, score in enumerate(trace['collaborative_filtering']['user_similarity_scores']) if score > 0.3 and (i + 1) != user_id]
    if similar_users:
        return f"Esta recomendación se basa en tus calificaciones anteriores y en la similitud con los gustos de otros usuarios similares como {similar_users}."
    return "Esta recomendación se basa en tus calificaciones anteriores."
