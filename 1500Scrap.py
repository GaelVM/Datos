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
for index, row in enumerate(table.find_all("tr")[1:], start=1):  # Ignorar la primera fila de encabezados
    cells = row.find_all("td")

    number = str(index)  # Convierte el índice en una cadena
    name = cells[1].text
    fast_skill = cells[2].text
    charged_skill_1 = cells[3].text
    charged_skill_2 = cells[4].text
    level = cells[5].text
    cp = cells[6].text
    iv = cells[7].text

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
