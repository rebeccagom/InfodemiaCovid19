import tweepy
import csv
from csv import reader
import time


consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    user = api.get_user(screen_name)
    alltweets = []
    
    if user.protected == False:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
        alltweets.extend(new_tweets)
        if len(alltweets) > 0:
            oldest = alltweets[-1].id - 1
    else:
        new_tweets=[]
    
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count, tweet.user.name, tweet.user.screen_name] for tweet in alltweets]

    with open(f'new_{screen_name}_tweets.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text", "retweets", "favorites", "username", "screen_name" ])
        writer.writerows(outtweets)
    
    pass

with open('influenciadores_rgb.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

    backoff_counter = 1
    while True:
        for influenciador in data:
            try:
                if __name__ == '__main__':
                    user = influenciador[0]
                    get_all_tweets(user)
    
            except tweepy.TweepError as e:
                print(e.reason)
                if 'Failed to send request:' in e.reason:
                    print ("Time out error caught.")
                    time.sleep(180)
                else:
                    outtweets = []
                    with open(f'new_{user}_tweets.csv', 'w', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["id","created_at","text", "retweets", "favorites", "username"])
                        writer.writerow([e.reason])
                        writer.writerows(outtweets)
        break