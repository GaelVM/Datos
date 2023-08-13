import requests
from bs4 import BeautifulSoup
import json

# URL del sitio web a raspar
url = "https://moonani.com/PokeList/pvp1500.php"

# Realizar la solicitud HTTP
response = requests.get(url)

if response.status_code == 200:
    page_content = response.content
else:
    print("Error al acceder al sitio web:", response.status_code)
    exit()

# Analizar el contenido HTML
soup = BeautifulSoup(page_content, 'html.parser')

# Encontrar la tabla por su atributo id
table = soup.find("table", id="customers")

data = []

# Iterar sobre las filas de la tabla
for row in table.find_all("tr")[1:]:  # Ignorar la primera fila de encabezados
    cells = row.find_all("td")

    number = cells[0].text
    name = cells[1].text
    number_dex = cells[2].text
    fast_skill = cells[3].text
    charged_skill_1 = cells[4].text
    charged_skill_2 = cells[5].text
    level = cells[6].text
    cp = cells[7].text
    iv = cells[8].text

    # Realizar solicitud para obtener los datos del tipo del Pokémon
    type_url = f"https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex/id/{number_dex}.json"
    type_response = requests.get(type_url)

    if type_response.status_code == 200:
        type_data = type_response.json()

        primary_type = type_data["primaryType"]["names"]["Spanish"]
        secondary_type = type_data["secondaryType"]["names"]["Spanish"] if type_data["secondaryType"] else None

        assets = type_data.get("assets", {})
        image_url = assets.get("image", "N/A")
        shiny_image_url = assets.get("shinyImage", "N/A")

        name_lower = name.lower()
        if "galarian" in name_lower:
            region_forms = type_data.get("regionForms", [])
            if region_forms and len(region_forms) > 0:
                image_url = region_forms[0].get("image", image_url)
                shiny_image_url = region_forms[0].get("shinyImage", shiny_image_url)
        elif "shadow" in name_lower:
            # Agrega aquí las URLs reales de las imágenes para Pokémon Shadow
            image_url = "URL de la imagen para Pokémon Shadow"
            shiny_image_url = "URL de la imagen shiny para Pokémon Shadow"
    else:
        primary_type = "Desconocido"
        secondary_type = None
        image_url = "N/A"
        shiny_image_url = "N/A"

    pokemon_data = {
        "#": number,
        "Name": name,
        "NumberDex": number_dex,
        "Fast Skill": fast_skill,
        "Charged Skill 1": charged_skill_1,
        "Charged Skill 2": charged_skill_2,
        "Level": level,
        "CP": cp,
        "IV": iv,
        "primaryType": primary_type,
        "secondaryType": secondary_type,
        "image": image_url,
        "shinyImage": shiny_image_url
    }

    data.append(pokemon_data)

# Guardar en formato JSON
output_file = "pvp1500_data.json"

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Se han raspado y guardado {len(data)} registros en {output_file}")
