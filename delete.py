import requests

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users/'
headers = {
    "X-USER-TOKEN":"fosi1234"
}

graph_endpoint = f"{ORIGINAL_ENDPOINT}/fosika"
    


response = requests.delete(url=graph_endpoint, headers=headers)
print(response.text)
print(response.status_code)

"""def create():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"

    graph_config = {
        "id":GRAPHID,
        "name":"Daily Activity Level",
        "unit":"commit",
        "type":"int",
        "color":"ichou"
    }

    response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
    print(response.text)"""
