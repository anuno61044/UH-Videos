import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

class Principal:
    """
    Clase principal para realizar el scraping de películas extranjeras.

    Esta clase encapsula la lógica necesaria para buscar y obtener información 
    sobre películas extranjeras desde el sitio web especificado.

    Attributes:
        year (int): El año actual para el cual se está buscando películas.
        base_url (str): La URL base para acceder a las páginas de películas.

    Methods:
        run(): Inicia el proceso de scraping.
        search_files(): Realiza la búsqueda recursiva de archivos en las páginas.
        search_recursive(url): Recursivamente busca enlaces en la página dada.
        get_info(url): Obtiene y guarda la información de una película específica.
    """

    def __init__(self):
        """
        Inicializa la clase Principal con el año de búsqueda y la URL base.

        Inicializa el año para el cual se realizará la búsqueda de películas y 
        construye la URL base utilizando el año.
        """
        self.year = 2020
        self.base_url = f'https://visuales.uclv.cu/Peliculas/Extranjeras/{self.year}/'

    def run(self):
        """
        Inicia el proceso de scraping.

        Este método mide el tiempo de ejecución y coordina el proceso de scraping
        llamando al método `search_files` para comenzar la búsqueda.
        """
        start = time.time()

        x = self.base_url.split("/")[-2]
        
        print('🏃 Scrapping...')
        self.search_files()

        print(f"⏰ Demoró {(time.time() - start)/60} minutos")

    def search_files(self):
        """
        Inicia la búsqueda de archivos en la URL base.

        Este método imprime un mensaje de inicio y llama al método `search_recursive`
        para realizar la búsqueda recursiva de archivos en la URL base.
        """
        print(f'Comienza el scrappeo en {self.base_url}...')
        self.search_recursive(self.base_url)

    def search_recursive(self, url):
        """
        Realiza una búsqueda recursiva de enlaces en una URL dada.

        Este método maneja los errores de conexión e intenta acceder a la página 
        especificada. Si se encuentra un subdirectorio, se sigue buscando 
        recursivamente; si se encuentra un archivo `.nfo`, se llama al método 
        `get_info` para obtener la información.

        Args:
            url (str): La URL en la que se realizará la búsqueda.
        """
        intime = True
        while intime:
            try:
                response = requests.get(url, timeout=15)
                intime = False
            except requests.exceptions.Timeout:
                print("❌ Fallo de conexión")
            except requests.exceptions.ConnectionError:
                print("💣 Fallo de conexión")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            falses = 5  # Ignora los primeros 5 enlaces, que usualmente no son relevantes

            for link in soup.find_all("a"):
                if falses:
                    falses -= 1
                    continue

                href = link.get("href")

                if href.endswith("/"):
                    subdirectory_url = urljoin(url, href)
                    print(f'🕵️  Buscando en {subdirectory_url}...')
                    self.search_recursive(subdirectory_url)
                else:
                    filename = href.split("/")[-1]
                    if re.search(r'(nfo)$', filename):
                        subdirectory_url = urljoin(url, href)
                        print(f'🕵️  Buscando en la página {subdirectory_url}...')
                        self.get_info(subdirectory_url)
                        return
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')

        else:
            print("❌ URL incorrecta")

    def get_info(self, url):
        """
        Obtiene y guarda la información de una película específica.

        Este método verifica si la información de la película ya existe en un 
        archivo local. Si no existe, realiza una solicitud a la página de la película,
        guarda el contenido HTML en un archivo `.txt` y lo guarda en la ubicación 
        especificada.

        Args:
            url (str): La URL de la página de la película.
        """
        name = url.split("/")[-2]
        
        # Verifica si el archivo ya existe
        if not os.path.exists(f'../backend/uh-videos-django/info_extranjeras/{self.year}/{name}.txt'):
            # Hacer una solicitud a la página web
            response = requests.get(url, timeout=15)

            # Obtener el contenido HTML
            html_content = response.text

            # Guardar el HTML en un archivo .txt
            with open(f'../backend/uh-videos-django/info_extranjeras/{self.year}/{name}.txt', 'w', encoding='utf-8') as file:
                file.write(html_content)

            print(f'El archivo ha sido guardado en {name}.txt')
        else:
            print(f'El archivo ya había sido guardado en {name}.txt')

def main():
    """
    Función principal que ejecuta el proceso de scraping.

    Esta función instancia la clase Principal y llama al método `run` 
    para iniciar el proceso de scraping.
    """
    search_extranjeras = Principal()
    search_extranjeras.run()

if __name__ == "__main__":
    main()
