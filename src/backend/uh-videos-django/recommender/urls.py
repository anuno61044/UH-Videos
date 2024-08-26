from django.urls import path
from .views import MovieList, MovieDetail, UserRatings, UserRecommendations

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('users/<int:user_id>/ratings/', UserRatings.as_view(), name='user-ratings'),
    path('users/<int:user_id>/recommendations/', UserRecommendations.as_view(), name='user-recommendations'),
]
