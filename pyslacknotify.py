from send_slack import send_slack_notification
from feeds.twitter import twitter_feed
from utils import read_profiles_file, get_utc_date_now, delay_one_minute, compile_slack_tweet

def pyslacknotify(list_twitter_users):
    last_update_time = get_utc_date_now()
    while True:
        tweets = twitter_feed(list_twitter_users, last_update_time)
        for tweet in tweets:
            slack_text = compile_slack_tweet(tweet)
            send_slack_notification(slack_text)
        last_update_time = get_utc_date_now()
        delay_one_minute()


if __name__ == '__main__':
    list_twitter_users_all = read_profiles_file('twitter_profiles')
    pyslacknotify(list_twitter_users_all)