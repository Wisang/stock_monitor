import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "BSBEGAP9CKNT713L"
NEWS_API_KEY = "e9c1830ec1fb4d2a9238085d07bc7008"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

parameters_news = {
    "q": COMPANY_NAME,
    "from": "2022-02-17",
    "sortBy": "popularity",
    "apikey": NEWS_API_KEY,
}

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
print(data_list)

price_list = [item["4. close"] for item in data_list]
print(price_list)


today_price = float(price_list[0])
yesterday_price = float(price_list[1])

price_diff = abs(today_price - yesterday_price)
price_diff_percent = int(price_diff / today_price * 100)

if True:  # price_diff_percent >= 5:
    print("get news")


# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
response = requests.get(NEWS_ENDPOINT, params=parameters_news)

articles = response.json()['articles']
news = [f"{STOCK_NAME}: 🔺{price_diff_percent*100}%\n"\
        f"Headline: {item['title']}\n"\
        f"Brief: {item['description']}\n"
        for item in articles]
top3_news = news[:3]

print(top3_news)

account_sid = "AC5d5d1d3bed511b084991b20279367956"
auth_token = "bf1a4bbc9aec73990980c06f096e76a1"

if True:  # need_to_bring_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=top3_news,
        from_='+18596952590',
        to='+821023309854'
    )
    print(message.status)

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
