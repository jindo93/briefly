#!/usr/bin/env python3

import time
from .mapper import Schema

filepath = 'src/datafiles/database.db'


class Public:
    def __init__(self):
        self.tweets = []

    def initialize(self):
        self.tweets = self.get_all_tweets()

    @staticmethod
    def getKey(arr):
        return arr[1]

    @staticmethod
    def get_time(arr):
        time_arr = []
        for item in arr:
            time_arr.append(time.localtime(item[1]))
        return time_arr

    def get_username_from_user_id(self, arr):
        username_lst = []
        with Schema(filepath) as db:
            for item in arr:
                username_lst.append(db.get_username(item[3]))
        return username_lst

    def get_all_tweets(self):
        with Schema(filepath) as db:
            tweets = db.get_all_tweets()
            retweets = db.get_all_retweets()
        all_tweets = tweets + retweets
        sorted_tweets = sorted(all_tweets, key=self.getKey, reverse=True)
        time_arr = self.get_time(sorted_tweets)
        usernames = self.get_username_from_user_id(sorted_tweets)

        for i in range(len(sorted_tweets)):
            sorted_tweets[i] = sorted_tweets[i]+time_arr[i]+(usernames[i],)
        return sorted_tweets
