import requests
from bs4 import BeautifulSoup
import json

# URL del sitio web a raspar
url = "https://moonani.com/PokeList/pvp2500.php"

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

    pokemon_data = {
        "#": number,
        "Name": name,
        "NumberDex": number_dex,
        "Fast Skill": fast_skill,
        "Charged Skill 1": charged_skill_1,
        "Charged Skill 2": charged_skill_2,
        "Level": level,
        "CP": cp,
        "IV": iv
    }

    data.append(pokemon_data)

# Cargar el archivo JSON externo de ataques
external_data_url = "https://raw.githubusercontent.com/GaelVM/Datos/main/pokemon_data.json"
response = requests.get(external_data_url)
if response.status_code == 200:
    external_data = json.loads(response.text)
else:
    print("Error al acceder al archivo JSON externo:", response.status_code)
    exit()

# Definir una función para obtener la traducción de un ataque
def obtener_traduccion(ataque_en):
    ataque_sin_asterisco = ataque_en.rstrip('*')
    for pokemon_entry in external_data:
        for attack_entry in pokemon_entry.get("attacks", []):
            if attack_entry["en"] == ataque_sin_asterisco:
                traduccion_es = attack_entry["es"]
                if ataque_en.endswith('*'):
                    traduccion_es = f"{traduccion_es} (*)"
                return traduccion_es
    return ataque_en

# Reemplazar los nombres de los ataques con las traducciones en español si hay coincidencias
for pokemon in data:
    pokemon["Fast Skill"] = obtener_traduccion(pokemon["Fast Skill"])
    pokemon["Charged Skill 1"] = obtener_traduccion(pokemon["Charged Skill 1"])
    pokemon["Charged Skill 2"] = obtener_traduccion(pokemon["Charged Skill 2"])

# Agregar información de "image" y "shinyImage" de la estructura JSON de comparación
for pokemon in data:
    number_dex = pokemon["NumberDex"]
    for entry in external_data:
        if entry["dexNr"] == int(number_dex):
            if "regionForms" in entry:
                for region_form in entry["regionForms"]:
                    if region_form["id"] == entry["id"]:
                        pokemon["primaryType"] = region_form["primaryType"]["es"]
                        pokemon["secondaryType"] = region_form["secondaryType"]["es"]
                        pokemon["image"] = region_form["assets"]["image"]
                        pokemon["shinyImage"] = region_form["assets"]["shinyImage"]
                        break
                else:
                    pokemon["primaryType"] = entry["primaryType"]["es"]
                    pokemon["secondaryType"] = entry["secondaryType"]["es"]
                    pokemon["image"] = entry["assets"]["image"]
                    pokemon["shinyImage"] = entry["assets"]["shinyImage"]
            else:
                pokemon["primaryType"] = entry["primaryType"]["es"]
                pokemon["secondaryType"] = entry["secondaryType"]["es"]
                pokemon["image"] = entry["assets"]["image"]
                pokemon["shinyImage"] = entry["assets"]["shinyImage"]
            break

# Guardar en formato JSON
output_file = "pvp2500_data.json"

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"Se han raspado y guardado {len(data)} registros en {output_file}")
