#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import argparse
"""
    Class file for TwitterAnalizer got from RealTimeTwitter.
    TODO Things:
        Make nice web interfaces.
        Allow it to connect with twitter (in progress)
        To make a bunch of online IDs to stickers
            Get user lists
            Get followers
            Get followings.
"""

class CLIArgumentParser(object):
    def parse(self):
        self.parser = argparse.ArgumentParser(description='Search a number of tweets by user\'s timeline or hashtag search, ordered by weight')
        # Search options.
        self.parser.add_argument('--user', dest='user', help='user list to search in', default=False)
        self.parser.add_argument('--hashtag', dest='hashtag',  help='hashtag list to search in', default=False )
        self.parser.add_argument('--user_info', dest='get_user_info',  help='return user info instead of tweets', default=False)
        self.parser.add_argument('--filter', dest='filter_',  help='filter user-driven search into a specific word', default=False)
        self.parser.add_argument('--since_id', dest='since_id',  help='Get tweets from this id on.', default=False)
        self.parser.add_argument('--dont_parse_weight', action="store_false", dest='parse_weight',  help='Dont bother about tweet\'s weight. AKA let not-retweeted in right now.', default=False)
        self.parser.add_argument('--max_tweets', dest='count',  help='Get COUNT Tweets.', default=False)
        # Read from file
        self.parser.add_argument('--read_file', dest='read_file',  help='Get tweets from this file in json format.', default=False)
        # Main options
        self.parser.add_argument('--server', dest='server',  action="store_true", help='launch server', default=False)
        self.parser.add_argument('--title', default="Real Life twitter", dest='title',  help='specify title')
        self.parser.add_argument('--timeout', dest='timeout',  help='End the bucle after X seconds', default=False)
        # Auth options
        self.parser.add_argument('--auth', dest='auth',  help='Autentication credentials to use', default=False)
        self.parser.add_argument('--auth_url', dest='auth_url',  help='Autentication url to use', default=False)
        # Data saving
        self.parser.add_argument('--destfile', dest='file',  help='Specify filenamSpecify filename ', default=False)
        self.parser.add_argument('--save_file', dest='save_file',  help='Save in a file')
        self.parser.add_argument('--enable_sqlite', dest='sqlite', action="store_true",  help='Save data in sqlite database. Requires destfile', default=False)
        self.parser.add_argument('--enable_mysql', dest='mysql',  help='Save data in mysql database. Requires info', default=False)
        self.parser.add_argument('--get_json', dest='get_json', action="store_true", help='Return json instead of html', default=False)
        self.args = self.parser.parse_args()
