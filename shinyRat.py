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

    # Ahora, puedes guardar sorted_data como JSON si lo deseas
    with open("ShinyRatSorted.json", "w") as file:
        json.dump(sorted_data, file, indent=4)

else:
    print("No se pudo acceder al sitio web.")
