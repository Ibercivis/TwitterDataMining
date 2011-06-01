#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import time
import os
import tornado
import tornado.web
import twitter
from RLT.datasources import twitterParser as Parser
from RLT.datasources import fileParser as FileParser
from RLT.interfaces import CLIArgumentParser as Interface
from RLT.processors import ResultsGenerator as Processor

debug=False
if debug: import pprint

class main(Interface, Processor, Parser, FileParser):
    def __init__(self):
        global args
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
                try:
                    if args.get_user_info :
                        table="Users"
                        self.get_user_info(args.user)
                    elif args.user and not args.get_user_info is "True":
                        self.get_by_timeline_array(args.user)
                    if args.hashtag and not args.get_user_info is "True":
                        self.get_by_hashtag(args.hashtag)
                    if args.read_file:
                        self.get_by_file(self.args.read_file)
                except:
                    pass
                self.finished=True
            elif ( time.time() - self.start_time ) > int(self.args.timeout):
                break
            else:
                self.get_by_hashtag(self.args.hashtag)
                time.sleep(30)
                self.get_by_timeline_array(self.args.user)
                time.sleep(30)
        if self.exit: return

        if table is "tweets":
            object_=self.tweets
        else:
            object_=self.users

        return self.process_data(html, object_)

    class RequestHandler(tornado.web.RequestHandler):
        def get(self, slug="MainPage"):
            global args
            content=""
            self.get_arguments_()

            if args.hashtag or args.get_user_info or args.users:
                args.timeout=False
                a.args=args
                a.tweets=[]
                a.users=[]
                a.finished=False
                if slug is not "MainPage":
                    loop=a.loop(True)
                    if slug is not "json":
                        content=loop[0]
                    else:
                        content=loop
            return self.render('Templates/%s' %slug, title=args.title, content=content)

        def get_arguments_(self):
            global args
            global a
            if args.auth: args.auth=args.auth.split(',')
            auth, get_user_info, hashtag, usernames = (False, False, False, False)

            try: auth=self.get_argument('auth')
            except: pass
            try: get_user_info=self.get_argument('get_user_info')
            except: pass
            try: hashtag=self.get_argument('hashtags').split(',')
            except: pass
            try: usernames=self.get_argument('usernames').split(',')
            except: pass

            if auth: args.auth=auth
            if get_user_info: args.get_user_info=get_user_info
            if hashtag: args.hashtag=hashtag
            if usernames: args.usernames=usernames


if __name__ == "__main__":
    global a
    a=main()
    try: a.api = twitter.Api(consumer_key=args.auth[0], consumer_secret=args.auth[0], access_token_key=args.auth[1], access_token_secret=args.auth[2])
    except:
        try:
            from RLT.authentication import TwitterOauth as Api
            a.api=Api().get_api()
        except Exception, e:
            print e
            a.api=twitter.Api()

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
