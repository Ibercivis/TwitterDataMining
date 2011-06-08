#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import json

class fileParser(object):
    def get_by_file(self, file_):
        with open(file_) as f:
            json.loads(f.read())

    def get_external_usernames(self):
        with open(self.args.external_users) as f:
            return f.read().split(',')

class twitterParser(object):
    """
        Gets tweets, filters them and orders them by weight
        Note: for analizer it currently not parses weight...
    """

    def second_level_find(self,list_,key):
        for sublist in list_: 
            return sublist[2] == key

    def get_user_info(self, users):
        for user in users:
            if not user: return
            try:
                user=self.api.GetUser(user.strip())
                self.users.append( { user.id : [ user.AsDict(), self.api.GetFollowerIDs(user.id) , self.api.GetFriendIDs(user.id) ]} )
            except Exception, e:
                if "Limit" in e:
                    import time
                    print "Exception: %s\nSleeping an hour" %e
                    time.sleep(3600)
                else:
                    print "Exception: %s" %e

    def get_by_timeline_array(self, timelines):
        filter_=self.args.filter_

        for user in timelines:
            if not user: return
            options={
                'screen_name': user,
                'since_id': self.args.since_id,
                'count': self.args.count,
            }
            try:
                for i in self.api.GetUserTimeline(**options): # TODO Fill options.
                    if not self.args.parse_weight:
                        if not self.second_level_find(self.tweets, i.text):
                            if not filter_:
                                self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                            elif filter_ in i.text:
                                self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                    else:
                        if not i.in_reply_to_user_id and not self.second_level_find(self.tweets, i.text):
                            if i.retweet_count is not 0 and i.retweet_count is not None:
                                if not filter_:
                                    self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                                elif filter_ in i.text:
                                    self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                self.tweets=sorted(self.tweets, reverse=True)
            except Exception, e:
                print e

    def get_by_hashtag(self, hashtags, geocode=None):
        for hashtag in hashtags:
            if not hashtag: return
            for tweet in self.api.GetSearch(term=hashtag, geocode=geocode):
                if not tweet.in_reply_to_user_id and not self.second_level_find(self.tweets, tweet.text):
                    self.tweets.append([tweet.retweet_count, tweet.created_at, tweet.text, tweet.location] )
            self.tweets=sorted(self.tweets, reverse=True)
