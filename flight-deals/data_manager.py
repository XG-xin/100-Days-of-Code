import requests
from pprint import pprint
import os

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

        # # print(data["id"])
    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        sheet_data = response.json()
        self.destination_data = sheet_data["prices"]
        return self.destination_data

    def update_iata_code(self):
        for city in self.destination_data:

            update_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            sheety_header = {
                "Content-Type": 'application/json'
            }
            sheety_response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=update_data, headers=sheety_header)
            print(sheety_response.text)
            
            
