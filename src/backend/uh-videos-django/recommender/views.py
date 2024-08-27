from rest_framework import generics
from .models import Movie, Rating, User
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .recommender import get_recommendations  # función que debes crear

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

class UserRecommendations(APIView):
    def get(self, request, user_id):
        recommendations, trace = get_recommendations(user_id)
        serialized_recommendations = MovieSerializer(recommendations, many=True).data
        return Response({
            "recommendations": serialized_recommendations,
            "trace": trace
        })

@api_view(['POST'])
def rate_movie(request, movie_id):
    user_id = request.data.get('user_id')
    score = request.data.get('score')
    
    movie = Movie.objects.get(id=movie_id)
    user = User.objects.get(id=user_id)

    # Actualizar o crear la calificación
    rating, created = Rating.objects.update_or_create(
        user=user,
        movie=movie,
        defaults={'score': score}
    )

    return Response({"success": True, "rating": rating.score})
