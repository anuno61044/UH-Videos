from django.urls import path
from .views import MovieList, MovieDetail, UserRatings, UserRecommendations, rate_movie

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('users/<int:user_id>/ratings/', UserRatings.as_view(), name='user-ratings'),
    path('users/<int:user_id>/recommendations/', UserRecommendations.as_view(), name='user-recommendations'),
    path('movies/<int:movie_id>/rate/', rate_movie, name='rate_movie'),
]
