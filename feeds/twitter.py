import twitter
from utils import convert_twitter_timestamp, difference_in_minutes
from settings import LAST_N
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


__api = twitter.Api(consumer_key=CONSUMER_KEY,
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

    user_tweets = __api.GetUserTimeline(screen_name=user, count=last_n_tweets)
    user_tweets = filter_only_author_tweets(user_tweets)
    user_tweets = filter_unpublished_tweets(user_tweets, last_update)

    return user_tweets


def filter_only_author_tweets(user_tweets):
    return [i.AsDict() for i in user_tweets if (is_not_retweet(i.AsDict()) and is_not_user_reply(i.AsDict()))]


def filter_unpublished_tweets(tweet_list, last_update):
    filtered_tweets = []
    for twt in tweet_list:
        twt.setdefault('timestamp', None)
        twt['timestamp'] = convert_twitter_timestamp(twt['created_at'])

        if difference_in_minutes(last_update, twt['timestamp']) < 1:
            filtered_tweets.append(twt)

    return filtered_tweets


def is_not_retweet(tweet_object):
    return 'retweeted_status' not in tweet_object


def is_not_user_reply(tweet_object):
    return 'in_reply_to_user_id' not in tweet_object