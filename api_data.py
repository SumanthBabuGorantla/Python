import requests
import pandas as pd
import csv
response = requests.get("https://api.le-systeme-solaire.net/rest/bodies")

nasa_data = response.json()['bodies']
#print(nasa_data[0])

headers = list(nasa_data[0].keys())
#print(headers)

data = open('C:/CDI_flatfile/output.csv', 'w', newline='',encoding='utf-8')
csv_writer = csv.DictWriter(data, fieldnames=headers)

    # Write headers
csv_writer.writeheader()

    # Write rows
csv_writer.writerows(nasa_data)