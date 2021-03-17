import requests

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users'
headers = {
    "X-USER-TOKEN":"12381jdj12jdj"
}

graph_endpoint = f"{ORIGINAL_ENDPOINT}/fosika"

response = requests.delete(url=graph_endpoint, headers=headers)
print(response.text)
