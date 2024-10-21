import json

with open("extracted_data_1.json", "r") as json_file:
    data = json.load(json_file)

with open("output.txt", "w") as output_file:
    for key, value in data.items():
        first_seven_chars = value[:7]
        
        output_file.write(f"https://hip.huurcommissie.nl/file?guid=73464968925932104&changedDate=1729051223157&name={first_seven_chars}.pdf\n")

print("Data processed and saved to output.txt")
