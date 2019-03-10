#!/usr/bin/env python3

from ..models.mapper import Schema


if __name__ == '__main__':
    with Schema('src/datafiles/database.db') as db:
        if db.create_table_users():
            print('Success: created <users> table')
        else:
            print('Error: <users> table')

        if db.create_table_tweets():
            print('Success: created <tweets> table')
        else:
            print('Error: <tweets> table')

        if db.create_table_retweets():
            print('Success: created <retweet> table')
        else:
            print('Error: <retweets> table')
