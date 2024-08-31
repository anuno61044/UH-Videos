from django.urls import path
from .views import MovieList, MovieDetail, UserList, UserRatingsView, UserRecommendations, rate_movie, UsersRatingsView
from .views import MyTokenObtainPairView, register_user, get_user

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('users/', UserList.as_view(), name='user-list'),
    path('user/', get_user, name='get_user'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('user/<int:user_id>/ratings/', UserRatingsView.as_view(), name='user-ratings'),
    path('users/ratings/', UsersRatingsView.as_view(), name='users-ratings'),
    # Example: localhost:8000/api/users/ratings/?user_ids=104&user_ids=105&user_ids=136&user_ids=163
    path('users/<int:user_id>/recommendations/', UserRecommendations.as_view(), name='user-recommendations'),
    path('movies/<int:movie_id>/rate/', rate_movie, name='rate_movie'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', register_user, name='register_user'),
]
