import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

class Principal:
    """
    Clase Principal para realizar scraping de archivos de video desde un sitio web específico.

    Atributos:
    ----------
    s : str
        Almacena las URLs de los archivos de video encontrados.
    base_url : str
        La URL base desde la cual se inicia el proceso de scraping.

    Métodos:
    --------
    run():
        Ejecuta el proceso completo de scraping, desde la búsqueda hasta la escritura en un archivo.
    search_files():
        Inicia el proceso de scraping llamando al método recursivo que busca en la URL base.
    search_recursive(url):
        Realiza el scraping recursivo en una URL dada, buscando archivos de video y subdirectorios.
    """

    def __init__(self):
        """
        Inicializa la clase Principal con la URL base y una cadena vacía para almacenar los resultados.
        """
        self.s = ""  # Almacena las URLs de los archivos de video encontrados
        self.base_url = "https://visuales.uclv.cu/Peliculas/Extranjeras/"

    def run(self):
        """
        Ejecuta el proceso completo de scraping.
        Mide el tiempo que demora el proceso y escribe los resultados en un archivo de texto.
        """
        start = time.time()

        # Obtener el nombre del directorio final de la URL base para usarlo como nombre de archivo
        x = self.base_url.split("/")[-2]
        file = open(f"./{x}.txt", "w")
        
        print('🏃 Scrapping...')
        self.search_files()

        # Escribir los resultados en el archivo y cerrarlo
        file.write(self.s)
        file.close()

        print(f"⏰ Demoró {(time.time() - start)/60} minutos")

    def search_files(self):
        """
        Inicia el proceso de scraping desde la URL base.
        Llama al método recursivo para buscar archivos y subdirectorios.
        """
        print(f'Comienza el scrappeo en {self.base_url}...')
        self.search_recursive(self.base_url)

    def search_recursive(self, url):
        """
        Realiza el scraping recursivo en una URL dada.
        Busca archivos de video y subdirectorios, y maneja errores de conexión.

        Parámetros:
        -----------
        url : str
            La URL en la que se realizará la búsqueda de archivos y subdirectorios.
        """
        intime = True
        while intime:
            try:
                response = requests.get(url, timeout=15)
                intime = False
            except requests.exceptions.Timeout:
                print("❌ Fallo de conexión por tiempo de espera")
            except requests.exceptions.ConnectionError:
                print("💣 Fallo de conexión")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            falses = 5  # El primer enlace busca al padre, se ignoran los primeros 5 enlaces

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
                    if re.search(r'(mpg|avi|mkv|mp4|3gp)$', filename):
                        self.s += url + filename + '\n'
                        print(f'🟢 Encontrado: {url + filename}')  
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')
        else:
            print("❌ URL incorrecta") 
