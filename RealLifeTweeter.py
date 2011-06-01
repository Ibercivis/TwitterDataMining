#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import time
import os
import tornado
import tornado.httpserver
import tornado.web
import twitter 
from RLT.datasources import twitterParser as Parser
from RLT.datasources import fileParser as FileParser
from RLT.interfaces import CLIArgumentParser as Interface
from RLT.interfaces import TornadoRequestHandler as WebInterface
from RLT.processors import ResultsGenerator as Processor

debug=False
if debug: import pprint

class main(Interface, WebInterface, Processor, Parser, FileParser):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.finished=False
        self.exit=False
        self.start_time=time.time()
        self.parse()

        if not type(self.args.hashtag) is list: self.args.hashtag=[self.args.hashtag]
        if not type(self.args.user) is list: self.args.user=[self.args.user]

    def loop(self, html=False, table="tweets"):
        while not self.finished:
            if not self.args.timeout:
                try:
                    if self.args.get_user_info:
                        print self.args
                        table="Users"
                        self.get_user_info(self.args.user)
                    elif self.args.user and not self.args.get_user_info is "True":  self.get_by_timeline_array(self.args.user)
                    if self.args.hashtag and not self.args.get_user_info is "True": self.get_by_hashtag(self.args.hashtag)
                    if self.args.read_file: self.get_by_file(self.args.read_file)
                except: pass
                self.finished=True
            elif ( time.time() - self.start_time ) > int(self.args.timeout):
                break
            else:
                # We put a 30 seconds sleep because twitter's api 1 minute caching.
                self.get_by_hashtag(self.args.hashtag)
                time.sleep(30)
                self.get_by_timeline_array(self.args.user)
                time.sleep(30)

        if self.exit: return
        if table is "tweets": object_=self.tweets
        else: object_=self.users
        return self.process_data(html, object_)

class Application(tornado.web.Application):
    def __init__(self, args, a):
        handlers=[
                ("/([^/]+)", a.RequestHandler),
                ("/", a.RequestHandler)
                ] 
        settings={ 
                'a': a,
                "args":args,
                "static_path": os.path.join(os.path.dirname(__file__), "static"),
                }

        tornado.web.Application.__init__(self, handlers, **settings)

class MainApp(object):
    def __init__(self):
        global a
        self.a=main()
        self.assign_api(self.a)
        if self.a.args.server:
            http_server = tornado.httpserver.HTTPServer(Application(self.a.args, self.a))
            http_server.listen(8080)
            tornado.ioloop.IOLoop.instance().start()
        else: self.a.loop()

    def assign_api(self, b):
        try: b.api = twitter.Api(consumer_key=b.args.auth[0], consumer_secret=b.args.auth[1], access_token_key=b.args.auth[2], access_token_secret=b.args.auth[3])
        except:
            try:
                from RLT.authentication import TwitterOauth as Api
                b.api=Api().get_api()
            except Exception, e:
                print e
                b.api=twitter.Api()


if __name__ == "__main__": MainApp()
