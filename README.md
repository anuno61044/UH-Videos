# 🎬 UH-VIDEOS

## Autores
- **Christopher Guerra Herrero**
- **Amanda Cordero Lezcano**
- **Alfredo Nuño Oquendo**

## Descripción del Problema
Este proyecto aborda el desarrollo de un sistema híbrido de recomendación de películas. El sistema combina técnicas de filtrado colaborativo y basado en contenido, integradas mediante un enfoque monolítico que permite proporcionar recomendaciones personalizadas a los usuarios. El objetivo es mejorar la experiencia de visualización, sugiriendo películas basadas en el historial de preferencias del usuario y características de las películas, tales como género y año de producción.

## Requerimientos

Para garantizar el correcto desempeño del proyecto ver requierements.txt.

## 🛠️ Uso y Ejecución del Proyecto

### Backend (Django)
1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias utilizando:
   ```bash
   pip install -r requirements.txt
   ```
3. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```
4. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

### Frontend (React con Vite)
1. Asegúrate de tener Node.js instalado.
2. Navega al directorio del frontend e instala las dependencias:
   ```bash
   npm install
   ```
3. Ejecuta el entorno de desarrollo:
   ```bash
   npm run dev
   ```

### Ejecución Completa
- Levanta primero el *backend* con Django y luego el *frontend* con Vite.
- Accede al sistema de recomendación a través de `http://localhost:3000` en tu navegador.

