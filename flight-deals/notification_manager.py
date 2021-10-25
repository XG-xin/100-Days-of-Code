from twilio.rest import Client
import os
from flight_data import FlightData

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

class NotificationManager(FlightData):
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=os.environ['SENDER_NUMBER'],
            to=os.environ['RECEIVER_NUMBER']
        )

        print(message.sid)