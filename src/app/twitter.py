import operator
from urllib import urlencode

import requests

from constants import CommonWords

class TwitterDataHandler(object):
    _token = None
    _secret = None
    _cache = {}

    def __init__(self, token, secret):
        ''' Set access variables needed to get twitter
            data from external API (dataminr)
        '''
        self._token = token
        self._secret = secret

    def getUserCredentials(self):
        ''' Return an object representing the Twitter user
            determined by access token and secret codes
        '''
        if 'user' in self._cache:
            return self._cache['user']

        r = requests.get(
            'https://homework.dataminr.com/getTwitterCredentials',
            params= {
                'accessToken': self._token,
                'accessTokenSecret': self._secret
            }
        )

        if r.ok:
            self._cache['user'] = r.json()
            return self._cache['user']

        return None

    def getUserTweetTimeline(self, timeline_type='home', limit=25, **params):
        ''' Return a list of tweets for the user
            determined by access token and secret codes
            @param String timeline_type. One of (home, mentions, user, retweets)
            @param Integer limit. The max number of history tweets to fetch
        '''
        tweets = []
        if timeline_type not in ('home', 'user', 'mentions', 'retweets'):
            raise Exception('The timeline type of {timeline_type} is not allowed!'.format(
                timeline_type = timeline_type
            ))

        req_params= {
            'accessToken': self._token,
            'accessTokenSecret': self._secret,
            'type': timeline_type,
        }
        r = requests.get(
            'https://homework.dataminr.com/getTwitterTimeline',
            # @todo - Couldnt find a nicer way to format a depth-2 dictionary
            # as query param
            params = urlencode(req_params) + '&count={limit}'.format(limit=limit),
        )

        if r.ok:
            tweets = r.json()

        tweets = self.simplifyTweetData(tweets)
        return tweets

    def getUserImageUrl(self, user=None):
        if not user:
            user = self.getUserCredentials()
        return user['profile_image_url_https']

    def simplifyTweetData(self, tweets):
        ''' We only need a few relevant data fields given by Twitter API,
            so don't waste bandwidth to front end sending stuff we dont need
            @param List tweets. List of json style dict tweet objects (from Twitter API)
        '''
        simplified_list = []
        for tweet in tweets:
            simple_tweet = {}
            for field in ['created_at', 'text']:
                simple_tweet[field] = tweet[field]

            # Only get Day and Date (no timestamp)
            #@todo - change time from GMT to local time
            simple_tweet['created_at'] = ' '.join([date_component for date_component in simple_tweet['created_at'].split()[:3]])

            simple_tweet['user'] = {}
            for field in ['profile_image_url', 'screen_name', 'name']:
                simple_tweet['user'][field] = tweet['user'][field]

            simplified_list.append(simple_tweet)

        return simplified_list

    def isURL(self, term):
        ''' Return true if given term is a URL
        '''
        return term.lower()[:4] == 'http'

    def findPopularTerms(self, tweets, term_limit=10):
        ''' Parse the list of tweets for list of top most popular terms
        '''
        if term_limit < 0:
            raise Exception('Please select a limit of popular terms greater than or equal to zero')

        common = CommonWords()

        term_count = {}
        for tweet in tweets:
            for word in tweet['text'].split(' '):
                word = word.lower()
                word = common.depunctuate_word(word)

                if word.strip() == '' or common.is_filler_word(word):
                    continue
                elif self.isURL(word):
                    continue
                elif word not in term_count:
                    term_count[word] = 0

                term_count[word] += 1

        # Convert terms to tuple of (term, count) so we can sort
        popular_terms = sorted(term_count.iteritems(), key=operator.itemgetter(1))
        popular_terms.reverse()
        # Now convert back to just the term
        return [term[0] for term in popular_terms[:term_limit]]

