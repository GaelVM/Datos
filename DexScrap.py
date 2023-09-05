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
        # Comprobar si se encontró el nombre del pokemon
        nombre_element = col.find("h2")
        nombre = nombre_element.text.strip() if nombre_element else "Nombre no encontrado"
        
        # Comprobar si se encontró el tipo del pokemon
        tipo_element = col.find("p", {"class": "type"})
        tipo = tipo_element.text.strip() if tipo_element else "Tipo no encontrado"
        
        # Comprobar si se encontró la altura del pokemon
        altura_element = col.find("p", {"class": "height"})
        altura = altura_element.text.strip() if altura_element else "Altura no encontrada"
        
        # Comprobar si se encontró el peso del pokemon
        peso_element = col.find("p", {"class": "weight"})
        peso = peso_element.text.strip() if peso_element else "Peso no encontrado"
        
        # Crear un diccionario con los datos del pokemon
        pokemon = {
            "nombre": nombre,
            "tipo": tipo,
            "altura": altura,
            "peso": peso
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
