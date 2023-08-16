import requests

# Realizar la solicitud web para obtener los datos
url = "https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex.json"
response = requests.get(url)
data = response.json()

# Procesar los datos y crear una estructura para el JSON resultante
processed_data = []

for entry in data:
    processed_entry = {
        "id": entry["id"],
        "formId": entry["formId"],
        "dexNr": entry["dexNr"],
        "generation": entry["generation"],
        "primaryType": entry["types"][0]["name"],
        "secondaryType": entry["types"][1]["name"] if len(entry["types"]) > 1 else None,
        "names": {
            "en": entry["name"],
            "es": entry["nameES"]
        },
        "quickMoves": {
            "en": entry["quickMoves"],
            "es": entry["quickMovesES"]
        }
    }
    processed_data.append(processed_entry)

# Guardar los datos procesados en un archivo JSON
output_filename = "pokemon_data.json"
with open(output_filename, "w") as outfile:
    json.dump(processed_data, outfile, indent=4)

print(f"Datos procesados guardados en '{output_filename}'")