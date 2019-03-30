# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 22:33:29 2019

@author: jssme
"""

import tweepy
import json
import emoji
import csv
#import re

class API:
    def __init__(self):
        self.consumer_key       = '---'
        self.consumer_secret    = '---'
        self.access_key         = '---'
        self.access_secret      = '---'
         
 		## selected account for testing
# 		self.user = ["katyperry", "ConanOBrien", "Oprah", "jimmyfallon", "EmmaWatson", "LeoDiCaprio", "BillGates", "taylorswift13", "rihanna"]
# 		self.comm = ["Padilla_Comm", "MayoClinic", "TheEconomist", "Google", "nytimes"]
    def getApi(self):
        try: 
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_key, self.access_secret)
            api = tweepy.API(auth)
        except:
            print('Error: Authentication failed')
        return api
     
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if 'created_at' in data:
#            row = tweet['id_str'] + "\t" + tweet['created_at'] + "\t" + tweet['user']['screen_name'] + "," + tweet['text']
#            print("------------------------------")
#            print(emoji.demojize(row))
#            print(row.encode("utf-8"))
#            print("******************************")
#            print("******************************")
            # Open/Create a file to append data
#            csvFile = open('raw_twitter.csv', 'a')
#            csvFile.write(row) 
            
            # Open/Create a file to append data
            csvFile = open('raw-twitter2.csv', 'a', newline='', encoding='utf-8')
            #Use csv Writer
            csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL, delimiter='\t')
            
            hashtag = ''
            for x in range(len(tweet['entities']['hashtags'])):
#                print(str(x) + '********' + tweet['entities']['hashtags'][x]['text'])
                if x == 0:
                    hashtag = tweet['entities']['hashtags'][x]['text']
                else:
                    hashtag = hashtag + ',' + tweet['entities']['hashtags'][x]['text']
                
            row = [tweet['id_str'],tweet['created_at'],tweet['user']['screen_name'],hashtag,emoji.demojize(tweet['text']).replace('\n', ' ')]
            print(row)
            csvWriter.writerow(row)
#        return True

    def on_error(self, status):
        print(status, self)
##        self.csvFile.close()        

## main function
x = API()
api = x.getApi()
#This handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
stream = tweepy.Stream(api.auth, l)

#This line filter Twitter Streams to capture data with the english language and keyword python
#    stream.filter(track=['python'], languages=['en'])
stream.sample() # Everything