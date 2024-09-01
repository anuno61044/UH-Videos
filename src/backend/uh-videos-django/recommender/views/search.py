import random
import Levenshtein
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Movie
from ..serializers import MovieSerializer

def search_movies(request):
    query = request.GET.get('q', '')
    threshold = 5  # Número mínimo de recomendaciones que quieres obtener

    # Obtener todas las películas de la base de datos
    movies = list(Movie.objects.all())

    if not query:
        random_movies = random.sample(movies, min(len(movies), threshold))
        explanations = ["Esta película fue recomendada aleatoriamente" for _ in range(threshold)]
        return JsonResponse({'movies': [MovieSerializer(movie).data for movie in random_movies], 'explanations': explanations})

    # Crear una lista con los títulos de todas las películas
    titles = [movie.title for movie in movies]

    # Crear el vectorizador TF-IDF
    vectorizer = TfidfVectorizer().fit(titles)

    # Vectorizar los títulos y la consulta
    vectors = vectorizer.transform(titles)
    query_vec = vectorizer.transform([query])

    # Calcular la similitud coseno entre la consulta y los títulos
    cos_similarities = cosine_similarity(query_vec, vectors).flatten()

    # Obtener los índices de las películas ordenadas por similitud coseno
    sorted_indices = cos_similarities.argsort()[::-1]

    # Filtrar las películas que tienen una similitud significativa
    top_movies = [(movies[int(i)], cos_similarities[int(i)]) for i in sorted_indices if cos_similarities[int(i)] > 0]

    # Si no hay suficientes resultados, aplicar Levenshtein
    if len(top_movies) < threshold:
        lev_distances = [(movie, Levenshtein.distance(query, movie.title)) for movie in movies]
        lev_distances.sort(key=lambda x: x[1])  # Ordenar por la distancia Levenshtein (menor es mejor)

        titles = [movie[0].title for movie in top_movies]
        # Agregar las mejores coincidencias de Levenshtein hasta completar el threshold
        for movie, distance in lev_distances:
            if movie.title not in titles:
                top_movies.append((movie, distance))
            if len(top_movies) == threshold:
                break

    # Retornar los resultados al template
    return JsonResponse({
        'movies': [MovieSerializer(movie).data for movie, score in top_movies[:threshold]],
        'query': query
    })
