import requests

# URL for your FastAPI endpoint
url = "http://127.0.0.1:8000/uploadfiles/"

# File paths to be sent in the request
files = [
    ('files', ('ocr.png', open('files/ocr.png', 'rb'), 'application/png')),
    # ('files', ('produceSales.xlsx', open('produceSales.xlsx', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')),
]

# Send the POST request with files
response = requests.post(url, files=files)

# Print the response from the API
print(response.status_code)
print(response.json())
