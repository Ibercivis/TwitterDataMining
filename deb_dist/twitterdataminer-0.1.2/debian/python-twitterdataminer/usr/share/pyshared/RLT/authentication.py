#!/usr/bin/env python
import os
import sys
from twitter import Api
import oauth2 as oauth

try:
  from urlparse import parse_qsl
except:
  from cgi import parse_qsl

class TwitterOauth(object):
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
    AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
    SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

    consumer_key="KPykPtL27CCIes3H7hPiA"
    consumer_secret="pVKiXlweobZIjEh3gOiaNB5r5e8bCx1Wz3fJqZt9o"

    def __init__(self):
        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        self.oauth_consumer             = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        self.oauth_client               = oauth.Client(self.oauth_consumer)
        self.resp, self.content = self.oauth_client.request(self.REQUEST_TOKEN_URL, 'GET')
        self.request_token = dict(parse_qsl(self.content))

        print ''
        print 'Please visit this Twitter page and retrieve the pincode to be used'
        print 'in the next step to obtaining an Authentication Token:'
        print ''
        print '%s?oauth_token=%s' % (self.AUTHORIZATION_URL, self.request_token['oauth_token'])
        print ''

        self.pincode = raw_input('Pincode? ')

        self.token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
        self.token.set_verifier(self.pincode)
        self.oauth_client  = oauth.Client(self.oauth_consumer, self.token)
        self.resp, self.content = self.oauth_client.request(self.ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % self.pincode)
        self.access_token  = dict(parse_qsl(self.content))

    def get_api(self):
        print "Api data is: %s %s %s %s" %(self.consumer_key, self.consumer_secret, self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
        return Api(self.consumer_key, self.consumer_secret, self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
