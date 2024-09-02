from django.urls import path
from .views.views import MovieList, MovieDetail, UserList, UserRatingsView, UserRecommendations, rate_movie, UsersRatingsView
from .views.views import MyTokenObtainPairView, register_user, get_user
from .views.search import search_movies

urlpatterns = [
    # Ruta para listar todas las películas o crear una nueva
    path('movies/', MovieList.as_view(), name='movie-list'),
    
    # Ruta para listar todos los usuarios o crear un nuevo usuario
    path('users/', UserList.as_view(), name='user-list'),
    
    # Ruta para obtener información del usuario autenticado a partir de un token JWT
    path('user/', get_user, name='get_user'),
    
    # Ruta para obtener, actualizar o eliminar los detalles de una película específica
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    
    # Ruta para obtener las calificaciones de un usuario específico
    path('user/<int:user_id>/ratings/', UserRatingsView.as_view(), name='user-ratings'),
    
    # Ruta para obtener las calificaciones de múltiples usuarios para todas las películas
    # Ejemplo de uso: localhost:8000/api/users/ratings/?user_ids=104&user_ids=105&user_ids=136&user_ids=163
    path('users/ratings/', UsersRatingsView.as_view(), name='users-ratings'),
    
    # Ruta para obtener recomendaciones de películas para un usuario específico
    path('users/<int:user_id>/recommendations/', UserRecommendations.as_view(), name='user-recommendations'),
    
    # Ruta para calificar una película específica por parte de un usuario
    path('movies/<int:movie_id>/rate/', rate_movie, name='rate_movie'),
    
    # Ruta para obtener un par de tokens JWT (refresh y access) mediante autenticación de usuario
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Ruta para registrar un nuevo usuario en el sistema
    path('register/', register_user, name='register_user'),
    
    # Ruta para buscar películas basadas en una consulta (título o descripción)
    path('search/', search_movies, name='search_movies'),
]
