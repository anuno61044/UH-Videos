import os

def check_files_in_directory(directory_path):
    """
    Lee todos los archivos en un directorio dado y verifica si el primer carácter 
    del contenido de cada archivo es un '<'. Si no lo es, imprime el nombre del archivo.

    Args:
        directory_path (str): La ruta al directorio que contiene los archivos.
    """
    # Iterar sobre todos los archivos en el directorio dado
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Asegurarse de que sea un archivo y no un directorio
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                first_char = file.read(1)  # Leer el primer carácter
                if first_char != '<':
                    print(f"El archivo '{filename}' no comienza con '<'")

# Ejemplo de uso:
directory_path = './'  # Cambia esto por la ruta de tu directorio
check_files_in_directory(directory_path)
