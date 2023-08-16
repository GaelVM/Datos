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

    region_forms = []
    region_forms_data = entry.get("regionForms", {})
    if isinstance(region_forms_data, dict):
        for form_id, form_data in region_forms_data.items():
            form_entry = {
                "id": form_data.get("id"),
                "formId": form_data.get("formId"),
                "dexNr": form_data.get("dexNr"),
                "generation": form_data.get("generation"),
                "primaryType": {
                    "en": form_data["primaryType"]["names"]["English"],
                    "es": form_data["primaryType"]["names"]["Spanish"]
                },
                "secondaryType": {
                    "en": form_data["secondaryType"]["names"]["English"] if form_data.get("secondaryType") else None,
                    "es": form_data["secondaryType"]["names"]["Spanish"] if form_data.get("secondaryType") else None
                },
                "names": {
                    "en": form_data["names"]["English"],
                    "es": form_data["names"]["Spanish"]
                },
                "quickMoves": {
                    "en": form_data.get("quickMoves", {}).get("names", {}).get("English", {}),
                    "es": form_data.get("quickMoves", {}).get("names", {}).get("Spanish", {})
                },
                "cinematicMoves": {
                    "en": form_data.get("cinematicMoves", {}).get("names", {}).get("English", {}),
                    "es": form_data.get("cinematicMoves", {}).get("names", {}).get("Spanish", {})
                },
                "eliteQuickMoves": {
                    "en": form_data.get("eliteQuickMoves", {}).get("names", {}).get("English", []),
                    "es": form_data.get("eliteQuickMoves", {}).get("names", {}).get("Spanish", [])
                },
                "eliteCinematicMoves": {
                    "en": form_data.get("eliteCinematicMoves", {}).get("names", {}).get("English", []),
                    "es": form_data.get("eliteCinematicMoves", {}).get("names", {}).get("Spanish", [])
                },
                "assets": {
                    "image": form_data["assets"]["image"] if form_data.get("assets") else None,
                    "shinyImage": form_data["assets"]["shinyImage"] if form_data.get("assets") else None
                }
                # Agregar más campos aquí según sea necesario
            }
            region_forms.append(form_entry)

    stats = entry.get("stats")
    stats_en = {
        "stamina": stats.get("stamina") if stats else None,
        "attack": stats.get("attack") if stats else None,
        "defense": stats.get("defense") if stats else None
    }

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
        "regionForms": region_forms,
        "stats": stats_en,
        "assets": {
            "image": entry["assets"]["image"] if entry.get("assets") else None,
            "shinyImage": entry["assets"]["shinyImage"] if entry.get("assets") else None
        }
    }
    processed_data.append(processed_entry)

# Guardar los datos procesados en un archivo JSON
output_filename = "pokemon_data.json"
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(processed_data, outfile, indent=4, ensure_ascii=False)

print(f"Datos procesados guardados en '{output_filename}'")
