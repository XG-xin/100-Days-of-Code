import requests
import os
from flight_data import FlightData
from pprint import pprint

KIWI_ENDPOINT = os.environ.get("KIWI_ENDPOINT")
KIWI_API_KEY = os.environ.get("KIWI_API_KEY")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def get_destination_code(self, city_name):
        location_endpoint = f"{KIWI_ENDPOINT}/locations/query"
        headers = {
            "apikey": KIWI_API_KEY,
        }
        query = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        print(results)
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        header = {
            "apikey": KIWI_API_KEY
        }
        search_params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url=f"{KIWI_ENDPOINT}/v2/search", params=search_params, headers=header)
        try:
            data = response.json()["data"][0]
        except IndexError:
            # print(f"No flights found for {destination_city_code}.")
            search_params["max_stopovers"] = 2
            response = requests.get(url=f"{KIWI_ENDPOINT}/v2/search", params=search_params, headers=header)
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                print(print(f"{flight_data.destination_city}: ${flight_data.price}"))
                return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city = data["route"][0]["cityFrom"],
                origin_airport = data["route"][0]["flyFrom"],
                destination_city = data["route"][0]["cityTo"],
                destination_airport = data["route"][0]["flyTo"],
                out_date =data["route"][0]["local_departure"].split("T")[0],
                return_date = data["route"][1]["local_departure"].split("T")[0]
            )

            if flight_data.stop_overs >=1:
                print(f"{flight_data.destination_city}: ${flight_data.price}")
                print(f"flight has {flight_data.stop_overs} stop over, via {flight_data.via_city} city")
            else:
                print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
