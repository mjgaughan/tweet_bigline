import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import time

#financial information based on the timeframe for a given tweet
def get_financials(ticker, save_array, now):
    style.use('ggplot')

    #NOTE: Trading hours are M-F 14:30-17:00 UTC (way to lazy to switch into EST)
    #setting parameters for financial query
    end = save_array[1]
    start = end - dt.timedelta(days=2)

    #grabbing current price of given stock
    df = web.DataReader(ticker, 'yahoo', start, end)
    df1 = df["Close"]
    #saving price to array
    save_array.append(df1[1])

    print(save_array[0])
    print("--------")
    print("Current time: " + str(save_array[1]))
    print(ticker + " stock price at the time of tweet: " + str(save_array[4]))
    #grabbing current BTC price
    if now:
        get_bitcoin(save_array)
    else:
        save_array.append("N/A")
    print("--------")

    #1200 seconds is 20 minutes
    #for testing purposes it is set to 1 seconds
    if now:
        time.sleep(1)

    #new parameters for financial queries
    end = end + dt.timedelta(minutes=20)
    print(end)

    #grabbing the current price of the stock
    df = web.DataReader(ticker, 'yahoo', start, end)
    df1 = df["Close"]

    save_array.append(df1[1])
    print("20 minutes later:")
    print(ticker + " stock price 20 minutes after tweet: " + str(save_array[6]))
    if now:
        get_bitcoin(save_array)
    else:
        save_array.append("N/A")
    #formatting the tweet url to result in a quote tweet for the sent out tweet
    tweet_url = "https://twitter.com/" + save_array[2] + "/status/" + save_array[3]
    save_array.append(tweet_url)
    save_array.append(ticker)
    #print(save_array)
    #rt_with_comment(save_array)


def rt_with_comment(save_array):
    tweet_release = (save_array[9] + " stock price at the time of tweet: " + str(save_array[4]) + "\n" +
                        "BTC at time of tweet: " + str(save_array[5]) + "\n" +
                        "----20 minutes later ----" + "\n" +
                        save_array[9] + " stock price 20 minutes after tweet: " + str(save_array[6]) + "\n" +
                        "BTC 20 minutes after tweet: " + str(save_array[7]) + "\n" +
                        save_array[8])
    api.update_status(tweet_release)
    #print("hi")

#getting current bitcoin price from Nomics API
def get_bitcoin(save_array):
    url = "unique Nomics API url goes here"
    #snatching big chunk of info
    BTC_info = urllib.request.urlopen(url).read()
    #grabbing just the current price
    BTC_price = str(BTC_info[163:176],'utf-8')
    save_array.append(BTC_price)
    print("BTC: " + str(BTC_price))
