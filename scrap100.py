import requests
from bs4 import BeautifulSoup
import time
import json

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
            # Crear una lista para almacenar los datos de cada fila de la tabla
            data_list = []

            # Iterar a través de las filas de la tabla (excepto la primera que contiene encabezados)
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) >= 14:
                    # Extraer los datos de cada columna
                    name = columns[0].text.strip()
                    number = columns[1].text.strip()
                    coords = columns[2].text.strip()
                    cp = columns[3].text.strip()
                    level = columns[4].text.strip()
                    attack = columns[5].text.strip()
                    defense = columns[6].text.strip()
                    hp = columns[7].text.strip()
                    iv = columns[8].text.strip()
                    form = columns[9].text.strip()
                    shiny = columns[10].text.strip()
                    start_time = columns[11].text.strip()
                    end_time = columns[12].text.strip()
                    country = columns[13].text.strip()

                    # Crear un diccionario con los datos
                    data = {
                        "Name": name,
                        "Number": number,
                        "Coords": coords,
                        "CP": cp,
                        "Level": level,
                        "Attack": attack,
                        "Defense": defense,
                        "HP": hp,
                        "IV": iv,
                        "Form": form,
                        "Shiny": shiny,
                        "Start Time": start_time,
                        "End Time": end_time,
                        "Country": country
                    }

                    # Agregar el diccionario a la lista
                    data_list.append(data)

            # Convertir la lista de datos en un objeto JSON
            json_data = json.dumps(data_list, indent=4)

            # Imprimir el JSON o guardarlo en un archivo
            print(json_data)
        else:
            print("No se encontró la tabla con ID 'customers'")
    else:
        print("No se pudo acceder al sitio web")

if __name__ == "__main__":
    while True:
        scrape_website()
        # Esperar un minuto antes de ejecutar la siguiente solicitud
        time.sleep(60)
