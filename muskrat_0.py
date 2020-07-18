#author: Jake Gaughan @falsejenga
import tweepy #https://github.com/tweepy/tweepy
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import time
import urllib.request
import csv
from process_financials import *


#setting up Tweepy authentication with the Twitter API
auth = tweepy.OAuthHandler("API Key", "API Key")
auth.set_access_token("API Key", "API Key")

api = tweepy.API(auth)
all_data = []
new_line = []

def grab_old_tweets(username):
    #some code and inspiration taken from https://gist.github.com/yanofsky/5436496
    #for all of the tweets
    alltweets = []
    #most recent tweets
    new_tweets = api.user_timeline(screen_name = username,count=200)
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = username,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")

    #transform the tweepy tweets into a 2D array that will populate the csv
    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    #iterating through all of the user's tweets to keep grabbing from further back
    with open('old_user_tweets.csv' , 'w' , newline = '') as file:
         writer = csv.writer(file)
         writer.writerow(["Text", "Time", "@", "ID", "PAT", "BTC_AT", "P20", "BTC_20", "URL", "Ticker"])
         for tweet in alltweets:
            now = False
            new_line = []
            print("==========================")
            new_line.append(tweet.text)
            new_line.append(tweet.created_at)
            new_line.append(tweet.user.screen_name)
            new_line.append(tweet.id_str)
            get_financials("TWTR", new_line, now)
            writer.writerow(new_line)


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
    myStream.filter(follow=['4919167088'], is_async=True)

if __name__ == "__main__":
    #writing to csv
    #monitoring('twitter')
    grab_old_tweets("jack")
