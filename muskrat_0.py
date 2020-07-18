#author: Jake Gaughan @falsejenga
import tweepy
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import time
import urllib.request


#setting up Tweepy authentication with the Twitter API
auth = tweepy.OAuthHandler("API Keys", "API Keys")
auth.set_access_token("API Keys", "API Keys")

api = tweepy.API(auth)
all_data = []
new_line = []

def grab_old_tweets(username):
    #some code and inspiration taken from https://gist.github.com/yanofsky/5436496
    #for all of the tweets
    all_tweets = []
    #most recent tweets
    new_tweets = api.user_timeline(screen_name = username,count=200)
    all_tweets.extend(new_tweets)
    #iterating through all of the user's tweets to keep grabbing from further back
    for tweet in new_tweets:
        now = False
        new_line = []
        print("==========================")
        new_line.append(tweet.text)
        new_line.append(tweet.created_at)
        get_financials("TSLA", new_line, now)

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
    get_bitcoin(save_array)
    print("--------")

    #1200 seconds is 20 minutes
    #for testing purposes it is set to 1 seconds
    if now:
        time.sleep(1)

    #new parameters for financial queries
    end = end + dt.timedelta(seconds=20)
    print(end)

    #grabbing the current price of the stock
    df = web.DataReader(ticker, 'yahoo', start, end)
    df1 = df["Close"]

    save_array.append(df1[1])
    print("20 minutes later:")
    print(ticker + " stock price 20 minutes after tweet: " + str(save_array[6]))
    get_bitcoin(save_array)
    #formatting the tweet url to result in a quote tweet for the sent out tweet
    tweet_url = "https://twitter.com/" + save_array[2] + "/status/" + save_array[3]
    save_array.append(tweet_url)
    save_array.append(ticker)
    #print(save_array)
    rt_with_comment(save_array)


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
    url = "unique url from Nomics API with api key inside"
    #snatching big chunk of info
    BTC_info = urllib.request.urlopen(url).read()
    #grabbing just the current price
    BTC_price = str(BTC_info[163:176],'utf-8')
    save_array.append(BTC_price)
    print("BTC: " + str(BTC_price))


#Stream listener watching all new tweets coming in given certain parameters
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        now = True
        print("==========================")
        #tossing da data into the array
        new_line.append(status.text)
        new_line.append(status.created_at)
        new_line.append(status.user.screen_name)
        new_line.append(status.id_str)
        #print(status.id_str)
        get_financials("TWTR", new_line, now)

        #da big master array for all data
        all_data.append(new_line)


    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False


def monitoring(tracking):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    #IDs:
    #Elon Musk: 44196397
    #Jack: 12
    #myStream.filter(follow=['']) (follow is for following specific accounts)
    myStream.filter(follow=['12'], is_async=True)

if __name__ == "__main__":
    #writing to csv
    monitoring('twitter')
    #grab_old_tweets("elonmusk")
