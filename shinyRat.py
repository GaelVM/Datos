import requests
from bs4 import BeautifulSoup
import json

url = "https://shinyrates.com/"

# Realizamos la solicitud GET a la URL
response = requests.get(url)

# Comprobamos si la solicitud fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encuentra la tabla con el id 'shiny_table'
    table = soup.find('table', {'id': 'shiny_table'})
    
    data = []
    
    # Itera a través de las filas de la tabla
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        
        # Verifica que haya al menos 5 columnas en la fila
        if len(cols) >= 5:
            item = {
                'ID': cols[1].text.strip(),
                'Name': cols[2].text.strip(),
                'Shiny Rate': cols[3].text.strip(),
                'Sample Size': cols[4].text.strip()
            }
            data.append(item)
    
    # Convierte los datos a formato JSON
    json_data = json.dumps(data, indent=4)
    
    # Guarda el JSON en un archivo llamado ShinyRate.json
    with open('ShinyRate.json', 'w') as json_file:
        json_file.write(json_data)
    
    print("Los datos se han guardado en ShinyRate.json")
else:
    print("No se pudo acceder a la página:", response.status_code)
