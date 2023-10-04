import requests
from bs4 import BeautifulSoup
import time

def scrape_website():
    url = "https://moonani.com/PokeList/index.php"

    # Realizar una solicitud GET al sitio web
    response = requests.get(url)

    if response.status_code == 200:
        # Analizar el contenido de la página web con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar la tabla con el ID "customers"
        table = soup.find('table', {'id': 'customers'})

        if table:
            # Procesar y almacenar los datos de la tabla aquí
            # Por ejemplo, puedes imprimir los datos:
            print(table.text)
        else:
            print("No se encontró la tabla con ID 'customers'")
    else:
        print("No se pudo acceder al sitio web")

if __name__ == "__main__":
    while True:
        scrape_website()
        # Esperar un minuto antes de ejecutar la siguiente solicitud
        time.sleep(60)