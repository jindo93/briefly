#!/usr/bin/env python3

import time
from .mapper import Schema

filepath = 'src/datafiles/database.db'


class User:

    def __init__(self):
        self.user_id = 0
        self.username = ""
        self.password = ""
        self.tweets = []

    def login(self, username, password):
        with Schema(filepath) as db:
            return db.confirm_user(username, password)

    # TODO
    def initialize(self, username):
        with Schema(filepath) as db:
            user = db.get_user(username)
            self.user_id = user[0]
            self.username = user[1]
            self.password = user[2]
            self.tweets = self.get_all_user_tweets(user[0])

    def signup(self, username, password):
        with Schema(filepath) as db:
            return db.insert_user(username, password)

    def check_username_exists(self, username):
        with Schema(filepath) as db:
            return db.check_username_exists(username)

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
        ''' Function used internally to get usernames of each tweet '''
        username_lst = []
        with Schema(filepath) as db:
            for item in arr:
                username_lst.append(db.get_username(item[3]))
        return username_lst

    def get_all_user_tweets(self, user_id):
        with Schema(filepath) as db:
            tweets = db.get_user_tweets(user_id)
            retweets = db.get_user_retweets(user_id)
        all_tweets = tweets + retweets
        sorted_tweets = sorted(all_tweets, key=self.getKey, reverse=True)
        time_arr = self.get_time(sorted_tweets)
        usernames = self.get_username_from_user_id(sorted_tweets)

        for i in range(len(sorted_tweets)):
            sorted_tweets[i] = sorted_tweets[i]+time_arr[i] + (usernames[i],)

        print(sorted_tweets)
        return sorted_tweets

    def tweet(self, twt_content):
        with Schema(filepath) as db:
            return db.insert_tweet(twt_content, self.user_id)

    def retweet(self, twt_id):
        with Schema(filepath) as db:
            return db.insert_retweet(twt_id, self.user_id)
