#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import twitter
import codecs
import argparse
import tornado
import tornado.web
debug=False
if debug: import pprint


"""
    Class file for TwitterAnalizer got from RealTimeTwitter.
"""

class ArgumentParser(object):
    def parse(self):
        self.parser = argparse.ArgumentParser(description='Search a number of tweets by user\'s timeline or hashtag search, ordered by weight')
        self.parser.add_argument('--user', dest='user', help='user list to search in')
        self.parser.add_argument('--hashtag', dest='hashtag',  help='hashtag list to search in')
        self.parser.add_argument('--server', dest='server',  help='launch server')
        self.parser.add_argument('--destfile', dest='file',  help='hashtag list to search ina')
        self.parser.add_argument('--filter', dest='filter_',  help='filter user-driven search into a specific word')
        self.parser.add_argument('--timeout', dest='timeout',  help='End the bucle after X seconds')
        self.parser.add_argument('--since_id', dest='since_id',  help='Get tweets from this id on.')
        self.parser.add_argument('--get_json', dest='get_json',  help='Return json instead of html')
        self.parser.add_argument('--max_tweets', dest='count',  help='Get COUNT Tweets.')
        self.args = self.parser.parse_args()

class tweetWeightParser(object):
    """
        Gets tweets, filters them and orders them by weight
        Note: for analizer it currently not parses weight...
    """
    def __init__(self):
        self.api = twitter.Api()
        self.tweets=[]

    def second_level_find(self,list_,key):
        for sublist in list_: 
            return sublist[2] == key

    def get_by_timeline_array(self, timelines):
        filter_=self.args.filter_

        for user in timelines:
            if user is None: return
            options={
                'screen_name': user,
                'since_id': self.args.since_id,
                'count': self.args.count,

            }
            print "Getting tweets for user"
            for i in self.api.GetUserTimeline(**options): # TODO Fill options.
                if not i.in_reply_to_user_id and not self.second_level_find(self.tweets, i.text):
                    if i.retweet_count is not 0 and i.retweet_count is not None:
                        if not filter_:
                            self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                        elif filter_ in i.text:
                            self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
            self.tweets=sorted(self.tweets, reverse=True)


    def get_by_hashtag(self, hashtags, geocode=None):
        for hashtag in hashtags:
            if not hashtag: return
            for tweet in self.api.GetSearch(term=hashtag, geocode=geocode):
                if not tweet.in_reply_to_user_id and not self.second_level_find(self.tweets, tweet.text):
                    self.tweets.append([tweet.retweet_count, tweet.created_at, tweet.text, tweet.location] )
            self.tweets=sorted(self.tweets, reverse=True)

class InterchangeableInterface(object):
    """
        Interchangeable user interface, override it to create a new user interface.
    """
    def action_menu(self):
        try: getattr(self, 'menu_' + raw_input("""\n Choose next action \nf) End processing data\np) Print data \nq) Quit\nEnter option: """))()
        except: self.action_menu()
    def warn(self, args): print args
    def menu_f(self): self.finished=True
    def menu_q(self): 
        self.finished=True
        self.exit=True
    def menu_p(self):
        print "printed"
        self.menu_quit()
    def show_data(self, tweets):
        for tweet in tweets:
            print tweet

class ResultsGenerator(object):
    """
        Generates result both in html, txt and prints (if debug enabled) output to console.
        override it for generating your own results.
    """
    def get_filename(self):
        if self.args.file: return self.args.file
        try:
            return ('_').join(self.args.hashtag) + "_" + ('_').join(self.args.user)
        except:
            return "Undefined"

    def process_data(self, stat=False):
        if stat:
            return self.write_html(stat)
        with open(self.get_filename(), 'w') as file:
            file.write(self.tweets.__str__())
        if debug: pprint.PrettyPrinter().pprint(self.tweets)
        return self.write_html(stat)

    def write_html(self, stat=False):
        a="<html><head><title>Real life tweeting</title><link media=\"all\" href=\"static/stickers.css\" type=\"text/css\" rel=\"stylesheet\" /></head><body><table class='sample'><tbody>"
        j=0
        for i in [tuple(self.tweets[i:i+2]) for i in xrange(0,len(self.tweets),2)]:
            if j == 6: 
                a+="</tbody></table><table class='sample'><tbody>"
                j=0
            j=j+1
            pri=i[0][2]
            sec=""
            if len(i) != 1: sec=i[1][2]
            a+="<tr><td><p>%s</p></td><td><p>%s</p></td></tr>" %(pri, sec)
        a+="</tbody></table></body>"

        if self.args.get_json:
            return self.tweets.__str__()
        if stat:
            return a

        with codecs.open(self.get_filename() + '.html','w','utf-8') as page_:
            page_.write(a.encode('ascii','ignore'))
