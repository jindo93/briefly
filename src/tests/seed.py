#!/usr/bin/env python3

import time
from ..models.mapper import Schema

if __name__ == '__main__':
    with Schema('src/datafiles/database.db') as db:
        if db.insert_user('jebsi', '0000'):
            db.insert_user('jd', '0000')
            db.insert_user('erving', '0000')
            print('Success: <insert_user>')
        else:
            print('Error: <insert_user>')

        msg1 = 'I have a dream'
        msg2 = 'BangBang'
        msg3 = 'Rule the dark web'
        if db.insert_tweet(msg1, 1):
            db.insert_tweet(msg2, 2)
            db.insert_tweet(msg3, 3)
            print('Success: <insert_tweet>')
        else:
            print('Error: <insert_tweet>')

        if db.insert_retweet(1, 1):
            db.insert_retweet(1, 2)
            # time.sleep(2)
            db.insert_retweet(1, 3)
            # time.sleep(1)
            db.insert_retweet(2, 1)
            print('Success: <insert_retweet>')
        else:
            print('Error: <insert_retweet>')
