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

    cinematic_moves_en = []
    cinematic_moves_es = []
    cinematic_moves_data = entry.get("cinematicMoves", {})
    if isinstance(cinematic_moves_data, dict):
        for move_key, move_data in cinematic_moves_data.items():
            move_names = move_data.get("names")
            if move_names:
                cinematic_moves_en.append(move_names["English"])
                cinematic_moves_es.append(move_names["Spanish"])

    elite_quick_moves_en = []
    elite_quick_moves_es = []
    elite_quick_moves_data = entry.get("eliteQuickMoves", {})
    if isinstance(elite_quick_moves_data, dict):
        for move_key, move_data in elite_quick_moves_data.items():
            move_names = move_data.get("names")
            if move_names:
                elite_quick_moves_en.append(move_names["English"])
                elite_quick_moves_es.append(move_names["Spanish"])

    elite_cinematic_moves_en = []
    elite_cinematic_moves_es = []
    elite_cinematic_moves_data = entry.get("eliteCinematicMoves", {})
    if isinstance(elite_cinematic_moves_data, dict):
        for move_key, move_data in elite_cinematic_moves_data.items():
            move_names = move_data.get("names")
            if move_names:
                elite_cinematic_moves_en.append(move_names["English"])
                elite_cinematic_moves_es.append(move_names["Spanish"])

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
                    },
                    "assets": {
                        "image": mega_evo["assets"]["image"] if mega_evo.get("assets") else None,
                        "shinyImage": mega_evo["assets"]["shinyImage"] if mega_evo.get("assets") else None
                    }
                }
                mega_evolutions.append(mega_entry)

    region_forms = []
    region_forms_data = entry.get("regionForms", [])
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
                    "en": [value["names"]["English"] for value in form_data.get("quickMoves", {}).values()],
                    "es": [value["names"]["Spanish"] for value in form_data.get("quickMoves", {}).values()]
                },
                 "cinematicMoves": {
                    "en": [value["names"]["English"] for value in form_data.get("cinematicMoves", {}).values()],
                    "es": [value["names"]["Spanish"] for value in form_data.get("cinematicMoves", {}).values()]
                },
                "eliteQuickMoves": form_data.get("eliteQuickMoves", []),
                "eliteCinematicMoves": {
                "en": [value["names"]["English"] for value in form_data.get("eliteCinematicMoves", {}).values()],
                "es": [value["names"]["Spanish"] for value in form_data.get("eliteCinematicMoves", {}).values()]
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
        "hasMegaEvolution": entry.get("hasMegaEvolution", False),
        "megaEvolutions": mega_evolutions,
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
