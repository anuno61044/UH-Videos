import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uh_videos.settings')
django.setup()

from recommender.models import Movie, User, Rating

fake = Faker()

def populate(num_users=100, num_movies=200, num_ratings=2000):
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
            release_date=fake.date_between(start_date='-50y', end_date='today')  # Corrigiendo la generación de fechas
        )
        movies.append(movie)
    print(f"{num_movies} películas creadas.")

    # Crear calificaciones de prueba
    print(f"Creando {num_ratings} calificaciones...")
    for _ in range(num_ratings):
        user = random.choice(users)
        movie = random.choice(movies)
        score = random.randint(1, 5)
        Rating.objects.create(user=user, movie=movie, score=score)
    print(f"{num_ratings} calificaciones creadas.")

    print("Base de datos poblada con datos de prueba.")

if __name__ == '__main__':
    populate()
