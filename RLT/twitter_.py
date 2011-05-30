#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
from twitter import Api, User
try:
    import oauth.oauth as oauth
except ImportError:
    import oauth

try:
      from urlparse import parse_qsl
except:
      from cgi import parse_qsl

import pprint

AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
SIGNIN_URL = 'http://twitter.com/oauth/authenticate'
REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'

class OAuthApi(Api):
    "OAuthApi code from http://oauth-python-twitter.googlecode.com"
    def __init__(self, consumer_key, consumer_secret, access_token=None):
        if access_token:
            Api.__init__(self,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token.key, access_token_secret=access_token.secret)
        else:
            Api.__init__(self)
        self._Consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self._access_token = access_token


    def _GetOpener(self):
        opener = self._urllib.build_opener()
        return opener

    def _FetchUrl(self,
                    url,
                    post_data=None,
                    parameters=None,
                    no_cache=None):
        '''Fetch a URL, optionally caching for a specified time.

        Args:
          url: The URL to retrieve
          post_data:
            A dict of (str, unicode) key/value pairs.  If set, POST will be used.
          parameters:
            A dict whose key/value pairs should encoded and added
            to the query string. [OPTIONAL]
          no_cache: If true, overrides the cache on the current request

        Returns:
          A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if self._default_params:
          extra_params.update(self._default_params)
        if parameters:
          extra_params.update(parameters)

        # Add key/value parameters to the query string of the url
        #url = self._BuildUrl(url, extra_params=extra_params)

        if post_data:
            http_method = "POST"
            extra_params.update(post_data)
        else:
            http_method = "GET"

        req = self._makeOAuthRequest(url, parameters=extra_params,
                                                    http_method=http_method)
        self._signRequest(req, self._signature_method)


        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        #encoded_post_data = self._EncodePostData(post_data)

        if post_data:
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""

        no_cache=True
        # Open and return the URL immediately if we're not going to cache
        # OR we are posting data
        if encoded_post_data or no_cache:
          if encoded_post_data:
              url_data = opener.open(url, encoded_post_data).read()
          else:
              url_data = opener.open(url).read()
          opener.close()
        else:
          # Unique keys are a combination of the url and the username
          if self._username:
            key = self._username + ':' + url
          else:
            key = url

          # See if it has been cached before
          last_cached = self._cache.GetCachedTime(key)

          # If the cached version is outdated then fetch another and store it
          if not last_cached or time.time() >= last_cached + self._cache_timeout:
            url_data = opener.open(url).read()
            opener.close()
            self._cache.Set(key, url_data)
          else:
            url_data = self._cache.Get(key)

        # Always return the latest version
        return url_data

    def _makeOAuthRequest(self, url, token=None,
                                        parameters=None, http_method="GET"):
        '''Make a OAuth request from url and parameters

        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        if not token:
            token = self._access_token
        request = oauth.OAuthRequest.from_consumer_and_token(
                            self._Consumer, token=token,
                            http_url=url, parameters=parameters,
                            http_method=http_method)
        return request

    def _signRequest(self, req, signature_method=oauth.OAuthSignatureMethod_HMAC_SHA1()):
        '''Sign a request

        Reminder: Created this function so incase
        if I need to add anything to request before signing

        Args:
          req: The OAuth request created via _makeOAuthRequest
          signate_method:
             The oauth signature method to use
        '''
        req.sign_request(signature_method, self._Consumer, self._access_token)


    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL

        Returns:
          A signed OAuthRequest authorization URL
        '''
        req = self._makeOAuthRequest(url, token=token)
        self._signRequest(req)
        return req.to_url()

    def getSigninURL(self, token, url=SIGNIN_URL):
        '''Create a signed Sign-in URL

        Returns:
          A signed OAuthRequest Sign-in URL
        '''

        signin_url = self.getAuthorizationURL(token, url)
        return signin_url

    def getAccessToken(self, pin, url=ACCESS_TOKEN_URL):
        token = self._FetchUrl(url, parameters={'oauth_verifier':pin},no_cache=True)
        return oauth.OAuthToken.from_string(token)

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token from Twitter

        Returns:
          A OAuthToken object containing a request token
        '''
        resp = self._FetchUrl(url, no_cache=True)
        token = oauth.OAuthToken.from_string(resp)
        return token

    def GetUserInfo(self, url='https://twitter.com/account/verify_credentials.json'):
        '''Get user information from twitter

        Returns:
          Returns the twitter.User object
        '''
        json = self._FetchUrl(url)
        data = simplejson.loads(json)
        self._CheckForTwitterError(data)
        return User.NewFromJsonDict(data)


class twitterParser(object):
    """
        Gets tweets, filters them and orders them by weight
        Note: for analizer it currently not parses weight...
    """
    accesstoken=False
    CONSUMERKEY="KPykPtL27CCIes3H7hPiA"
    CONSUMERSECRET="pVKiXlweobZIjEh3gOiaNB5r5e8bCx1Wz3fJqZt9o"
    def __init__(self):
        self.api = OAuthApi(self.CONSUMERKEY, self.CONSUMERSECRET)
        self.request_token = self.api.getRequestToken()
        self.auth_url = self.api.getAuthorizationURL(self.request_token)
        self.pin=False
        self.users=[]
        self.tweets=[]

    def getpin(self):
        # FIXME Make user launch URL
        # This is hard, as we've got to deceide if via web or locally...
        # And then get results acording to one thing or another...
        # What about to store it in a cookie/file??
        if self.pin:
            self.api = OAuthApi(self.CONSUMERKEY, self.CONSUMERSECRET, self.request_token)
            self.accesstoken = self.api.getAccessToken(self.pin)

    def second_level_find(self,list_,key):
        for sublist in list_: 
            return sublist[2] == key

    def get_user_info(self, users):
        for user in users:
            if user is None: return
            print "getting user %s" %user
            self.users.append([self.api.GetUser(user), self.api.GetFriends(user), self.api.GetFollowers(user) ])

    def get_by_file(self, file_):
        with open(file_) as f:
            json.loads(f.read())

    def get_by_timeline_array(self, timelines):
        filter_=self.args.filter_

        for user in timelines:
            if user is None: return
            options={
                'screen_name': user,
                'since_id': self.args.since_id,
                'count': self.args.count,
            }
            try:
                for i in self.api.GetUserTimeline(**options): # TODO Fill options.
                    if not self.args.parse_weight:
                        if not self.second_level_find(self.tweets, i.text):
                            if not filter_:
                                self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                            elif filter_ in i.text:
                                self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                    else:
                        if not i.in_reply_to_user_id and not self.second_level_find(self.tweets, i.text):
                            if i.retweet_count is not 0 and i.retweet_count is not None:
                                if not filter_:
                                    self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                                elif filter_ in i.text:
                                    self.tweets.append([ i.retweet_count, i.created_at, i.text , i.location])
                self.tweets=sorted(self.tweets, reverse=True)
            except Exception, e:
                self.tweets.append(('Twitter Error','Twitter Error',e))
                self.tweets.append(('Twitter Error','Twitter Error',e))

    def get_by_hashtag(self, hashtags, geocode=None):
        for hashtag in hashtags:
            if not hashtag: return
            for tweet in self.api.GetSearch(term=hashtag, geocode=geocode):
                if not tweet.in_reply_to_user_id and not self.second_level_find(self.tweets, tweet.text):
                    self.tweets.append([tweet.retweet_count, tweet.created_at, tweet.text, tweet.location] )
            self.tweets=sorted(self.tweets, reverse=True)
