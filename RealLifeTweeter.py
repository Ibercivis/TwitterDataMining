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

    def loop(self, html=False, table="tweets"):
        while not self.finished:
            if not args.timeout:
                print args.get_user_info
                if "True" in args.get_user_info :
                    table="Users"
                    self.get_user_info(args.user)
                elif args.user and not args.get_user_info is "True":
                    self.get_by_timeline_array(args.user)
                if args.hashtag and not args.get_user_info is "True":
                    self.get_by_hashtag(args.hashtag)
                if args.read_file:
                    self.get_by_file(self.args.read_file)

                self.finished=True
            elif ( time.time() - self.start_time ) > int(self.args.timeout):
                break
            else:
                self.get_by_hashtag(self.args.hashtag)
                time.sleep(30)
                self.get_by_timeline_array(self.args.user)
                time.sleep(30)
        if self.exit: return
        return self.process_data(html, table)

    class RequestHandler(tornado.web.RequestHandler):
        def get(self, slug="MainPage"):
            """
                TODO: Implement OAUTH
            """
            global args
            content=""

            try:
                if not args.auth: 
                    args.auth=self.get_argument('auth')
                else:
                    a.auth=args.auth.split(',') 
                    a.api = twitter.Api(consumer_secret=a.auth[0], access_token_key=a.auth[1], access_token_secret=a.auth[2])
            except Exception, e:
                print "Ey, could not auth myself! %s" %e
                pass

            try:
                if not args.get_user_info: args.get_user_info=self.get_argument('get_user_info')
            except Exception, e:
                print e
                pass
            try:
                if len(args.hashtag) > 0: args.hashtag=self.get_argument('hashtags').split(',')
            except:
                pass
            try:
                if len(args.user) > 0: args.user=self.get_argument('usernames').split(',')
            except:
                pass

            if args.hashtag or args.get_user_info or args.users:
                args.timeout=False
                a.args=args
                a.tweets=[]
                a.users=[]
                a.finished=False
                if slug is not "MainPage":
                    content=a.loop(True)
            return self.render('Templates/%s' %slug, content=content)

if __name__ == "__main__":
    global a
    a=main()
    if a.args.server:
        urls=[
                ("/([^/]+)", a.RequestHandler),
                ("/", a.RequestHandler)
                ] 
        settings={ "static_path": os.path.join(os.path.dirname(__file__), "static"), }
        application = tornado.web.Application(urls, **settings)
        application.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    else:
        a.loop()
