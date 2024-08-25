import os
import requests
import xml.etree.ElementTree as ET


# URL a la que quieres hacer el POST
url = 'http://localhost:1337/api/'

genres = set()
years = set()
countries = set()
actors = set()
directors = set()
languages = set()

# Cargar información de las películas
for archivo in os.listdir('./info_extranjeras'):
    if archivo.endswith('.txt'):
        # Leer el archivo XML
        tree = ET.parse(f'./info_extranjeras/{archivo}')
        root = tree.getroot()

        years.add(root.find('year').text)
        directors.add(root.find('director').text)
        languages.add(root.find('fileinfo').find('streamdetails').find('audio').find('language').text)
        for country in root.findall('country'):
            countries.add(country.text)
        for genre in root.findall('genre'):
            genres.add(genre.text)
        for actor in root.findall('actor')[:3]:
            actors.add(actor.find('name').text)
            
# print('Géneros:\n', genres, '\n')
# print('Años:\n', years, '\n')
# print('Países:\n', countries, '\n')
# print('Actores:\n', actors, '\n')
# print('Directores:\n', directors, '\n')
# print('Idiomas:\n', languages, '\n')
            
# # Cargar los géneros en la base de datos
# for genre in genres:
#     # Datos que quieres enviar
#     item = {
#         'data': {
#             'name': genre
#         }
#     }
    
#     headers = {
#         'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
#     } # Token
    
#     response = requests.post(f'{url}genders', json=item, headers=headers) 
    
#     print(response.text) # Imprimir la respuesta


# Cargar los países en la base de datos
for country in countries:
    # Datos que quieres enviar
    item = {
        'data': {
            'name': country
        }
    }
    
    headers = {
        'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
    } # Token
    
    response = requests.post(f'{url}countries', json=item, headers=headers) 
    
    print(response.text) # Imprimir la respuesta

# # Cargar los años en la base de datos
# for year in years:
#     # Datos que quieres enviar
#     item = {
#         'data': {
#             'number': year
#         }
#     }
    
#     headers = {
#         'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
#     } # Token
    
#     response = requests.post(f'{url}years', json=item, headers=headers) 
    
#     print(response.text) # Imprimir la respuesta

# # Cargar los actores en la base de datos
# for actor in actors:
#     # Datos que quieres enviar
#     item = {
#         'data': {
#             'name': actor
#         }
#     }
    
#     headers = {
#         'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
#     } # Token
    
#     response = requests.post(f'{url}actors', json=item, headers=headers) 
    
#     print(response.text) # Imprimir la respuesta
    
# # Cargar los directores en la base de datos
# for director in directors:
#     # Datos que quieres enviar
#     item = {
#         'data': {
#             'name': director
#         }
#     }
    
#     headers = {
#         'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
#     } # Token
    
#     response = requests.post(f'{url}directors', json=item, headers=headers) 
    
#     print(response.text) # Imprimir la respuesta

# # Cargar los directores en la base de datos
# for language in languages:
#     # Datos que quieres enviar
#     item = {
#         'data': {
#             'name': language
#         }
#     }
    
#     headers = {
#         'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
#     } # Token
    
#     response = requests.post(f'{url}languages', json=item, headers=headers) 
    
#     print(response.text) # Imprimir la respuesta

headers = {
    'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
} # Token
    
# Obtener los id de los idiomas
response = requests.get(f'{url}languages', headers=headers)
data = response.json()
languages_dic = {item['attributes']['name']: item['id'] for item in data['data']}

# Obtener los id de los géneros
response = requests.get(f'{url}genders', headers=headers)
data = response.json()
genders_dic = {item['attributes']['name']: item['id'] for item in data['data']}

# Obtener los id de los países
response = requests.get(f'{url}countries', headers=headers)
data = response.json()
countries_dic = {item['attributes']['name']: item['id'] for item in data['data']}

# Obtener los id de los años
response = requests.get(f'{url}years', headers=headers)
data = response.json()
years_dic = {item['attributes']['number']: item['id'] for item in data['data']}

# Obtener los id de los actores
response = requests.get(f'{url}actors', headers=headers)
data = response.json()
actors_dic = {item['attributes']['name']: item['id'] for item in data['data']}

# Obtener los id de los directores
response = requests.get(f'{url}directors', headers=headers)
data = response.json()
directors_dic = {item['attributes']['name']: item['id'] for item in data['data']}


# Cargar información de las películas
for archivo in os.listdir('./info_extranjeras'):
    if archivo.endswith('.txt'):
        # Leer el archivo XML
        tree = ET.parse(f'./info_extranjeras/{archivo}')
        root = tree.getroot()

        movie_title = root.find('originaltitle').text
        movie_year = root.find('year').text
        movie_director = root.find('director').text
        movie_language = root.find('fileinfo').find('streamdetails').find('audio').find('language').text
        movie_countries = [country.text for country in root.findall('country')]
        movie_genres = [genre.text for genre in root.findall('genre')]
        movie_actors = [actor.find('name').text for actor in root.findall('actor')[:3]]
            
        obj = {
            "data": {
                "name": movie_title,
                "countries": {"id":countries_dic[country] for country in movie_countries},
                "languages": {"id":languages_dic[movie_language]},
                "genders": {"id":genders_dic[genre] for genre in movie_genres},
                "year": {"id": years_dic[int(movie_year)]}
            }
        }
        
        headers = {
            'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
        } # Token
        
        response = requests.post(f'{url}videos', json=obj, headers=headers) 
        
        print(response.text) # Imprimir la respuesta