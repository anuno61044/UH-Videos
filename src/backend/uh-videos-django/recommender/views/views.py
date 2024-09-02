from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import MovieSerializer, RatingSerializer, UserSerializer
from ..models import Movie, Rating, User
from .recommender import get_recommendations  # función que debes crear

class MovieList(generics.ListCreateAPIView):
    """
    API view que permite listar y crear películas.
    
    Métodos HTTP permitidos:
    - GET: Lista todas las películas.
    - POST: Crea una nueva película.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserList(generics.ListCreateAPIView):
    """
    API view que permite listar y crear usuarios.
    
    Métodos HTTP permitidos:
    - GET: Lista todos los usuarios.
    - POST: Crea un nuevo usuario.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view que permite recuperar, actualizar o eliminar una película específica.
    
    Métodos HTTP permitidos:
    - GET: Recupera los detalles de una película.
    - PUT/PATCH: Actualiza una película existente.
    - DELETE: Elimina una película.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserRecommendations(APIView):
    """
    API view que proporciona recomendaciones de películas para un usuario específico.
    
    Métodos HTTP permitidos:
    - GET: Obtiene recomendaciones de películas para el usuario dado.
    
    Parámetros:
    - user_id (int): El ID del usuario para el cual se generarán las recomendaciones.
    
    Retorna:
    - Response: Un objeto Response con las recomendaciones y las trazas.
    """
    def get(self, request, user_id):
        recommendations, trace = get_recommendations(user_id)
        serialized_recommendations = MovieSerializer(recommendations, many=True).data
        return Response({
            "recommendations": serialized_recommendations,
            "trace": trace
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def rate_movie(request, movie_id):
    """
    API view que permite a un usuario calificar una película.
    
    Métodos HTTP permitidos:
    - POST: Califica una película.
    
    Parámetros:
    - movie_id (int): El ID de la película a calificar.
    - user_id (int): El ID del usuario que realiza la calificación.
    - score (int): La calificación asignada a la película.
    
    Retorna:
    - Response: Un objeto Response con la calificación actualizada o creada.
    """
    user_id = request.data.get('user_id')
    score = request.data.get('score')
    
    try:
        movie = Movie.objects.get(id=movie_id)
        user = User.objects.get(id=user_id)

        # Actualizar o crear la calificación
        rating, created = Rating.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={'score': score}
        )

        return Response({"success": True, "rating": rating.score})
    
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

class UserRatingsView(APIView):
    """
    API view que permite obtener todas las calificaciones de un usuario específico.
    
    Métodos HTTP permitidos:
    - GET: Recupera todas las calificaciones hechas por un usuario.
    
    Parámetros:
    - user_id (int): El ID del usuario cuyas calificaciones se desean obtener.
    
    Retorna:
    - Response: Un objeto Response con las películas calificadas y sus puntuaciones.
    """
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        ratings = Rating.objects.filter(user=user).select_related('movie')
        rated_movies = [
            {
                "movie_id": rating.movie.id,
                "score": rating.score
            }
            for rating in ratings
        ]

        return Response({
            "user": user.username,
            "rated_movies": rated_movies
        })

class UsersRatingsView(APIView):
    """
    API view que permite obtener las calificaciones de múltiples usuarios para todas las películas.
    
    Métodos HTTP permitidos:
    - GET: Recupera las calificaciones de películas para un conjunto de usuarios.
    
    Parámetros:
    - user_ids (list): Lista de IDs de los usuarios para los que se desean obtener las calificaciones.
    
    Retorna:
    - Response: Un objeto Response con las calificaciones de cada usuario para cada película.
    """
    def get(self, request):
        user_ids = request.query_params.getlist('user_ids')
        if not user_ids:
            return Response({"error": "No user IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(id__in=user_ids)

        if not users.exists():
            return Response({"error": "No valid users found"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todas las películas calificadas por al menos uno de los usuarios
        all_movies = Movie.objects.filter(rating__user__in=users).distinct()

        result = []
        for movie in all_movies:
            movie_ratings = {"movie_title": movie.title}
            for user in users:
                rating = Rating.objects.filter(user=user, movie=movie).first()
                movie_ratings[str(user.id)] = rating.score if rating else 0
            result.append(movie_ratings)

        return Response(result)

class MyTokenObtainPairView(TokenViewBase):
    """
    API view personalizada para obtener un par de tokens JWT (refresh y access) basado en el email del usuario.
    
    Métodos HTTP permitidos:
    - POST: Genera y retorna un par de tokens JWT si el email proporcionado es válido.
    
    Parámetros:
    - email (str): El email del usuario para el cual se generarán los tokens.
    
    Retorna:
    - Response: Un objeto Response con el token de refresh y el token de access.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API view que permite registrar un nuevo usuario.
    
    Métodos HTTP permitidos:
    - POST: Crea un nuevo usuario.
    
    Parámetros:
    - username (str): El nombre de usuario (opcional).
    - email (str): El email del usuario (obligatorio).
    
    Retorna:
    - Response: Un objeto Response indicando si el usuario fue creado exitosamente.
    """
    data = request.data
    try:
        user = User.objects.create(
            username=data.get('username', ''),  # Campo opcional
            email=data['email'],  # Campo obligatorio
        )
        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request):
    """
    API view que permite obtener la información del usuario autenticado basado en el token JWT.

    Métodos HTTP permitidos:
    - GET: Retorna la información del usuario autenticado.

    Retorna:
    - Response: Un objeto Response con los detalles del usuario autenticado (ID, username, email).
    """
    auth_header = request.headers.get('Authorization')
    # print("Authorization header:", auth_header)  # Verifica que el token está siendo enviado

    jwt_authenticator = JWTAuthentication()
    try:
        user, token = jwt_authenticator.authenticate(request)
        if user is None:
            raise Exception("User not found")

        # print(f"Authenticated user: {user.username}")
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return Response({"detail": "Authentication failed", "code": "user_not_found"}, status=401)
