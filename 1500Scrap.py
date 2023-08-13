import requests
from bs4 import BeautifulSoup
import json
import os

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

    # Obtener información adicional del Pokémon desde la API
    number_dex_int = int(number_dex)
    api_url = f"https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex/id/{number_dex}.json"
    api_response = requests.get(api_url)

    if api_response.status_code == 200:
        api_data = api_response.json()
        primary_type = api_data.get("primaryType", {}).get("names", {}).get("Spanish", "Desconocido")

        secondary_type_data = api_data.get("secondaryType", {})
        if secondary_type_data:
            secondary_type = secondary_type_data.get("names", {}).get("Spanish", None)
        else:
            secondary_type = None

        region_forms = api_data.get("regionForms", [])

        image_url = "N/A"
        shiny_image_url = "N/A"

        name_lower = name.lower()
        if "galarian" in name_lower:
            assets_galarian = {}
            for form_key, form_data in region_forms.items():
                if "GALARIAN" in form_key:
                    assets_galarian = form_data.get("assets", {})
                    image_url = assets_galarian.get("image", image_url)
                    shiny_image_url = assets_galarian.get("shinyImage", shiny_image_url)
                    break  # Detener la búsqueda una vez que se encuentre la forma "GALARIAN"
        elif "shadow" in name_lower:
            # Agrega aquí las URLs reales de las imágenes para Pokémon Shadow
            image_url = "URL de la imagen para Pokémon Shadow"
            shiny_image_url = "URL de la imagen shiny para Pokémon Shadow"
            # Agrega aquí las URLs reales de las imágenes para Pokémon Shadow
            image_url = "URL de la imagen para Pokémon Shadow"
            shiny_image_url = "URL de la imagen shiny para Pokémon Shadow"

        else:
            assets_normal = api_data.get("assets", {})
            image_url = assets_normal.get("image", image_url)
            shiny_image_url = assets_normal.get("shinyImage", shiny_image_url)

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

# Directorio de salida
output_directory = "Data"

# Crear el directorio si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Guardar en formato JSON en la carpeta /Data
output_file = os.path.join(output_directory, "pvp1500_data.json")
with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Se han raspado y guardado {len(data)} registros en {output_file}")