def generate_explanation(trace):
    explanation = []
    explanation.append("Las recomendaciones se basan en la siguiente combinación de características de contenido y predicciones colaborativas:")
    
    for movie_idx, score in enumerate(trace['content_scores']):
        if score > 0:
            explanation.append(f"La película con índice {movie_idx} tiene un puntaje de {score:.2f} basado en las características enriquecidas.")
    
    return "\n".join(explanation)
