from scrapAndSearch import Principal

def main():
    """
    Función principal que instancia la clase Principal y ejecuta el método run().

    Esta función se utiliza como punto de entrada para ejecutar el proceso de scraping definido en la clase Principal.
    """
    # Instancia de la clase Principal
    p = Principal()

    # Ejecución del método run() que realiza todo el proceso de scraping
    p.run()

if __name__ == "__main__":
    main()
