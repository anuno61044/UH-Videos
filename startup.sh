#!/bin/bash

# Activar el entorno virtual de Anaconda
echo "Activando entorno virtual de Anaconda..."
echo "Si usted prefiere usar otro entorno virtual modifique el archivo startup.sh"
source ~/anaconda3/bin/activate

# Instalar dependencias de Python en el backend
echo "Instalando dependencias de Python para el backend..."
pip install -r requirements.txt

# Navegar al directorio del backend y aplicar migraciones de Django
echo "Navegando al directorio del backend y aplicando migraciones..."
cd src/backend/uh-videos-django
python manage.py migrate

# Iniciar el servidor de desarrollo de Django
echo "Iniciando el servidor de desarrollo de Django..."
python manage.py runserver &

# Cambiar al directorio del frontend
echo "Cambiando al directorio del frontend..."
cd ../../frontend/uh-videos

# Instalar dependencias de Node.js
echo "Instalando dependencias de Node.js..."
npm install

# Iniciar el servidor de desarrollo de Vite
echo "Iniciando el servidor de desarrollo de Vite..."
npm run dev &

echo "El sistema de recomendación está en funcionamiento. Puedes acceder al frontend en http://localhost:3000"
