import requests
from twilio.rest import Client

api_key = <API_KEY>
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = <ACCOUNT_SID>
auth_token = <AUTH_TOKEN>

parameters = {
    "lat": "42.252876",
    "lon": "-71.002274",
    "exclude": "current,minutely,daily",
    "appid": api_key,
}

response = requests.get(url=OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
# print(weather_data)
weather_slice = weather_data["hourly"][:12]
will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today, bring an ☔.",
        from_=<SENDER>,
        to=<RECEIVER>,
    )
    print(message.status)

