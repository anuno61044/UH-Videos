from ..models import Rating, User

def generate_explanation(trace, recommended_movie_idx, movies, user_id, collaborative_scores, content_scores):
    """
    Genera una explicación en lenguaje natural sobre por qué se recomendó una película,
    destacando el enfoque predominante (colaborativo o basado en contenido) o una combinación de ambos.

    Parámetros:
    - trace (dict): Un diccionario que contiene las trazas de ambos enfoques (colaborativo y basado en contenido).
    - recommended_movie_idx (int): El índice de la película recomendada.
    - movies (QuerySet): El conjunto de películas disponibles.
    - user_id (int): El ID del usuario para el cual se genera la explicación.
    - collaborative_scores (np.ndarray): Las calificaciones basadas en filtrado colaborativo.
    - content_scores (np.ndarray): Las calificaciones basadas en contenido.

    Retorna:
    - str: Una explicación en lenguaje natural sobre por qué se recomendó la película.
    """
    # Determinar qué enfoque tuvo más peso
    collaborative_score = collaborative_scores[recommended_movie_idx]
    content_score = content_scores[recommended_movie_idx]

    if collaborative_score > content_score * 1.5:  # Si el enfoque colaborativo tiene significativamente más peso
        similar_users = collaborative_explanation(trace, user_id, recommended_movie_idx)
        if similar_users > 0:
            return f"Te recomendamos esta película porque {similar_users} usuario(s) que vieron películas similares a las tuyas la calificaron bien."
        return "Te recomendamos esta película basada en las preferencias de usuarios similares a ti."
    elif content_score > collaborative_score * 1.5:  # Si el enfoque basado en contenido tiene significativamente más peso
        similar_movies, characteristics = content_based_explanation(trace, recommended_movie_idx, movies, user_id)
        if similar_movies and characteristics:
            return f"Esta película es similar a otras que te han gustado como {', '.join(similar_movies)} en cuanto al {', '.join(characteristics)}."
        return "Esta película se basa en tus preferencias pasadas."
    else:  # Si ambos enfoques tienen peso similar, usar una explicación combinada
        similar_users = collaborative_explanation(trace, user_id, recommended_movie_idx)
        similar_movies, characteristics = content_based_explanation(trace, recommended_movie_idx, movies, user_id)
        if similar_users > 0 and similar_movies and characteristics:
            return f"Te recomendamos esta película porque es similar a otras que has visto como {', '.join(similar_movies)} en cuanto a {', '.join(characteristics)}. Además {similar_users} usuario(s) que vieron películas similares a las tuyas la calificaron bien."
        elif similar_movies and characteristics:
            return f"Te recomendamos esta película porque es similar a otras que has visto como {', '.join(similar_movies)} en cuanto a {', '.join(characteristics)}. Además algunos usuarios que vieron películas similares a las tuyas la calificaron bien."
        elif similar_users > 0:
            return f"Te recomendamos esta película {similar_users} usuario(s) que vieron películas similares a las tuyas la calificaron bien. Y basado en tus preferencias pasadas."
        else:
            return f"Te recomendamos esta película porque es similar a otras que has visto. Además algunos usuarios que vieron películas similares a las tuyas la calificaron bien."
        
        

def collaborative_explanation(trace, user_id, recommended_movie_idx):
    """
    Genera una explicación basada en la similitud de usuarios, utilizando los IDs reales de los usuarios
    y organizándolos según su similitud.

    Parámetros:
    - trace (dict): Un diccionario que contiene las puntuaciones de similitud del usuario y las calificaciones ponderadas.
    - user_id (int): El ID del usuario para el cual se genera la explicación.
    - recommended_movie_idx (int): El índice de la película recomendada.

    Retorna:
    - int: El número de usuarios similares que calificaron positivamente la película recomendada.
    """
    # Obtener los IDs de los usuarios y sus correspondientes similitudes
    user_similarity_scores = trace['collaborative_filtering']['user_similarity_scores']
    users = User.objects.all()

    # Crear una lista de tuplas (user_id, similarity) excluyendo al usuario actual
    similar_users = [user for user, score in enumerate(user_similarity_scores) if score > 0.5]

    user_count = 0
    for user in similar_users:
        if trace['collaborative_filtering']["rating_matrix"][user][recommended_movie_idx] > 2:
            user_count += 1

    # Generar la explicación en lenguaje natural
    return user_count

def content_based_explanation(trace, recommended_movie_idx, movies, user_id):
    """
    Genera una explicación basada en el filtrado basado en contenido, identificando las características de las películas
    que son similares a las que el usuario ya ha calificado positivamente.

    Parámetros:
    - trace (dict): Un diccionario que contiene las características y calificaciones basadas en contenido.
    - recommended_movie_idx (int): El índice de la película recomendada.
    - movies (QuerySet): El conjunto de películas disponibles.
    - user_id (int): El ID del usuario para el cual se genera la explicación.

    Retorna:
    - tuple: Un par que contiene una lista de títulos de películas similares y un conjunto de características comunes.
    """
    seen_movies = Rating.objects.filter(user_id=user_id).values_list('movie__title', flat=True)
    similar_movies = []
    characteristics = set()  # Usar un conjunto para evitar duplicados
    for idx, score in enumerate(trace['content_based_filtering']['content_scores']):
        if idx != recommended_movie_idx and score > 0.5 and movies[idx].title in seen_movies:
            # similar_movies.append(movies[idx].title)
            pos = []
            for i,caract in enumerate(trace['content_based_filtering']['content_based_features'][idx]):
                if caract*trace['content_based_filtering']['content_based_features'][recommended_movie_idx][i] > 0:
                    pos.append(i)
            if len(pos) > 0:
                similar_movies.append(movies[idx].title)
                for i in pos: 
                    characteristics.add(trace['content_based_filtering']['names'][i])

    return similar_movies, characteristics
