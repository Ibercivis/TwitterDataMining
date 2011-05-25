#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
from RLT import *
import time
import os
class main(tweetWeightParser, InterchangeableInterface, ResultsGenerator, ArgumentParser):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.finished=False
        self.exit=False
        self.start_time=time.time()
        self.parse()
        global args
        args=self.args

        if not type(self.args.hashtag) is list: self.args.hashtag=[self.args.hashtag]
        if not type(self.args.user) is list: self.args.user=[self.args.user]

    def loop(self, html=False):
        while not self.finished:
            if not self.args.timeout:
                self.get_by_hashtag(self.args.hashtag)
                self.get_by_timeline_array(self.args.user)
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
