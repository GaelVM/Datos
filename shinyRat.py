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
        matching_pokemon = next((pokemon for pokemon in data_pokedex if pokemon["nombre"] == item["name"]), None)

        if matching_pokemon:
            formatted_item = {
                "ID": item["id"],
                "Name": item["name"],
                "Shiny Rate": item["rate"],
                "Sample Size": item["total"],
                "assets": {
                    "image": matching_pokemon["assets"]["image"]
                },
                "primaryType": {
                    "es": matching_pokemon["primaryType"]["es"]
                }
            }
            formatted_data.append(formatted_item)

    # Ordenar la lista por "Shiny Rate" en orden ascendente
    sorted_data = sorted(formatted_data, key=lambda x: int(x["Shiny Rate"].replace(",", "").split("/")[1]))

    # Asignar un número secuencial a los elementos
    contador = 1
    for item in sorted_data:
        item["Top Number"] = contador
        contador += 1

    # Ahora, puedes guardar sorted_data como JSON si lo deseas
    with open("ShinyRat.json", "w") as file:
        json.dump(sorted_data, file, indent=4)

else:
    print("No se pudo acceder a una de las URLs.")
