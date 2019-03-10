#!/usr/bin/env python3

from ..models.mapper import Schema

if __name__ == '__main__':
    with Schema('src/datafiles/database.db') as db:
        if db.delete_table('users'):
            print('Success: deleted <users> table')
        else:
            print('Error: <users> table')

        if db.delete_table('tweets'):
            print('Success: deleted <tweets> table')
        else:
            print('Error: <tweets> table')

        if db.delete_table('retweets'):
            print('Success: deleted <retweet> table')
        else:
            print('Error: <retweets> table')
