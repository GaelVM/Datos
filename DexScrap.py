import requests
from bs4 import BeautifulSoup
import json

# URL del sitio web a raspar
url = "https://gostats.app/pokedex"

# Realizar una solicitud GET al sitio web
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar el div con id "pokemons"
    pokemons_div = soup.find("div", {"id": "pokemons"})
    
    # Encontrar todos los divs con la clase "col"
    col_divs = pokemons_div.find_all("div", {"class": "col"})
    
    # Inicializar una lista para almacenar los datos de los pokemons
    pokemon_data = []
    
    # Iterar a través de los divs con clase "col"
    for col in col_divs:
        # Obtener el texto dentro del span
        span_text = col.span.get_text()
        
        # Dividir el texto en líneas
        lines = span_text.split("\n")
        
        # Extraer los datos que deseas
        nodex_and_name = lines[2].strip()
        max_pc = lines[3].strip()
        max_pc_50 = lines[4].strip()
        
        # Separar el número de nodo y el nombre
        nodex, name = nodex_and_name.split(" ", 1)
        
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
