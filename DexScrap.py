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
        # Obtener el texto dentro del div
        info_text = col.get_text()
        
        # Dividir el texto en líneas
        lines = info_text.split("\n")
        
        # Comprobar si hay suficientes líneas antes de acceder a los elementos
        if len(lines) >= 4:
            nodex = lines[0].strip()
            nombre = lines[1].strip()
            max_pc = lines[2].split(":")[1].strip()
            max_pc50 = lines[3].split(":")[1].strip()
            
            # Crear un diccionario con los datos del pokemon
            pokemon = {
                "nodex": nodex,
                "nombre": nombre,
                "maxpc": max_pc,
                "maxpc50": max_pc50,
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
