import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
EXERCISE_ENDPOINT = os.environ.get("EXERCISE_ENDPOINT")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

print(EXERCISE_ENDPOINT)

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

exercise = input("Tell me which exercise you did? ")

parameters = {
    "query": exercise,
    "gender": "female",
    "weight_kg": "56.7",
    "height_cm": "158",
    "age": "28"
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=headers, data=parameters)
my_row = response.json()

today = datetime.now()

for my_exercise in my_row["exercises"]:
    my_data = {
        "workout": {
            "date": today.strftime(f'%d/%m/%Y'),
            "time": today.strftime("%X"),
            "exercise": my_exercise["name"].title(),
            "duration": str(my_exercise["duration_min"]),
            "calories": my_exercise["nf_calories"]
        }
    }

    sheety_header = {
        "Content-Type": 'application/json',
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    sheet_response = requests.post(url=SHEETY_ENDPOINT, json=my_data, headers=sheety_header)
    print(sheet_response.text)
