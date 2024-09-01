from rest_framework import serializers
from .models import Movie, Rating, User

from rest_framework import serializers
from .models import Movie, Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']

class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(source='rating_set', many=True, read_only=True)  # Incluye las calificaciones

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'director','url', 'description', 'release_date', 'ratings']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
