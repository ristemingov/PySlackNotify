import os
import time
import twitter
import datetime
from settings import LAST_N
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET



api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def twitter_feed(list_users, last_update):
    tweet_feed = []

    for t_user in list_users:
        user_feed = get_tweeter_user_feed(t_user, LAST_N, last_update)
        tweet_feed.extend(user_feed)

    return tweet_feed

def get_tweeter_user_feed(user, last_n_tweets, last_update):

    t = api.GetUserTimeline(screen_name=user, count=last_n_tweets)
    tweet_list = [i.AsDict() for i in t if ('retweeted_status' not in i.AsDict() and
                                            'in_reply_to_user_id' not in i.AsDict()
                                            )]
    filtered_tweets = filter_unpublished_tweets(tweet_list, last_update)

    return filtered_tweets



def filter_unpublished_tweets(tweet_list, last_update):
    filtered_tweets = []
    for twt in tweet_list:
        twt.setdefault('timestamp',
                       time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.strptime(twt['created_at'], '%a %b %d %H:%M:%S +0000 %Y')))
        d2 = datetime.datetime.strptime(twt['timestamp'], '%Y-%m-%d %H:%M:%S')

        d1_ts = time.mktime(last_update.timetuple())
        d2_ts = time.mktime(d2.timetuple())

        if (int(d1_ts-d2_ts) / 60) < 1:
            filtered_tweets.append(twt)

    return filtered_tweets

