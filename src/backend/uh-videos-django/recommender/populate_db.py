import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommendation.settings')
django.setup()

from recommender.models import Movie, User, Rating

def populate():
    # Crear usuarios de prueba
    user1 = User.objects.create(username='alice', email='alice@example.com', password='password123')
    user2 = User.objects.create(username='bob', email='bob@example.com', password='password123')
    user3 = User.objects.create(username='carol', email='carol@example.com', password='password123')

    # Crear películas de prueba
    movie1 = Movie.objects.create(title='The Matrix', genre='Action', director='Lana Wachowski', description='A computer hacker learns about the true nature of reality.', release_date='1999-03-31')
    movie2 = Movie.objects.create(title='Inception', genre='Sci-Fi', director='Christopher Nolan', description='A thief who steals corporate secrets uses dream-sharing technology.', release_date='2010-07-16')
    movie3 = Movie.objects.create(title='The Godfather', genre='Crime', director='Francis Ford Coppola', description='The aging patriarch of an organized crime dynasty transfers control to his son.', release_date='1972-03-24')

    # Crear calificaciones de prueba
    Rating.objects.create(user=user1, movie=movie1, score=5)
    Rating.objects.create(user=user1, movie=movie2, score=4)
    Rating.objects.create(user=user2, movie=movie1, score=4)
    Rating.objects.create(user=user2, movie=movie3, score=5)
    Rating.objects.create(user=user3, movie=movie2, score=5)
    Rating.objects.create(user=user3, movie=movie3, score=4)

    print("Base de datos poblada con datos de prueba.")

if __name__ == '__main__':
    populate()
