#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import codecs
import json
import types

class Result(object):
    def __init__(self, generators, args):
        generators.append(self)
        self.args=args

    def get_filename(self):
        if self.args.file: return self.args.file
        try:
            return ('_').join(self.args.hashtag) + "_" + ('_').join(self.args.user)
        except:
            return "Undefined"

class JSONExporter(Result):
    def result(self, return_json=False, obj=False):
        if self.args.get_json or self.args.get_user_info: return_json=True
        if return_json: return self.json_(obj)


    def json_(self, obj):
        b=[ c.AsDict() for c in obj[0] if type(c) is not types.NoneType ]
        b.append(obj[1])
        if self.args.save_file:
            with open(self.get_filename() + '.json', 'w') as file:
                file.write(json.dumps(b))
        return json.dumps(b)

class SQLiteExporter(Result):
    def result(self, return_sqlite=False, obj=False):
        if self.args.sqlite: return_sqlite=True
        if return_sqlite:
            c=sqlite3.connect(self.get_filename() + '.sqlite3').cursor()
            if self.args.get_user_info:
                c.execute('Create table users if not exists (name text, followers text, following text, geocode text) ')
                for user in self.users:
                    c.execute('Insert into users (%s,%s,%s,%s)' %(user.name, user.followers, user.following, user.geocode)) # FIXME TODO

            if len(self.args.tweets) > 0:
                c.execute('Create table tweets if not exists (user text, text text, date text) ')
                for tweet in self.tweets:
                    c.execute('Insert into tweets (%s,%s,%s,%s)' %(tweet[1], tweet[2], tweet[3]))

class MYSQLExporter(Result):
    def result(self, return_mysql=False, obj=False):
        query=[ "Insert into tweets (%s,%s,%s,%s,%s)" , # FIXME
                "Insert into users (%s,%s,%s,%s,%s)"
                ]
        return [ self.save(query[i] %(o)) for i,o in enumerate(obj)]

    def save(self, query):
        #TODO Save it =D
        return

class HTMLExporter(Result):
    def result(self, return_html=False, obj=False):
        html="<table class='sample'><tbody>%s</tbody></table>" %(self.table(obj))

        if self.args.save_file:
            with codecs.open(self.get_filename() + '.html','w','utf-8') as page_:
                page_.write(a.encode('ascii','ignore'))

        if return_html:
            return html

    def table(self, object_, j=0, a=""):
        for i in [tuple(object_[i:i+2]) for i in xrange(0,len(object_),2)]:
            if j == 6: 
                a+="</tbody></table><table class='sample'><tbody>"
                j=0
            j=j+1
            pri=i[0][2]
            sec=""
            if len(i) != 1: sec=i[1][2]
            a+="<tr><td><p>%s</p></td><td><p>%s</p></td></tr>" %(pri, sec)
        return a

class ResultsGenerator(object):
    """
        Generates result both in html, txt and prints (if debug enabled) output to console.
        override it for generating your own results.
    """

    def process_data(self, get_html=False, obj=False):
        if not obj:
            obj=(self.tweets, self.users)

        if type(obj) is not types.TupleType:
            obj=tuple(obj)

        opts=[
                [True, obj], # HTMLExporter
                #[get_html, obj], # SQLiteExporter
                #[False, obj], # MysqlExporter
                [False, (self.users, self.tweets)], # JSONExporter
                ]
        self.objects=[]

        HTMLExporter(self.objects, self.args)
        #SQLiteExporter(self.objects, self.args)
        #MysqlExporter(self.objects, self.args)
        JSONExporter(self.objects, self.args)

        return [ a.result(*opts[b]) for b,a in enumerate(self.objects)]
