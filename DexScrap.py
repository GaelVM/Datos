import requests
from bs4 import BeautifulSoup
import json
import re

# URL del sitio web a raspar
url = "https://gostats.app/pokedex"

# Realizar una solicitud GET al sitio web
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar todos los elementos <span> con la clase "badge"
    badge_elements = soup.find_all("span", {"class": "badge"})
    
    # Inicializar una lista para almacenar los datos de los pokemons
    pokemon_data = []
    
    # Iterar a través de los elementos <span>
    for badge in badge_elements:
        # Obtener el texto dentro del elemento <span>
        span_text = badge.get_text().strip()
        
        # Utilizar expresiones regulares para extraer los datos
        match = re.search(r'#(\d+) (.+?)MAX PC: (\d+)MAX PC 50: (\d+)', span_text)
        if match:
            nodex = match.group(1)
            name = match.group(2)
            max_pc = match.group(3)
            max_pc_50 = match.group(4)[:4]  # Tomar los primeros 4 dígitos
        else:
            nodex = "No encontrado"
            name = "No encontrado"
            max_pc = "No encontrado"
            max_pc_50 = "No encontrado"
        
        # Crear un diccionario con los datos del pokemon
        pokemon = {
            "nodex": nodex,
            "nombre": name,
            "maxpc": max_pc,
            "maxpc50": max_pc_50,
        }
        
        # Agregar el diccionario a la lista
        pokemon_data.append(pokemon)
    
    # Convertir la lista de datos de pokemons a JSON
    json_data = json.dumps(pokemon_data, indent=4, ensure_ascii=False)
    
    # Guardar el JSON en un archivo llamado "pokedex2023.json"
    with open("pokedex2023.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    print("El archivo pokedex2023.json ha sido creado exitosamente.")

else:
    print("Error al realizar la solicitud al sitio web.")
