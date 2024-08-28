import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uh_videos.settings')
django.setup()

from recommender.models import Movie, User, Rating

fake = Faker()

def populate(num_users=10, num_movies=20, num_ratings=40):
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

    # Crear películas de prueba
    print(f"Creando {num_movies} películas...")
    movies = []
    for _ in range(num_movies):
        movie = Movie.objects.create(
            title=fake.sentence(nb_words=3).replace('.', ''),
            genre=random.choice(['Action', 'Sci-Fi', 'Crime', 'Drama', 'Comedy', 'Horror']),
            director=fake.name(),
            description=fake.text(),
            release_date=fake.date_between(start_date='-50y', end_date='today')
        )
        movies.append(movie)
    print(f"{num_movies} películas creadas.")

    # Crear grupos de usuarios similares
    similar_groups = 3  # Número de grupos de usuarios similares
    group_size = num_users // similar_groups  # Tamaño de cada grupo

    print(f"Creando calificaciones similares para {similar_groups} grupos de usuarios...")
    for group in range(similar_groups):
        base_ratings = {}  # Calificaciones base para el grupo
        selected_movies = random.sample(movies, k=3)  # Seleccionamos 20 películas para el grupo

        # Crear calificaciones base para estas películas
        for movie in selected_movies:
            base_ratings[movie] = random.randint(3, 5)  # Calificaciones entre 3 y 5

        # Asignar calificaciones similares a cada usuario en el grupo
        for i in range(group_size):
            user = users[group * group_size + i]
            for movie, score in base_ratings.items():
                # Pequeña variación en las calificaciones dentro del grupo
                varied_score = score + random.choice([-1, 0, 1])
                varied_score = max(1, min(5, varied_score))  # Asegurarse de que esté entre 1 y 5
                Rating.objects.create(user=user, movie=movie, score=varied_score)

    # Crear calificaciones aleatorias adicionales
    remaining_ratings = num_ratings - (similar_groups * group_size * 3)
    print(f"Creando {remaining_ratings} calificaciones adicionales aleatorias...")
    for _ in range(remaining_ratings):
        user = random.choice(users)
        movie = random.choice(movies)
        score = random.randint(1, 5)
        Rating.objects.create(user=user, movie=movie, score=score)

    print(f"Base de datos poblada con {num_users} usuarios, {num_movies} películas, y {num_ratings} calificaciones.")

if __name__ == '__main__':
    populate()
