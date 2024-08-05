import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re


class Principal:

    def __init__(self):
        self.s=""
        self.base_url = "https://visuales.uclv.cu/Peliculas/Extranjeras/"

    def run(self):

        start = time.time()

        x = self.base_url.split("/")[-2]
        file = open(f"./{x}.txt", "w")
        
        print('🏃 Scrapping...')
        self.search_files()

        file.write(self.s)
        file.close()

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

            falses = 5 #Pq el primer enlace busca al padre

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
                    if re.search(r'(mpg|avi|mkv|mp4|3gp)$', filename):
                        self.s += url + filename + '\n'
                        print(f'🟢 Encontrado: {url + filename}')  
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')

        else:
            print("❌ URL incorrecta")             
