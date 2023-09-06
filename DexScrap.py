import requests
import json

# URL del JSON en GitHub
json_url = "https://raw.githubusercontent.com/GaelVM/Datos/main/pokemon_data.json"

# Descargar el JSON desde la URL
response = requests.get(json_url)

# Comprobar si la descarga fue exitosa
if response.status_code == 200:
    # Cargar el JSON descargado
    json_data = json.loads(response.text)

    # Cargar el JSON generado anteriormente
    with open("pokedex2023.json", "r", encoding="utf-8") as generated_json_file:
        generated_data = json.load(generated_json_file)

    # Inicializar una lista para almacenar los datos coincidentes
    matched_data = []

    # Iterar a través de los datos generados
    for generated_pokemon in generated_data:
        # Obtener el valor de "nodex" del JSON generado
        generated_nodex = generated_pokemon["nodex"]
        
        # Buscar una coincidencia en el JSON descargado por "dexNr"
        matching_pokemon = next((pokemon for pokemon in json_data if pokemon.get("dexNr") == generated_nodex), None)
        
        if matching_pokemon:
            # Extraer la información deseada y agregarla a la lista
            extracted_data = {
                "nodex": generated_pokemon["nodex"],
                "nombre": generated_pokemon["nombre"],
                "maxpc": generated_pokemon["maxpc"],
                "maxpc50": generated_pokemon["maxpc50"],
                "primaryType": matching_pokemon.get("primaryType"),
                "secondaryType": matching_pokemon.get("secondaryType"),
                "assets": {
                    "image": matching_pokemon.get("assets", {}).get("image"),
                    "shinyImage": matching_pokemon.get("assets", {}).get("shinyImage"),
                }
            }
            
            matched_data.append(extracted_data)

    # Convertir la lista de datos coincidentes a JSON
    matched_json = json.dumps(matched_data, indent=4, ensure_ascii=False)

    # Guardar el JSON de datos coincidentes en un archivo
    with open("matched_pokemon_data.json", "w", encoding="utf-8") as matched_json_file:
        matched_json_file.write(matched_json)

    print("Se ha creado el archivo matched_pokemon_data.json con los datos coincidentes.")

else:
    print("Error al descargar el JSON desde la URL.")
