#!/usr/bin/env python3

import sqlite3
import time


class Schema:
    def __init__(self, filepath):
        self.connection = sqlite3.connect(filepath, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()

    ############################
    ####    CREATE TABLE    ####
    ############################

    def create_table_users(self):
        try:
            self.cursor.execute(
                '''CREATE TABLE users(
                    user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    username        VARCHAR,
                    password        VARCHAR
                );'''
            )
            return True
        except:
            return False

    def create_table_tweets(self):
        try:
            self.cursor.execute(
                '''CREATE TABLE tweets(
                    twt_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       FLOAT,
                    twt_content     VARCHAR,
                    user_id         INTEGER,
                    type            VARCHAR,
                    retwt_count     INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                );'''
            )
            return True
        except:
            return False

    def create_table_retweets(self):
        try:
            self.cursor.execute(
                '''CREATE TABLE retweets(
                    retwt_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       FLOAT,
                    twt_content     VARCHAR,
                    user_id         INTEGER,
                    type            VARCHAR,
                    twt_id          INTEGER,
                        FOREIGN KEY (twt_id) REFERENCES tweets(twt_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                );'''
            )
            return True
        except:
            return False

    ################################
    ####    MANIPULATE TABLE    ####
    ################################
    def add_column(self, table_name, column_name, column_type):
        try:
            sql = ''' ALTER TABLE "{0}"
                        ADD COLUMN "{1}" "{2}"
                    ;'''.format(table_name, column_name, column_type)
            self.cursor.execute(sql)
            return True
        except:
            return False

    def delete_table(self, tablename):
        try:
            self.cursor.execute(
                '''DROP TABLE IF EXISTS "{0}";'''.format(tablename)
            )
            return True
        except:
            return False

    ##################################
    ####    CHECKING & UTILITIES  ####
    ##################################

    def confirm_user(self, username, password):
        self.cursor.execute(
            '''SELECT *
            FROM users
            WHERE username = "{0}"
            AND password = "{1}";'''.format(username, password)
        )
        user = self.cursor.fetchall()
        if len(user) == 1:
            return True
        return False

    def check_username_exists(self, username):
        self.cursor.execute(
            '''SELECT *
            FROM users
            WHERE username = "{0}";'''.format(username)
        )
        user = self.cursor.fetchall()
        if len(user) == 1:
            return True
        return False

    ##############################
    ####    INSERT ENTRIES    ####
    ##############################

    def insert_user(self, username, password):
        try:
            self.cursor.execute(
                '''INSERT INTO users(
                    username, password
                ) VALUES (?,?);''', (username, password)
            )
            return True
        except:
            return False

    def insert_tweet(self, twt_content, user_id):
        try:
            self.cursor.execute(
                '''INSERT INTO tweets(
                    twt_content, retwt_count, timestamp, user_id, type
                ) VALUES (?,?,?,?,?);''',
                (twt_content, 0, time.time(), user_id, 'brief')
            )
            return True
        except:
            return False

    def insert_retweet(self, twt_id, user_id):
        try:
            twt_content = self.get_tweet_content(twt_id)
            self.cursor.execute(
                '''INSERT INTO retweets(
                    twt_content, timestamp, twt_id, user_id, type
                ) VALUES (?,?,?,?,?);''',
                (twt_content, time.time(), twt_id, user_id, 'rebrief')
            )
            retwt_count = self.get_retwt_count(twt_id)
            new_retwt_count = retwt_count + 1
            self.cursor.execute(
                '''UPDATE tweets
                SET retwt_count = ?
                WHERE twt_id = ?;''', (new_retwt_count, twt_id)
            )
            # TODO find why retwt_count is not incrementing
            #self.update_retwt_count(twt_id, user_id)
            return True
        except:
            return False

    # FIXME NOT USED CURRENTLY
    def update_retwt_count(self, twt_id, user_id):
        ''' Internal function used when retweeted'''
        try:
            retwt_count = self.get_retwt_count(twt_id)
            print('count: ', retwt_count)
            retwt_count += 1
            print('count+1', retwt_count)
            self.cursor.execute(
                '''UPDATE tweets
                SET retwt_count = ?
                WHERE twt_id = ?
                AND user_id = ?;''', (retwt_count, twt_id, user_id)
            )
            return True
        except:
            return False

    ########################
    ####    GET ITEMS   ####
    ########################
    def get_tweet_content(self, twt_id):
        self.cursor.execute(
            '''SELECT twt_content
            FROM tweets
            WHERE twt_id = {0};'''.format(twt_id)
        )
        twt_content = self.cursor.fetchone()[0]
        return twt_content

    def get_retwt_count(self, twt_id):
        self.cursor.execute(
            '''SELECT retwt_count
            FROM tweets
            WHERE twt_id = {0};'''.format(twt_id)
        )
        retwt_count = self.cursor.fetchone()[0]
        print('retweeted: ', retwt_count)
        return retwt_count

    def get_user_id(self, username):
        self.cursor.execute(
            '''SELECT user_id
            FROM users
            WHERE username = "{0}";'''.format(username)
        )
        user_id = self.cursor.fetchone()[0]
        return user_id

    def get_username(self, user_id):
        self.cursor.execute(
            '''SELECT username
            FROM users
            WHERE user_id = "{0}";'''.format(user_id)
        )
        username = self.cursor.fetchone()[0]
        return username

    def get_user(self, username):
        self.cursor.execute(
            '''SELECT *
            FROM users
            WHERE username = "{0}";'''.format(username)
        )
        user = self.cursor.fetchall()[0]
        return user

    def get_all_tweets(self):
        self.cursor.execute(
            '''SELECT *
            FROM tweets;'''
        )
        tweets = self.cursor.fetchall()
        return tweets

    def get_all_retweets(self):
        self.cursor.execute(
            '''SELECT *
            FROM retweets;'''
        )
        retweets = self.cursor.fetchall()
        return retweets

    def get_user_tweets(self, user_id):
        self.cursor.execute(
            '''SELECT *
            FROM tweets
            WHERE user_id = "{0}";'''.format(user_id)
        )
        tweets = self.cursor.fetchall()
        return tweets

    def get_user_retweets(self, user_id):
        self.cursor.execute(
            '''SELECT *
            FROM retweets
            WHERE user_id = "{0}";'''.format(user_id)
        )
        retweets = self.cursor.fetchall()
        return retweets
