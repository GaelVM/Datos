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
    primary_type_es = entry["primaryType"]["names"]["Spanish"]
    secondary_type_es = entry["secondaryType"]["names"]["Spanish"] if entry.get("secondaryType") else None

    quick_moves_en = []
    quick_moves_es = []
    quick_moves_data = entry.get("quickMoves", {})
    if isinstance(quick_moves_data, dict):
        for move_key, move_data in quick_moves_data.items():
            move_names = move_data.get("names")
            if move_names:
                quick_moves_en.append(move_names["English"])
                quick_moves_es.append(move_names["Spanish"])

    mega_evolutions = []
    if entry.get("hasMegaEvolution") == True:
        mega_evolution_data = entry.get("megaEvolutions")
        if mega_evolution_data:
            for mega_evo_key, mega_evo in mega_evolution_data.items():
                mega_entry = {
                    "id": mega_evo.get("id"),
                    "names": mega_evo.get("names"),
                    "primaryType": {
                        "en": mega_evo["primaryType"]["names"]["English"],
                        "es": mega_evo["primaryType"]["names"]["Spanish"]
                    },
                    "secondaryType": {
                        "en": mega_evo["secondaryType"]["names"]["English"] if mega_evo.get("secondaryType") else None,
                        "es": mega_evo["secondaryType"]["names"]["Spanish"] if mega_evo.get("secondaryType") else None
                    }
                }
                mega_evolutions.append(mega_entry)

    processed_entry = {
        "id": entry["id"],
        "formId": entry["formId"],
        "dexNr": entry["dexNr"],
        "generation": entry["generation"],
        "primaryType": {
            "en": primary_type,
            "es": primary_type_es
        },
        "secondaryType": {
            "en": secondary_type,
            "es": secondary_type_es
        },
        "names": {
            "en": entry["names"]["English"],
            "es": entry["names"]["Spanish"]
        },
        "quickMoves": {
            "en": quick_moves_en,
            "es": quick_moves_es
        },
        "hasMegaEvolution": entry.get("hasMegaEvolution", False),
        "megaEvolutions": mega_evolutions,
        "assets": {
            "image": entry["assets"]["image"],
            "shinyImage": entry["assets"]["shinyImage"]
        }
    }
    processed_data.append(processed_entry)

# Guardar los datos procesados en un archivo JSON
output_filename = "pokemon_data.json"
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(processed_data, outfile, indent=4, ensure_ascii=False)

print(f"Datos procesados guardados en '{output_filename}'")
