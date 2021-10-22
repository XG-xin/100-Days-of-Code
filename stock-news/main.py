import requests
import datetime
from pandas.tseries.offsets import BDay
import html
from twilio.rest import Client
import re

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = <news_api_key>
STOCK_API_KEY = <alphavantage_api_key>

# today = datetime.date.today()
today = datetime.date.today()
offset = max(1, (today.weekday() + 6) % 7 - 3)
timedelta = datetime.timedelta(offset)
yesterday = today - timedelta

offset_2 = max(1, (yesterday.weekday() + 6) % 7 - 3)
timedelta_2 = datetime.timedelta(offset_2)
before_yesterday = yesterday - timedelta_2

print(yesterday)
print(before_yesterday)


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
close_price_yesterday = float(response.json()["Time Series (Daily)"][f"{yesterday}"]["4. close"])
close_price_before_yesterday = float(response.json()["Time Series (Daily)"][f"{before_yesterday}"]["4. close"])

price_difference = close_price_yesterday - close_price_before_yesterday
change_percentage = round(abs(price_difference) / close_price_yesterday * 100)
# print(price_difference)
# print(change_percentage)
if price_difference >= 0:
    header_text = f"{STOCK}: 🔺{change_percentage}%"
else:
    header_text = f"{STOCK}: 🔻{change_percentage}%"

if change_percentage > 2:
    news_parameters = {
        "q": COMPANY_NAME,
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    article_slice = response.json()["articles"][:3]


    news_title = [re.sub('<[^<]+?>', '', article["title"]) for article in article_slice]
    news_body = [re.sub('<[^<]+?>', '', article["description"]) for article in article_slice]
    # print(news_title)
    # print(news_body)

    # Send a separate message with each article's title and description to your phone number.
    account_sid = <twilio_id>
    auth_token = <twilio_auto_token>
    client = Client(account_sid, auth_token)

    for i in range(3):
        message = client.messages \
            .create(
            body=f"{header_text} \nHeadline: {news_title[i]} \nBrief: {news_body[i]}",
            from_=<sender>,
            to=<receiver>'
        )

    print(message.sid)

