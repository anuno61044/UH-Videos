from django.urls import path
from .views import MovieList, MovieDetail, UserList, UserRatingsView, UserRecommendations, rate_movie, UsersRatingsView

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('users/', UserList.as_view(), name='user-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('user/<int:user_id>/ratings/', UserRatingsView.as_view(), name='user-ratings'),
    path('users/ratings/', UsersRatingsView.as_view(), name='users-ratings'),
    path('users/<int:user_id>/recommendations/', UserRecommendations.as_view(), name='user-recommendations'),
    path('movies/<int:movie_id>/rate/', rate_movie, name='rate_movie'),
]
