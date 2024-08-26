from rest_framework import generics
from .models import Movie, Rating, User
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserRatings(generics.ListCreateAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Rating.objects.filter(user_id=user_id)



from rest_framework.views import APIView
from rest_framework.response import Response
from .recommender import get_recommendations  # función que debes crear

class UserRecommendations(APIView):
    def get(self, request, user_id):
        recommendations = get_recommendations(user_id)
        return Response(recommendations)
