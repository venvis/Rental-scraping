import requests

url = 'https://hip.huurcommissie.nl/file?guid=73464968925932104&changedDate=1729051223157&name=2308288.pdf'
file_name = '2308288.pdf'

try:
    response = requests.get(url)
    response.raise_for_status()  
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"{file_name} downloaded successfully!")
except requests.exceptions.RequestException as e:
    print(f"Failed to download the file: {e}")
