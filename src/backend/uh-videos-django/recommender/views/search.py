import random
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from ..models import Movie
from ..serializers import MovieSerializer

def search_movies(request):
    query = request.GET.get('q', '')
    threshold = 5  # Número mínimo de recomendaciones que quieres obtener


    # Obtener todas las películas de la base de datos
    movies = Movie.objects.all()

    if not query:
        random_movies = [random.choice(movies) for _ in range(threshold)]
        explanations = ["Esta película fue recomendada aleatoriamente" for _ in range(threshold)]
        return JsonResponse({'movies': [MovieSerializer(movie).data for movie in random_movies], 'explanations': explanations})

    # Crear una lista con los títulos de todas las películas
    titles = [movie.title for movie in movies]

    # Crear el vectorizador TF-IDF
    vectorizer = TfidfVectorizer().fit(titles)

    # Vectorizar los títulos y la consulta
    vectors = vectorizer.transform(titles)  # Esto sigue siendo una csr_matrix
    query_vec = vectorizer.transform([query]).toarray()  # Vectorizar la consulta

    # Calcular la similitud coseno entre la consulta y los títulos
    cos_similarities = cosine_similarity(query_vec, vectors).flatten()

    # Obtener los índices de las películas ordenadas por similitud coseno
    sorted_indices = cos_similarities.argsort()[::-1]

    # Filtrar las películas que tienen una similitud significativa
    top_movies = [(movies[int(i)], cos_similarities[int(i)]) for i in sorted_indices if cos_similarities[int(i)] > 0]

    # Retornar los resultados al template
    return JsonResponse({
        'movies': [MovieSerializer(movie).data for movie, score in top_movies[:threshold]],
        'query': query
    })
    
