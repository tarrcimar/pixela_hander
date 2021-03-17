import requests

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users/'
headers = {
    "X-USER-TOKEN":"skljfva8a4wrm283"
}

graph_endpoint = f"{ORIGINAL_ENDPOINT}/tmarton/graphs"
    
create_params = {
    "id":"fos1",
    "name":"Fostoló",
    "unit":"fos",
    "type":"int",
    "color":"shibafu"
}

print(create_params)

response = requests.post(url=graph_endpoint, json=create_params, headers=headers)
print(response.text)
with open("user.txt", "a") as file:
    file.write(",fos1")
