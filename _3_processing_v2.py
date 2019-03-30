# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import string
import csv
import time
import datetime
import functools
import operator
import emoji
import re
import nltk
import pandas as pd
from polyglot.detect import Detector

def get_date_time():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
    return st

class preProcess:
    def __init__(self):
        self.hashCol = 3
        self.textCol = 4
        self.csvTweets = 'raw-twitter2.csv'
        self.codec = 'utf-8'
        self.root = ''
        self.process = self.root + ''
        self.nrc_processed = self.root + 'nrc.csv'
        self.cachedStopWords = nltk.corpus.stopwords.words('english')
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.wordList = []
        self.better = {}
        self.noWord = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #lang = detect("Ein, zwei, drei, vier")
    #print lang
    
    def is_english(self, cell):
        try:
    #        print(cell)
    #        print(cell.decode(codec))
            language = Detector(cell).language #.decode(codec)
    #        print(language)
    #        print(cell.decode(codec))
        except:
            return False
    
        if language.name == "English":
            return True
        else:
            return False
    
    ## get NRC word list and associated attributes
    def getValues(self):
        nrc = pd.read_csv(self.nrc_processed, header = None, index_col = False)
        for index, row in nrc.iterrows():
            self.better[row[0]] = row[1:].values.tolist()
            self.wordList.append(row[0])
#            print(self.wordList[index])
        return self.better
    
    def is_no_retweet(self, tweet):
        if tweet[:2] == 'RT':
            return False
        else:
            return True
    
    def is_emoji(self, s):
        count = 0
        for em in emoji.UNICODE_EMOJI:
            count += s.count(em)
            if count > 1:
                return False
        return bool(count)
    
    def getTweetValues(self, text, hashtag):
        em = emoji.emojize(text) #'Hey 👨‍👩‍👧‍👧👨🏿😷😷🇬🇧'
        em_split_emoji = emoji.get_emoji_regexp().split(em)
        em_split_whitespace = [substr.split() for substr in em_split_emoji]
        em_split = functools.reduce(operator.concat, em_split_whitespace)
        tweet = []
        text = ''
        emoticons = ''
        for separated in em_split:
    #        print(separated + ' ||| ' + str(is_emoji(separated)))
            if self.is_emoji(separated):
                emoticons = emoticons + separated
            else:
    #            print(lemmatizer.lemmatize(separated))
                text = text + self.lemmatizer.lemmatize(separated) + ' '
            
        text = re.sub('@[^\s]+','',text)
        text = re.sub(r'http\S+', '', text)
        text = ' '.join([word for word in text.split() if word not in self.cachedStopWords])
        text = text.strip()
        
        for tag in hashtag.split(','):
            text = text.replace('#' + tag, '')
    
        tweet.append(text)
        tweet.append(emoticons)

        attr = []
#        print('-----------TWEET-----------')
#        print(self.wordList[0])
#        for word in self.wordList:
#            print(word)
            
        for word in text.translate(str.maketrans('','',string.punctuation)).split():
#             print(word)            
             if(word in self.wordList):
#                print(self.better[word])
                attr.append(self.better[word])
#                print('xxx')
             else:
                attr.append(self.noWord)
#                print('yyy')
#                print(self.noWord)
                continue
    #        tweet.append([sum(x) for x in zip(*attr)])
#        print('-----------------------------------')
#        tweet.append([sum(x) for x in zip(*attr)])
#        print([sum(x) for x in zip(*attr)])
#        print(zip(attr))
    #    tweet.append([sum(x) for x in zip(*attr)])
        
        tot = 0
        for tw in [sum(x) for x in zip(*attr)]:
            tweet.append(tw)
            tot = tot + tw

        if(tot > 0):
            tweet.append(True)
        else:
            tweet.append(False)   
    #    print(text + '---' + emoticons)
    #    print(tweet[0] + '---' + tweet[1])
#        print(len(tweet))
        return tweet
    
    def open_csv(self):
        with open(self.csvTweets, newline='', encoding=self.codec) as csv_input:
            with open(self.process + self.csvTweets[:-4] + '_clean.csv', 'w', encoding=self.codec) as csvoutput:
                csv_reader = csv.reader(csv_input, delimiter='\t')
                csv_writer = csv.writer(csvoutput, lineterminator='\n')
            #    line_count = sum(1 for row in csv_reader) 
                
                line_count = 0
                new = []
               
                for row in csv_reader:
                    text = row[self.textCol]
                    hashtag = row[self.hashCol]
                    tweet = self.getTweetValues(text, hashtag)
                    
    #                row.append(is_english(tweet[0]))
    #                row.append(is_no_retweet(tweet[0]))
                    if self.is_english(tweet[0]) and self.is_no_retweet(tweet[0]):
    #                    row.append(tweet[0]) #text
    #                    row.append(tweet[1]) #emoji
    #                    row.append(tweet[2]) #NRC word list
                        for tw in tweet:
#                            print(len(tw))
                            row.append(tw)
                        
    #                    row.append([sum(x) for x in zip(*attr)])
    #                    row.append(values[word])
                        if row[17]:
                            new.append(row[:16])
#                        print(row)
                    line_count += 1
    
    #                print(row[4].join([word for word in row[3].split() if word not in cachedStopWords]))
    #                print(emoji.demojize(text))
                
                print("Processed ", line_count, " lines.")
                csv_writer.writerows(new)
    #            pd.DataFrame(tweet).to_csv(self.process + s + ".csv", header = False, index = False)
        
#if __name__ == '__main__':
x = preProcess()
st = get_date_time()
print(st + " START")
x.getValues()
x.open_csv()
et = get_date_time()
print(st + " START")
print(et + " END ")

#open_csv()
#print("TEST2")