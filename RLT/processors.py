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
        a=""
        try: a+='_'.join(self.args.hashtag)
        except: pass
        try: a+='_'.join(self.args.user)
        except: pass

        try:
            return a
        except:
            return "Undefined"

class JSONExporter(Result):
    def result(self, return_json=False, obj=False):
        if self.args.get_json or self.args.get_user_info: return_json=True
        if return_json: return self.json_(obj)
    def json_(self, obj):
        if self.args.save_file:
            with open(self.get_filename() + '.json', 'a') as file_:
                file_.write(json.dumps(obj))
        return json.dumps(obj)

class SQLiteExporter(Result):
    def result(self, return_sqlite=False, obj=False):
        if self.args.sqlite: return_sqlite=True
        if return_sqlite:
            import sqlite3
            c=sqlite3.connect(self.get_filename() + '.sqlite3').cursor()
            if self.args.get_user_info:
                c.execute('Create table users if not exists (name text, followers text, following text, geocode text) ')
                for user in self.users:
                    c.execute('Insert into users (%s,%s,%s,%s)' %(user.name, user.followers, user.following, user.geocode)) # FIXME make this rigmake this right..

            if len(self.args.tweets) > 0:
                c.execute('Create table tweets if not exists (user text, text text, date text) ')
                for tweet in self.tweets:
                    c.execute('Insert into tweets (%s,%s,%s,%s)' %(tweet[1], tweet[2], tweet[3]))

class MYSQLExporter(Result):
    def result(self, return_mysql=False, obj=False):
        if not self.args.mysql: return
        import MySQLdb
        query=[ "Insert into tw_user  (name, tw_id, task_status, task_host, created_at, statuses_count, friend_count, followers_count, geo_lat, get_long, geo_text) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , # FIXME make this right.
                "Insert into user_followers (%s,%s,%s,%s,%s)"
                ]
        mysql=self.args.mysql 
        self.sqlconn= MySQLdb.connect (host = mysql[0], user = mysql[1], passwd = mysql[2], db = mysql[3])


    def save(self, query, args):
        try:
            self.sqlconn.cursor().execute(query %args)
        except:
            pass
        with open(self.get_filename + '.mysql', 'a') as file_:
            file_.write(query)

        return

class HTMLExporter(Result):
    def result(self, return_html=False, obj=False):
        html="<table class='sample'><tbody>%s</tbody></table>" %(self.table(obj))

        if self.args.save_file:
            with codecs.open(self.get_filename() + '.html','w','utf-8') as page_:
                page_.write(html.encode('ascii','ignore'))

        if return_html:
            return html

    def table(self, object_, j=0, a=""):
        for i in [tuple(object_[i:i+2]) for i in xrange(0,len(object_),2)]:
            if j == 6: 
                a+="</tbody></table><table class='sample'><tbody>"
                j=0
            j=j+1
            try:
                pri=i[0][2]
                sec=""
                if len(i) != 1: sec=i[1][2]
                a+="<tr><td><p>%s</p></td><td><p>%s</p></td></tr>" %(pri, sec)
            except:
                pass
        return a

class ResultsGenerator(object):
    """
        Generates result both in html, txt and prints (if debug enabled) output to console.
        override it for generating your own results.
    """

    def get_mysql_obj(self, users):
        """
            Return parsed objects ready to be injected in mysql queries for a BIFI project's datamining 
        """
        myusers=[]
        myfollowers=[]
        myfriends=[]
        self.host="127.0.0.1"

        for user in users[0]:
            user_=users[0][user]

            try:
                (geo_lat, geo_long)=user_[0]['status']['geo'].split(',')
            except:
                geo_lat=""
                geo_long=""

            try:
                myusers.append(
                    [
                        user_[0]['screen_name'],
                        user_[0]['id'],
                        2,
                        self.host,
                        user_[0]['created_at'],
                        user_[0]['statuses_count'],
                        user_[0]['friends_count'],
                        user_[0]['followers_count'],
                        geo_lat,
                        geo_long,
                        user_[0]['location'],
                    ]
                    )
            except Exception, e:
                print e

            for follower_id in user_[1]['ids']:
                myfollowers.append([user_[0]['id'], follower_id])

            for friend_id in user_[2]['ids']:
                myfriends.append(user[0]['id'], friend_id])

        return (myusers, myfollowers, myfriends)

    def process_data(self, get_html=False, obj=False):
        if not obj:
            obj=(self.tweets, self.users)

        if type(obj) is not types.TupleType:
            obj=tuple(obj)

        opts=[
                [True, obj], # HTMLExporter
                #[get_html, obj], # SQLiteExporter
                [False, self.get_mysql_obj(obj)], # MYSQLExporter
                [False, (self.users, self.tweets)], # JSONExporter
                ]
        self.objects=[]

        try: HTMLExporter(self.objects, self.args)
        except: pass
        #SQLiteExporter(self.objects, self.args)
        try: MysqlExporter(self.objects, self.args)
        except: pass
        try: JSONExporter(self.objects, self.args)
        except: pass

        return [ a.result(*opts[b]) for b,a in enumerate(self.objects)]
