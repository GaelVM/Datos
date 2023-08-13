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

# Encontrar los elementos que contienen la información
pokemon_entries = soup.find_all("div", class_="pokemon-entry")

data = []

for index, entry in enumerate(pokemon_entries, start=1):
    number = index
    name = entry.find("h3").text
    fast_skill = entry.find("p", class_="fast-skill").text
    charged_skills = entry.find_all("p", class_="charged-skill")
    charged_skill_1 = charged_skills[0].text
    charged_skill_2 = charged_skills[1].text
    level = entry.find("p", class_="level").text
    cp = entry.find("p", class_="cp").text
    iv = entry.find("p", class_="iv").text

    pokemon_data = {
        "#": number,
        "Name": name,
        "Number": number,
        "Fast Skill": fast_skill,
        "Charged Skill 1": charged_skill_1,
        "Charged Skill 2": charged_skill_2,
        "Level": level,
        "CP": cp,
        "IV": iv
    }

    data.append(pokemon_data)

# Guardar en formato JSON
output_file = "pvp1500_data.json"

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"Se han raspado y guardado {len(data)} registros en {output_file}")