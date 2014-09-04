import requests

from flask import render_template, request, session, redirect, url_for
from app import app
from app.newsapi import get_all_articles
from app.twitter import TwitterDataHandler

#---- VIEWS ----#
@app.route('/')
def index():
    if 'username' in session:
        # If already logged in, go to users news page
        return redirect(url_for('user_news', username=session['username']))
    else:
        return render_template(
            'index.html',
            username=None,
            tweets = [],
            terms = [],
            news = {}
        )

@app.route('/<username>')
def user_news(username):
    if 'username' not in session or session['username'] != username:
        # Cannot access a user's page unless he is logged in
        return redirect(url_for('index'))

    api = TwitterDataHandler(token = session['access_token'], secret = session['access_token_secret'])
    tweet_history = api.getUserTweetTimeline(limit=100)
    popular_terms = api.findPopularTerms(tweet_history)

    news = []
    if popular_terms:
        news = get_all_articles(popular_terms, limit=100)

    return render_template(
        'usernews.html',
        username=username,
        tweets = tweet_history,
        terms = popular_terms,
        news = news
    )

@app.route('/login')
def login():
    ''' Login to app using Twitter OAuth
    '''
    if 'username' in session:
        # If already logged in, go to users news page
        return redirect(url_for('user_news', username=session['username']))
    else:
        # Get the request token and secret from Dataminr
        r = requests.get(
            'https://homework.dataminr.com/getTwitterRequestToken',
            params={'callback': url_for('login_oauth_success', _external=True)}
        )
        result = r.json()

        # Handle any errors when trying to get request token
        if not r.ok or result['results']['oauth_callback_confirmed'] != 'true':
            return render_template('error.html')

        # Set tokens as session variables
        session['request_token'] = result['requestToken']
        session['request_token_secret'] = result['requestTokenSecret']

        # Redirect to Twitter to actually login
        return redirect(
            'https://api.twitter.com/oauth/authorize?oauth_token={request_token}'.format(request_token = result['requestToken']),
            code = 302
        )

@app.route('/login/oauthSuccess')
def login_oauth_success():
    ''' Set the login credentials in user's session and redirect to homepage
        This view should only be accessed as a redirect from Twitter Authorization page
        @params String oauth_token
        @params String oauth_verifier
    '''
    oauth_verifier = request.args.get('oauth_verifier')

    # Get the access token and secret from DataMinr
    r = requests.get(
        'https://homework.dataminr.com/getTwitterAccessToken',
        params={
            'requestToken': session['request_token'],
            'requestTokenSecret': session['request_token_secret'],
            'oauth_verifier': oauth_verifier
        }
    )
    result = r.json()

    # Handle any errors when trying to get request token
    if not r.ok:
        return render_template('error.html')

    # Set session variables with Access tokens
    session['username'] = result['results']['screen_name']
    session['access_token'] = result['accessToken']
    session['access_token_secret'] = result['accessTokenSecret']
    return redirect(url_for('user_news', username=session['username']))

@app.route('/logout')
def logout():
    ''' Logout current user by deleting all session variables
    '''
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_msg='404'), 404
