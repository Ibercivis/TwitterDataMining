#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
from RLT import *
import time
import os
class main(twitterParser, InterchangeableInterface, ResultsGenerator, ArgumentParser):
    def __init__(self):
        global args
        self.OAUTH_APP_SETTINGS = {
            'twitter': {
                'consumer_key': '',
                'consumer_secret': '',
                'request_token_url': 'https://twitter.com/oauth/request_token',
                'access_token_url': 'https://twitter.com/oauth/access_token',
                'user_auth_url': 'http://twitter.com/oauth/authorize',
                'default_api_prefix': 'http://twitter.com',
                'default_api_suffix': '.json',
            },
        }
        super(self.__class__, self).__init__()
        self.finished=False
        self.exit=False
        self.start_time=time.time()
        self.parse()

        args=self.args

        if not type(self.args.hashtag) is list: self.args.hashtag=[self.args.hashtag]
        if not type(self.args.user) is list: self.args.user=[self.args.user]

    def loop(self, html=False):
        while not self.finished:
            if not self.args.timeout:
                if self.args.hashtag and not self.args.get_user_info:
                    self.get_by_hashtag(self.args.hashtag)
                if self.args.user and not self.args.get_user_info:
                    self.get_by_timeline_array(self.args.user)
                if self.args.get_user_info:
                    self.get_user_info(self.args.user)
                if self.args.read_file:
                    self.get_by_file(self.args.read_file)
                self.finished=True
            elif ( time.time() - self.start_time ) > int(self.args.timeout):
                break
            else:
                self.get_by_hashtag(self.args.hashtag)
                time.sleep(10)
                self.get_by_timeline_array(self.args.user)
                time.sleep(10)
        if self.exit: return
        return self.process_data(html)

    class RequestHandler(tornado.web.RequestHandler):
        def get(self, slug=False):
            """
                TODO: Implement limits as twitter limits it!!!!
            """
            global args

            try:
                args.auth=self.get_argument('auth')
                if args.auth:
                    a.auth=args.auth.split(',') 
                    a.api = twitter.Api(consumer_secret=self.auth[0], access_token_key=self.auth[1], access_token_secret=self.auth[2])
            except:
                print "Ey, could not auth myself!"
                pass


            try:
                args.hashtag=self.get_argument('hashtags').split(',')
            except:
                pass
            try:
                args.user=self.get_argument('usernames').split(',')
            except:
                pass

            if args.hashtag or args.users:
                args.timeout=False
                a.args=args
                a.tweets=[]
                a.users=[]
                a.finished=False
                self.write(a.loop(True))
                return

            self.render('Templates/Starting', args=args)

if __name__ == "__main__":
    global a
    a=main()
    if a.args.server:
        urls=[("/", a.RequestHandler)]
        print "Rendering urls for %s" %urls
        settings={ "static_path": os.path.join(os.path.dirname(__file__), "static"), }
        application = tornado.web.Application(urls, **settings)
        application.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    else:
        a.loop()
