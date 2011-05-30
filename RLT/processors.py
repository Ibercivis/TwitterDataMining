#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import codecs
import json

class ResultsGenerator(object):
    """
        Generates result both in html, txt and prints (if debug enabled) output to console.
        override it for generating your own results.
    """
    def get_filename(self):
        if self.args.file: return self.args.file
        try:
            return ('_').join(self.args.hashtag) + "_" + ('_').join(self.args.user)
        except:
            return "Undefined"

    def process_data(self, stat=False, table="tweets"):
        if stat:
            return self.write_html(stat, table)
        with open(self.get_filename(), 'w') as file:
            file.write(self.tweets.__str__())
        if debug: pprint.PrettyPrinter().pprint(self.tweets)
        return self.write_html(stat)

    def get_table(self, table="tweets"):
        j=0
        a=""
        if table is "tweets":
            object_=self.tweets
        else:
            object_=self.users
        if self.second_level_find(self.tweets, 'Twitter Error'):
            return  "%s %s" %(a, "An error ocurred, try again later: %s" %self.tweets.__str__())

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

    def write_html(self, stat=False, table="tweets"):
        if self.args.get_json or self.args.get_user_info:
            b=[ c.AsDict() for c in self.users ]
            b.append(self.tweets)
            return json.dumps(b)

        a="<table class='sample'><tbody>%s</tbody></table>" %(self.get_table(table))

        if stat:
            return a

        with codecs.open(self.get_filename() + '.html','w','utf-8') as page_:
            page_.write(a.encode('ascii','ignore'))

        if self.args.sqlite:
            c=sqlite3.connect(self.get_filename() + '.sqlite3').cursor()
            if self.args.get_user_info:
                c.execute('Create table users if not exists (name text, followers text, following text) ')
                for user in self.users:
                    c.execute('Insert into users (%s,%s,%s)' %(user.name, user.followers, user.following)) # FIXME
