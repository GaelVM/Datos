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

    quick_moves_en = [move_data["names"]["English"] for move_data in entry.get("quickMoves", {}).values()]
    quick_moves_es = [move_data["names"]["Spanish"] for move_data in entry.get("quickMoves", {}).values()]

    cinematic_moves_en = [move_data["names"]["English"] for move_data in entry.get("cinematicMoves", {}).values()]
    cinematic_moves_es = [move_data["names"]["Spanish"] for move_data in entry.get("cinematicMoves", {}).values()]

    elite_quick_moves_en = []
    elite_quick_moves_es = []
    elite_quick_moves_data = entry.get("eliteQuickMoves", [])
    for move_data in elite_quick_moves_data:
        move_names = move_data.get("names")
        if move_names:
            elite_quick_moves_en.append(move_names["English"])
            elite_quick_moves_es.append(move_names["Spanish"])

    elite_cinematic_moves_en = []
    elite_cinematic_moves_es = []
    elite_cinematic_moves_data = entry.get("eliteCinematicMoves", [])
    for move_data in elite_cinematic_moves_data:
        move_names = move_data.get("names")
        if move_names:
            elite_cinematic_moves_en.append(move_names["English"])
            elite_cinematic_moves_es.append(move_names["Spanish"])

    mega_evolutions = []
    if entry.get("hasMegaEvolution") == True:
        mega_evolution_data = entry.get("megaEvolutions")
        if mega_evolution_data:
            for mega_evo in mega_evolution_data.values():
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
                    },
                    "assets": {
                        "image": mega_evo["assets"]["image"] if mega_evo.get("assets") else None,
                        "shinyImage": mega_evo["assets"]["shinyImage"] if mega_evo.get("assets") else None
                    }
                }
                mega_evolutions.append(mega_entry)

    region_forms = []
    region_forms_data = entry.get("regionForms", {})
    for form_id, form_data in region_forms_data.items():
        form_entry = {
            "id": form_data.get("id"),
            "formId": form_data.get("formId"),
            "dexNr": form_data.get("dexNr"),
            "generation": form_data.get("generation"),
            "names": {
                "en": form_data["names"]["English"],
                "es": form_data["names"]["Spanish"]
            },
            "stats": form_data.get("stats"),
            "primaryType": {
                "en": form_data["primaryType"]["names"]["English"],
                "es": form_data["primaryType"]["names"]["Spanish"]
            },
            "secondaryType": {
                "en": form_data["secondaryType"]["names"]["English"] if form_data.get("secondaryType") else None,
                "es": form_data["secondaryType"]["names"]["Spanish"] if form_data.get("secondaryType") else None
            },
            "quickMoves": {
                "en": form_data.get("quickMoves", {}).get("names", {}).get("English", []),
                "es": form_data.get("quickMoves", {}).get("names", {}).get("Spanish", [])
            },
            "cinematicMoves": {
                "en": form_data.get("cinematicMoves", {}).get("names", {}).get("English", []),
                "es": form_data.get("cinematicMoves", {}).get("names", {}).get("Spanish", [])
            },
            "eliteQuickMoves": {
                "en": elite_quick_moves_en,
                "es": elite_quick_moves_es
            },
            "eliteCinematicMoves": {
                "en": elite_cinematic_moves_en,
                "es": elite_cinematic_moves_es
            },
            "assets": {
                "image": form_data.get("assets", {}).get("image"),
                "shinyImage": form_data.get("assets", {}).get("shinyImage")
            }
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
        "quickMoves": {
            "en": quick_moves_en,
            "es": quick_moves_es
        },
        "cinematicMoves": {
            "en": cinematic_moves_en,
            "es": cinematic_moves_es
        },
        "eliteQuickMoves": {
            "en": elite_quick_moves_en,
            "es": elite_quick_moves_es
        },
        "eliteCinematicMoves": {
            "en": elite_cinematic_moves_en,
            "es": elite_cinematic_moves_es
        },
        "assets": {
            "image": entry["assets"]["image"] if entry.get("assets") else None,
            "shinyImage": entry["assets"]["shinyImage"] if entry.get("assets") else None
        },
        "regionForms": region_forms,
        "stats": stats_en
    }

    processed_data.append(processed_entry)

# Guardar el JSON resultante en un archivo
with open("processed_pokedex.json", "w") as json_file:
    json.dump(processed_data, json_file, indent=4)

print("Datos procesados y guardados en 'processed_pokedex.json'.")
