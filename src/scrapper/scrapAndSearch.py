import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re


class Principal:

    def __init__(self):
        self.year = 2021
        self.base_url = f'https://visuales.uclv.cu/Peliculas/Extranjeras/{self.year}/'

    def run(self):

        start = time.time()

        x = self.base_url.split("/")[-2]
        
        print('🏃 Scrapping...')
        self.search_files()

        print(f"⏰ Demoró {(time.time() - start)/60} minutos")

    def search_files(self):

        print(f'Comienza el scrappeo en {self.base_url}...')
        self.search_recursive(self.base_url)

    def search_recursive(self, url):

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

            falses = 5 # Pq el primer enlace busca al padre

            for link in soup.find_all("a"):

                if falses:
                    falses-=1
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
                        print(f'🕵️  Buscando en la pagina {subdirectory_url}...')
                        self.get_info(subdirectory_url)
                        return
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')

        else:
            print("❌ URL incorrecta")             

    def get_info(self, url):
        name = url.split("/")[-2]
        
        if not os.path.exists(f'../backend/uh-videos-django/info_extranjeras/{self.year}/{name}.txt'):
            # Hacer una solicitud a la página web
            response = requests.get(url, timeout=15)

            # Obtener el contenido HTML
            html_content = response.text

            # Guardar el HTML en un archivo .txt
            with open(f'../backend/uh-videos-django/info_extranjeras/{self.year}/{name}.txt', 'w', encoding='utf-8') as file:
                file.write(html_content)
                
            # # Guardar el HTML en un archivo .txt
            # with open(f'./info_extranjeras/2022/{name}.txt', 'w', encoding='utf-8') as file:
            #     file.write(html_content)

            print(f'El archivo ha sido guardado en {name}.txt')
        else:
            print(f'El archivo ya había sido guardado en {name}.txt')
            
        
def main():
    search_extranjeras = Principal()
    search_extranjeras.run()


if __name__ == "__main__":
    main()