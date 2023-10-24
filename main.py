import requests
import datetime

BTC_stock_url = "https://www.alphavantage.co/query"
#Get BTC Stock price percentage
stock_parameter = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "CNY",
    "apikey": "YOUR API KEY"
}

response_stock = requests.get(BTC_stock_url, params=stock_parameter)
response_stock.raise_for_status()
stock_data = response_stock.json()
#
yesterday_date = str(datetime.datetime.today().date() - datetime.timedelta(days=1))
two_days_ago_date = str(datetime.datetime.today().date() - datetime.timedelta(days=2))

yesterday_price = float(stock_data["Time Series (Digital Currency Daily)"][yesterday_date]["4b. close (USD)"])
two_days_ago_price = float(stock_data["Time Series (Digital Currency Daily)"][two_days_ago_date]["4b. close (USD)"])
persentage_stock = float("{:.2f}".format((yesterday_price - two_days_ago_price)/yesterday_price * 100))

if abs(persentage_stock) > 5:
    # get news about BTC
    BTC_news_url = "https://newsapi.org/v2/everything"
    news_parameter = {
        "q": "bitcoin",
        "apikey": "YOUR API KEY",
        "sortBy": "publishedAt"
    }
    response_news = requests.get(BTC_news_url, params=news_parameter)
    response_news.raise_for_status()
    stock_news = response_news.json()
    today_article = " ".join(
        [f"\nDates: {news['publishedAt'].replace('T', ' ').replace('Z', ' ')}\nHeadline: {news['title']}\nlink: {news['url']}\n" for news in
         stock_news["articles"][0:5]])
    BTC_percentage = f"🔻{abs(persentage_stock)}" if persentage_stock < 0 else f"🔺{abs(persentage_stock)}"
    print(today_article)

    # send sms via twilo
    from twilio.rest import Client

    account_sid = 'YOUR SID ACCOUNT'
    auth_token = 'YOUR ACCOUNT TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      from_='TWILIO NUMBER',
      body=f"\nBTC: {BTC_percentage}%\n{today_article}",
      to='NUMBER YOU WANT TO SEND TO'
    )
    print(str(len(f"\nBTC: {BTC_percentage}%\n{today_article}")) + " Character")
    print(message.sid)
