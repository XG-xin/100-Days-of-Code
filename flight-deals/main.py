from data_manager import DataManager
from pprint import pprint
from flight_search import FlightSearch
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from notification_manager import NotificationManager
from flight_data import FlightData

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# pprint(sheet_data)

ORIGIN_CITY_IATA = "BOS"

today = datetime.now()
tomorrow = (today + timedelta(days=1)).strftime("%d/%m/%Y")
six_months = (today + relativedelta(months=+6)).strftime("%d/%m/%Y")
stops = 1
for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months
    )
    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        print("found lower price")
        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}"
        if flight.stop_overs > 0:
            message +=  f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city} city."
        print(message)
        notification_manager.send_sms(message=message)
