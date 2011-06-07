#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import codecs
import json
import types
import socket
import fcntl
import struct

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
        query=[ "update tw_user set tw_id=\'%s\', task_status=\'%s\', task_host=\'%s\', created_at=\'%s\', statuses_count=\'%s\', friend_count=\'%s\', followers_count=\'%s\', geo_lat=\'%s\', geo_long=\'%s\', geo_text=\'%s\' where  name=\'%s\'" ,
                "Insert into tw_userfollower (user_tw_id, follower) values (%s,%s)",
                "Insert into tw_frienduser (friend, user_tw_id) values (%s,%s)"
                ]
        mysql=self.args.mysql.split(',') 
        try:
            self.sqlconn= MySQLdb.connect (host = mysql[0], user = mysql[1], passwd = mysql[2], db = mysql[3])
        except Exception, e:
            print "Not saving to mysql database: %s" %e
        return [ [ self.save(query[o], b) for b in i ] for o, i  in enumerate(obj)]

    def save(self, query, args):
        try:
            print(query %tuple(args))
            self.sqlconn.cursor().execute(query %tuple(args))
        except Exception, e:
            print e
            print "Probably something failed connecting to db"
            pass
        try:
            with open(self.get_filename() + '.mysql', 'a') as file_:
                file_.write(query %tuple(args))
                file_.write('\n')
        except:
            pass
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

def get_ip_address(ifname):
    """
    http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])



class ResultsGenerator(object):
    """
        Generates result both in html, txt, sql and prints (if debug enabled) output to console.
        override it for generating your own results.
    """

    def get_mysql_obj(self, users):
        """
            Return parsed objects ready to be injected in mysql queries for a BIFI project's datamining 
        """
        myusers=[]
        myfollowers=[]
        myfriends=[]
        self.host=get_ip_address('eth0')
        for users_ in users:
            for user_ in users_:
                user_=users_[user_]
        
                try:
                    (geo_lat, geo_long)=user_[0]['status']['geo'].split(',')
                    print "Lat, long: %s,%s" %(geo_lat, geo_long)
                except:
                    geo_lat=-1
                    geo_long=-1

                try:
                    dt=user_[0]['created_at']
                except Exception, e:
                    print "DATE ERROR: %s" %e
                    dt=""

                try:
                    location=user_[0]['location'] 
                    print location
                except:
                    location=""

                try:
                    screen_name=user_[0]['screen_name']
                    print user_[0]['screen_name']
                except:
                    try:
                        screen_name=user_[0]['screen_name'].encode('utf-8', errors='replace')
                    except:
                        screen_name=Failed

                try:
                    myusers.append( [ user_[0]['id'],  2, self.host, dt, user_[0]['statuses_count'],
                          user_[0]['friends_count'], user_[0]['followers_count'], 
                          geo_lat, geo_long, location, screen_name 
                          ] )
                except Exception, e:
                    print e
                    pass

                for follower_id in user_[1]['ids']:
                    myfollowers.append([user_[0]['id'], follower_id])
    
                for friend_id in user_[2]['ids']:
                    myfriends.append(friend_id, [user_[0]['id'])

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
        try: MYSQLExporter(self.objects, self.args)
        except Exception, e: print e
        try: JSONExporter(self.objects, self.args)
        except: pass
        return [ a.result(*opts[b]) for b,a in enumerate(self.objects)]
