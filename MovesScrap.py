import requests
from bs4 import BeautifulSoup
import json

# URL de la página a raspar en inglés y en español
url_en = "https://pokemon.gameinfo.io/en/moves"
url_es = "https://pokemon.gameinfo.io/es/moves"

# Realiza la solicitud GET a la página en inglés
response_en = requests.get(url_en)
soup_en = BeautifulSoup(response_en.text, 'html.parser')

# Realiza la solicitud GET a la página en español
response_es = requests.get(url_es)
soup_es = BeautifulSoup(response_es.text, 'html.parser')

# Encuentra la tabla de movimientos en inglés
table_en = soup_en.find('table', class_='sortable')

# Encuentra la tabla de movimientos en español
table_es = soup_es.find('table', class_='sortable')

# Crear listas para almacenar los datos
moves_data = []

# Iterar a través de las filas de la tabla en inglés
for row_en, row_es in zip(table_en.find_all('tr')[1:], table_es.find_all('tr')[1:]):
    cells_en = row_en.find_all('td')
    cells_es = row_es.find_all('td')

    move_name_en = cells_en[1].text.strip()

    # Comprobar si existe un elemento <span> dentro de la celda
    span_en = cells_en[2].find('span')
    if span_en is not None and 'data-type' in span_en.attrs:
        move_type_en = span_en['data-type']
    else:
        move_type_en = "Unknown"

    move_name_es = cells_es[1].text.strip()

    # Comprobar si existe un elemento <span> dentro de la celda
    span_es = cells_es[2].find('span')
    if span_es is not None and 'data-type' in span_es.attrs:
        move_type_es = span_es['data-type']
    else:
        move_type_es = "Unknown"

    move_data = {
        "ataque": move_name_en,
        "tipo": move_type_en,
        "ataquetraduccion": move_name_es,
        "tipotraduccion": move_type_es
    }

    moves_data.append(move_data)

# Guarda los datos en un archivo JSON
with open('moves_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(moves_data, json_file, ensure_ascii=False, indent=4)

print("Raspado completado y datos guardados en moves_data.json")