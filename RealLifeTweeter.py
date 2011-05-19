#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import argparse
import time 
from RLT import *
import time
class main(tweetWeightParser, InterchangeableInterface, ResultsGenerator):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.parser = argparse.ArgumentParser(description='Search a number of tweets by user\'s timeline or hashtag search, ordered by weight')
        self.parser.add_argument('--user', dest='user', help='user list to search in')
        self.parser.add_argument('--hashtag', dest='hashtag',  help='hashtag list to search in')
        self.parser.add_argument('--destfile', dest='file',  help='hashtag list to search ina')
        self.parser.add_argument('--filter', dest='filter_',  help='filter user-driven search into a specific word')
        self.parser.add_argument('--timeout', dest='timeout',  help='End the bucle after X seconds')
        self.args = self.parser.parse_args()
        self.finished=False
        self.exit=False
        self.warn("Processing your petitions, press ctrl+C to stop anytime")
        if not type(self.args.hashtag) is list: self.args.hashtag=[self.args.hashtag]
        if not type(self.args.user) is list: self.args.user=[self.args.user]
        self.start_time=time.time()
        while not self.finished:
            spent_time=int(time.time() - self.start_time)
            if self.args.timeout and ( time.time() - self.start_time ) > int(self.args.timeout) : break

            try:
                self.get_by_hashtag(self.args.hashtag)
                time.sleep(10)
                self.get_by_timeline_array(self.args.user)
                time.sleep(10)
            except KeyboardInterrupt:
                self.show_data(self.tweets)
                self.action_menu()
        if self.exit: return
        html=self.process_data()

a=main()
