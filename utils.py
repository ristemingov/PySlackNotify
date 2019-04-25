import os
import time
import datetime

def read_profiles_file(filename):
    with open(filename) as f:
        content = f.readlines()

    return [x.strip() for x in content]


def get_utc_date_now():
    return datetime.datetime.utcnow()

def delay_one_minute():
    time.sleep(60)

def compile_slack_tweet(tweet):
    user = tweet['user']['screen_name']
    tweet_link =  create_tweet_link(tweet, user)
    return ("User: " + user + "\n" + "Text: " + tweet['text'] + "\n"
            + "Link: " + tweet_link + "\n" +"Time: " + tweet['timestamp'])

def create_tweet_link(tweet, user):
    return os.path.join('https://twitter.com', user, 'status', tweet['id_str'])

def convert_twitter_timestamp(twitter_timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twitter_timestamp, '%a %b %d %H:%M:%S +0000 %Y'))

def difference_in_minutes(last_update, timestamp):
    d2 = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    d1_ts = time.mktime(last_update.timetuple())
    d2_ts = time.mktime(d2.timetuple())

    return int(d1_ts-d2_ts) / 60

