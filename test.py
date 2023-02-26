import requests, json


### Default Json
new_item = {
    "description": "EDIT_THIS_LONGER_DESCRIPTION",
    "endpoint": "http://127.0.0.1:8530",
    "name": "New Element",
    "protocol": "A10HTTPREST",
    "type": [
        "tpm2.0"
    ],
    "attribute": "test"
}


# Get all elements
response = requests.get("http://127.0.0.1:8510/v2/elements")

r = requests.post("http://127.0.0.1:8510/v2/element", json=new_item)
#r = requests.post('http://127.0.0.1:8510/v2/element', json={"key": "value"})


print(r.status_code)
print(r.json())
print(response.status_code)
print(response.json())