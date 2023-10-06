import requests
import json

# Obtener los datos de tu URL
url_shinyrates = "https://shinyrates.com/data/rate/"
url_pokedex = "https://raw.githubusercontent.com/GaelVM/Datos/main/pokedex2023.json"

response_shinyrates = requests.get(url_shinyrates)
response_pokedex = requests.get(url_pokedex)

if response_shinyrates.status_code == 200 and response_pokedex.status_code == 200:
    data_shinyrates = response_shinyrates.json()
    data_pokedex = response_pokedex.json()

    formatted_data = []

    for item in data_shinyrates:
        # Buscar el elemento correspondiente en el JSON de la pokedex por nombre
        matching_pokemon = next((pokemon for pokemon in data_pokedex if pokemon["nombre"] == item["Name"]), None)

        if matching_pokemon:
            formatted_item = {
                "ID": item["id"],
                "Name": item["Name"],
                "Shiny Rate": item["Shiny Rate"],
                "Sample Size": item["Sample Size"],
                "assets": {
                    "image": matching_pokemon["assets"]["image"]
                },
                "primaryType": {
                    "es": matching_pokemon["primaryType"]["es"]
                }
            }
            formatted_data.append(formatted_item)

    # Ahora, puedes guardar formatted_data como JSON si lo deseas
    with open("ShinyRat.json", "w") as file:
        json.dump(formatted_data, file, indent=4)

else:
    print("No se pudo acceder a una de las URLs.")
