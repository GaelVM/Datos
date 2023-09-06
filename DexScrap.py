import requests
from bs4 import BeautifulSoup
import json
import re

# URL del sitio web a raspar
url = "https://gostats.app/pokedex"

# URL del JSON con datos adicionales
json_url = "https://raw.githubusercontent.com/GaelVM/Datos/main/pokemon_data.json"

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
        
        # Realizar una solicitud GET al JSON
        json_response = requests.get(json_url)
        
        # Comprobar si la solicitud del JSON fue exitosa
        if json_response.status_code == 200:
            # Cargar el JSON desde la respuesta
            json_data = json_response.json()
            
            # Buscar el elemento correspondiente en el JSON por "dexNr" (nodex en formato numérico)
            for entry in json_data:
                if entry.get("dexNr") == int(nodex):
                    # Extraer los datos adicionales del JSON
                    primary_type = entry.get("primaryType", "No encontrado")
                    secondary_type = entry.get("secondaryType", "No encontrado")
                    assets = entry.get("assets", {})
                    image = assets.get("image", "No encontrado")
                    shiny_image = assets.get("shinyImage", "No encontrado")
                    
                    # Modificar el campo "nombre" si contiene "(Shadow)" y agregar el campo "oscuro"
                    if "(Shadow)" in name:
                        name = name.replace("(Shadow)", "(Oscuro)")
                        oscuro = "https://raw.githubusercontent.com/PokeMiners/pogo_assets/master/Images/Rocket/ic_shadow.png"
                    else:
                        oscuro = "No encontrado"
                    
                    # Crear un diccionario con todos los datos
                    pokemon = {
                        "nodex": nodex,
                        "nombre": name,
                        "maxpc": max_pc,
                        "maxpc50": max_pc_50,
                        "primaryType": primary_type,
                        "secondaryType": secondary_type,
                        "assets": {
                            "image": image,
                            "shinyImage": shiny_image,
                            "oscuro": oscuro,  # Agregar el campo "oscuro"
                        },
                    }
                    
                    # Agregar el diccionario a la lista
                    pokemon_data.append(pokemon)
                    break  # Romper el bucle una vez que se encuentra el elemento en el JSON
    
    # Convertir la lista de datos de pokemons a JSON
    json_data = json.dumps(pokemon_data, indent=4, ensure_ascii=False)
    
    # Guardar el JSON en un archivo llamado "pokedex2023.json"
    with open("pokedex2023.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

    print("El archivo pokedex2023.json ha sido creado exitosamente.")

else:
    print("Error al realizar la solicitud al sitio web.")
