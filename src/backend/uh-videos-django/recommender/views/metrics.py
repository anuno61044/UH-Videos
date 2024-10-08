import random
from ..models import Rating, Movie
from .content_based_filtering import content_based_filtering_train_set
from .collaborative_filtering import collaborative_filtering_train_set

def generate_recommendations_from_train_set(user_id, train_items, num_recommendations=10):
    """
    Genera recomendaciones basadas en un enfoque híbrido que combina filtrado basado en contenido y colaborativo
    usando únicamente el conjunto de entrenamiento.
    
    Args:
        user_id (int): ID del usuario.
        train_items (List[int]): Lista de IDs de películas en el conjunto de entrenamiento.
        num_recommendations (int): Número de recomendaciones a generar (default=10).
    
    Returns:
        List[int]: Lista de IDs de películas recomendadas.
        dict: Diccionario de trazas con detalles de cada método y la combinación final.
    """
    
    # 1. Obtener las recomendaciones basadas en contenido y su traza
    content_scores, content_trace = content_based_filtering_train_set(user_id, train_items)
    
    # 2. Obtener las recomendaciones basadas en filtrado colaborativo y su traza
    collaborative_scores, collaborative_trace = collaborative_filtering_train_set(user_id, train_items)
    
    print(content_scores)
    print(collaborative_scores)
    # 3. Combinar los puntajes de ambos métodos
    hybrid_scores = content_scores*0.5 + collaborative_scores*0.5  # Combina los puntajes (promedio)

    # 4. Obtener los IDs de las películas en el conjunto de entrenamiento para su ordenación
    all_movies = list(Movie.objects.all())
    movie_ids = [movie.id for movie in all_movies]
    
    # 5. Ordenar las películas por los puntajes híbridos y seleccionar las mejores recomendaciones
    recommended_movies = sorted(zip(movie_ids, hybrid_scores), key=lambda x: x[1], reverse=True)
    recommended_movie_ids = [movie_id for movie_id, _ in recommended_movies[:num_recommendations]]
    
    # 6. Trazas para fines de análisis
    trace = {
        "content_based_trace": content_trace,
        "collaborative_trace": collaborative_trace,
        "hybrid_scores": hybrid_scores,
        "recommended_movie_ids": recommended_movie_ids
    }
    
    return recommended_movie_ids


def get_train_test_split(user_id, test_ratio=0.2):
    """
    Divide las interacciones de un usuario en conjuntos de entrenamiento y prueba.
    
    Args:
        user_id (int): ID del usuario.
        test_ratio (float): Proporción de datos para el conjunto de prueba.
        
    Returns:
        Tuple[List[int], List[int]]: (Entrenamiento, Prueba)
    """
    ratings = Rating.objects.filter(user=user_id)
    ratings_only_id = ratings.values_list('id', flat=True)
    # Extrae las películas asociadas a esos ratings
    ratings_without_id = [rating.movie for rating in list(ratings)]

    ratings = [(ratings_only_id[i], ratings_without_id[i]) for i in range(len(ratings_without_id))]

    random.shuffle(ratings)
    split_index = int(len(ratings) * (1 - test_ratio))
    train_items =[elem[1] for elem in ratings[:split_index]]
    test_items = [elem[0] for elem in ratings[split_index:]]
    return train_items, test_items

def evaluate_recommendations(user_id):
    # Dividir las interacciones del usuario en conjuntos de entrenamiento y prueba
    train_items, test_items = get_train_test_split(user_id)
    
    # Generar recomendaciones usando solo el conjunto de entrenamiento
    recommended_items = generate_recommendations_from_train_set(user_id, train_items)
    
    # Calcular las métricas
    precision_value = precision(recommended_items, test_items)
    recall_value = recall(recommended_items, test_items)
    f1 = f1_score(precision_value, recall_value)

    # Imprimir o registrar las métricas
    print(f"User {user_id} - Precision: {precision_value:.2f}, Recall: {recall_value:.2f}, F1 Score: {f1:.2f}")
    # return precision_value, recall_value, f1

def precision(recommended_items, relevant_items):
    print(recommended_items)
    print(relevant_items)
    # Asegúrate de que recommended_items y relevant_items sean listas o conjuntos
    relevant_and_recommended = set(recommended_items) & set(relevant_items)
    return len(relevant_and_recommended) / len(recommended_items) if recommended_items else 0

def recall(recommended_items, relevant_items):
    relevant_and_recommended = set(recommended_items) & set(relevant_items)
    return len(relevant_and_recommended) / len(relevant_items) if relevant_items else 0

def f1_score(precision_value, recall_value):
    return 2 * (precision_value * recall_value) / (precision_value + recall_value) if (precision_value + recall_value) else 0

def main():
    """
    Función principal para probar el sistema de recomendaciones.
    Genera recomendaciones para un usuario específico, evalúa el rendimiento y muestra las métricas.
    """
    # ID del usuario para el cual se desea generar y evaluar recomendaciones
    user_id = 1  # Cambia este ID según el usuario que desees probar

    # Ejecutar la evaluación de recomendaciones y obtener las métricas
    precision_value, recall_value, f1_value = evaluate_recommendations(user_id)

    # Imprimir los resultados de la evaluación
    print("\n--- Resultados de la evaluación ---")
    print(f"Usuario ID: {user_id}")
    print(f"Precisión: {precision_value:.2f}")
    print(f"Recall: {recall_value:.2f}")
    print(f"F1 Score: {f1_value:.2f}")

if __name__ == "__main__":
    main()