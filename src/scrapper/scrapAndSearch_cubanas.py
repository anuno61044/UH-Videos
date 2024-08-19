import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re


class Principal:

    def __init__(self):
        self.base_url = "https://visuales.uclv.cu//Peliculas/Cubanas/"

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
                    if re.search(r'(mpg|avi|mkv|mp4|3gp|rmvb)$', filename):
                        # self.video += url + filename + '\n'
                        file = open(f"./Cubanas.txt", "a")
                        file.write(url + '-foto-')
                        file.close()
                        print(f'🟢 Encontrado: {url + filename}')  
                        self.search_recursive_image(url)
                        continue
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')

        else:
            print("❌ URL incorrecta")             

    def search_recursive_image(self, url):

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

                if not href.endswith("/"):
                    filename = href.split("/")[-1]
                    if re.search(r'(jpg|png)$', filename):
                        # self.image += url + filename + '\n'
                        file = open(f"./Cubanas.txt", "a")
                        file.write(url + filename + '\n')
                        file.close()
                        print(f'🟢 Encontrada imagen: {url + filename}')  
                        return
                    else:
                        print(f'🗑️  Archivo no interesante: {url + filename}')
            
            file = open(f"./Cubanas.txt", "a")
            file.write('-\n')
            file.close()

        else:
            print("❌ URL incorrecta")  
        