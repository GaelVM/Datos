import requests
import json

# Realizar la solicitud web para obtener los datos
url = "https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex.json"
response = requests.get(url)
data = response.json()

# Procesar los datos y crear una estructura para el JSON resultante
processed_data = []

for entry in data:
    primary_type = entry["primaryType"]["names"]["English"]
    secondary_type = entry["secondaryType"]["names"]["English"] if entry.get("secondaryType") else None

    quick_moves_en = []
    quick_moves_es = []
    for move_data in entry["quickMoves"]:
        quick_moves_en.append(move_data["names"]["English"])
        quick_moves_es.append(move_data["names"]["Spanish"])

    processed_entry = {
        "id": entry["id"],
        "formId": entry["formId"],
        "dexNr": entry["dexNr"],
        "generation": entry["generation"],
        "primaryType": primary_type,
        "secondaryType": secondary_type,
        "names": {
            "en": entry["names"]["English"],
            "es": entry["names"]["Spanish"]
        },
        "quickMoves": {
            "en": quick_moves_en,
            "es": quick_moves_es
        }
    }
    processed_data.append(processed_entry)

# Guardar los datos procesados en un archivo JSON
output_filename = "pokemon_data.json"
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(processed_data, outfile, indent=4, ensure_ascii=False)

print(f"Datos procesados guardados en '{output_filename}'")
