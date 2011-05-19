#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import twitter
import codecs
debug=False
if debug: import pprint


"""
    Class file for RealTimeTwitter
"""

class tweetWeightParser(object):
    """
        Gets tweets, filters them and orders them by weight
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
            for i in self.api.GetUserTimeline(user):
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
        return ('_').join(self.args.hashtag) + "_" + ('_').join(self.args.user)

    def process_data(self):
        with open(self.get_filename(), 'w') as file:
            file.write(self.tweets.__str__())
        if debug: pprint.PrettyPrinter().pprint(self.tweets)
        return self.write_html()

    def write_html(self):
        a="<html><head><title>Real life tweeting</title><link media=\"all\" href=\"stickers.css\" type=\"text/css\" rel=\"stylesheet\" /></head><body><table class='sample'><tbody>"
        for i in [tuple(self.tweets[i:i+2]) for i in xrange(0,len(self.tweets),2)]:
            pri=i[0][2]
            sec=""
            if len(i) != 1: sec=i[1][2]
            a+="<tr><td><p>%s</p></td><td><p>%s</p></td></tr>" %(pri, sec)
        a+="</tbody></table></body>"

        with codecs.open(self.get_filename() + '.html','w','utf-8') as page_:
            page_.write(a.encode('ascii','ignore'))
