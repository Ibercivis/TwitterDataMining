#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
from RLT import *
import time

class main(tweetWeightParser, InterchangeableInterface, ResultsGenerator, ArgumentParser):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.finished=False
        self.exit=False
        self.start_time=time.time()
        self.parse()

        if not type(self.args.hashtag) is list: self.args.hashtag=[self.args.hashtag]
        if not type(self.args.user) is list: self.args.user=[self.args.user]

    def loop(self):
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
        self.process_data()

    class RequestHandler(tornado.web.RequestHandler):
        def get(self, slug=False):
            """
                TODO: Implement limits as twitter limits it!!!!
            """
            print "Rendering slug %s" %slug
            self.args.hashtag=self.get_argument('hashtags').split(',')
            self.args.users=self.get_argument('usernames').split(',')
            self.args.timeout=False
            self.loop()
            if not slug: slug="Starting"
            self.render('Templates/%s' %(slug), slug=slug, users=self.args.users, hashtags=self.args.hashtags )

if __name__ == "__main__":
    a=main()
    if a.args.server:
        urls=[("/view/([^/]+)", a.RequestHandler)]
        print "Rendering urls for %s" %urls
        application = tornado.web.Application(urls)
        application.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    else:
        a.loop()
