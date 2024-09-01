import os
import django
import random
import xml.etree.ElementTree as ET
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uh_videos.settings')
django.setup()

fake = Faker()

from recommender.models import Movie, User, Rating

# Constantes
GENRES = ['Action', 'Sci-Fi', 'Crime', 'Drama', 'Comedy', 'Horror']
NUM_DIRECTORS = 6
GROUP_SIZE_RATIO = 0.3  # Proporción de usuarios en cada grupo similar
CONTENT_BIAS_PROBABILITY = 0.7  # Probabilidad de que una calificación esté sesgada por el contenido
HIGH_SCORE_RANGE = (4, 5)  # Rango de puntuaciones altas
LOW_SCORE_RANGE = (1, 3)  # Rango de puntuaciones bajas
RATING_VARIATION = [-1, 0, 1]  # Variación de calificación en grupos similares

def populate(num_users=30, num_movies=20, num_ratings=150):
    """
    Pobla la base de datos con usuarios, películas y calificaciones para ejemplificar
    los casos cubiertos por el filtrado colaborativo y basado en contenido.

    Parámetros:
    - num_users (int): Número de usuarios a crear.
    - num_movies (int): Número de películas a crear.
    - num_ratings (int): Número total de calificaciones a crear.

    Este script realiza los siguientes pasos:
    1. Borra los datos existentes en las tablas `Rating`, `Movie` y `User`.
    2. Crea usuarios con nombres y correos electrónicos generados aleatoriamente.
    3. Crea películas con diversos géneros y directores.
    4. Genera calificaciones similares para grupos de usuarios específicos (para probar el filtrado colaborativo).
    5. Genera calificaciones adicionales con sesgos hacia ciertos géneros o directores (para probar el filtrado basado en contenido).
    """
    # Borrar la información anterior
    print("Borrando datos anteriores...")
    Rating.objects.all().delete()
    Movie.objects.all().delete()
    User.objects.all().delete()
    print("Datos anteriores borrados.")

    # Crear usuarios de prueba
    print(f"Creando {num_users} usuarios...")
    users = []
    for _ in range(num_users):
        user = User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'  # Puedes usar una función hash aquí si es necesario
        )
        users.append(user)
    print(f"{num_users} usuarios creados.")

    movies = []
    # Cargar información de las películas
    years = ['2024', '2023', '2022']
    for year in years:
        for archivo in os.listdir(f'./info_extranjeras/{year}'):
            if archivo.endswith('.txt'):
                print(archivo)
                # Leer el archivo XML
                tree = ET.parse(f'./info_extranjeras/{year}/{archivo}')
                root = tree.getroot()
                
                movie_title = root.find('originaltitle').text
                # movie_year = root.find('year').text
                movie_director = root.find('director').text
                # movie_language = root.find('fileinfo').find('streamdetails').find('audio').find('language').text
                # movie_countries = [country.text for country in root.findall('country')]
                movie_genres = [genre.text for genre in root.findall('genre')]
                # movie_actors = [actor.find('name').text for actor in root.findall('actor')[:3]]
                movie_description = root.find('plot').text
                if movie_description is None:
                    movie_description = 'No description'
                
                movie = Movie.objects.create(
                    title=movie_title,
                    genre=movie_genres[0],
                    director=movie_director,
                    url=f'https://visuales.uclv.cu/Peliculas/Extranjeras/{year}/{archivo[:-4]}/',
                    description=movie_description,
                    release_date=root.find('releasedate').text
                )
                movies.append(movie)
    
    num_movies = len(movies)
    print(f"{num_movies} películas creadas.")

    # Crear grupos de usuarios similares (Filtrado Colaborativo)
    similar_groups = int(num_users * GROUP_SIZE_RATIO)  # Número de grupos de usuarios similares
    group_size = max(1, num_users // similar_groups)  # Tamaño de cada grupo

    print(f"Creando calificaciones similares para {similar_groups} grupos de usuarios...")
    for group in range(similar_groups):
        base_ratings = {}  # Calificaciones base para el grupo
        selected_movies = random.sample(movies, k=3)  # Seleccionamos 3 películas para el grupo

        # Crear calificaciones base para estas películas
        for movie in selected_movies:
            base_ratings[movie] = random.randint(*HIGH_SCORE_RANGE)  # Calificaciones entre 4 y 5

        # Asignar calificaciones similares a cada usuario en el grupo
        for i in range(group_size):
            user = users[group * group_size + i]
            for movie, score in base_ratings.items():
                # Pequeña variación en las calificaciones dentro del grupo
                varied_score = score + random.choice(RATING_VARIATION)
                varied_score = max(1, min(5, varied_score))  # Asegurarse de que esté entre 1 y 5
                Rating.objects.create(user=user, movie=movie, score=varied_score)

    # Crear calificaciones adicionales sesgadas hacia contenido (Filtrado Basado en Contenido)
    remaining_ratings = num_ratings - (similar_groups * group_size * 3)
    print(f"Creando {remaining_ratings} calificaciones adicionales sesgadas hacia el contenido...")
    for _ in range(remaining_ratings):
        user = random.choice(users)
        movie = random.choice(movies)
        # Sesgo en calificaciones basado en géneros o directores
        if random.random() < CONTENT_BIAS_PROBABILITY:
            if user.username.endswith(('a', 'e', 'i', 'o', 'u')):  # Sesgo basado en el nombre del usuario
                score = random.randint(*LOW_SCORE_RANGE)
            else:
                score = random.randint(*HIGH_SCORE_RANGE)
        else:
            score = random.randint(1, 5)
        Rating.objects.create(user=user, movie=movie, score=score)

    print(f"Base de datos poblada con {num_users} usuarios, {num_movies} películas, y {num_ratings} calificaciones.")

if __name__ == '__main__':
    populate()