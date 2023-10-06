import requests
import json

url = "https://shinyrates.com/data/rate/"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    formatted_data = []

    for item in data:
        formatted_item = {
            "ID": item["id"],
            "Name": item["name"],
            "Shiny Rate": item["rate"],
            "Sample Size": item["total"]
        }
        formatted_data.append(formatted_item)

    # Ordenar los datos por el segundo valor en "Shiny Rate" en orden ascendente
    sorted_data = sorted(formatted_data, key=lambda x: int(x["Shiny Rate"].replace(",", "").split("/")[1]))

    # Asignar un número secuencial a los elementos con "Shiny Rate" que contiene "1"
    contador = 1
    for item in sorted_data:
        if "1" in item["Shiny Rate"]:
            item["Top Number"] = contador
            contador += 1
        else:
            item["Top Number"] = None

    # Ahora, puedes guardar sorted_data como JSON si lo deseas
    with open("ShinyRat.json", "w") as file:
        json.dump(sorted_data, file, indent=4)

else:
    print("No se pudo acceder al sitio web.")
