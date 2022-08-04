from newsapi import NewsApiClient
from config import *
import tweepy
from constants import *
import time

newsap = NewsApiClient(api_key=api_key)

auth = tweepy.OAuthHandler(consumer_key=twitter_consumer_key,
                           consumer_secret=twitter_consumer_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)


def post_on_twitter(title, body, source):
    api.update_status(f"{title}\nSource: {source}\n{body}")
    return


def get_today_news(language='en', category='business', country='in'):
    top_headlines = newsap.get_top_headlines(language=language, category=category, country=country)
    return top_headlines


def get_news_with_category():
    news = {}
    for category in categories.keys():
        try:
            gtn = get_today_news(language='en', category=category, country='in')
            news[category] = gtn
        except:
            print(f"No news collected from : {category}")
    return news


if __name__ == "__main__":
    news_headlines = get_news_with_category()
    print (news_headlines)
    for category in news_headlines.keys():
        news_count = 1
        count = 1
        for content in news_headlines[category]["articles"]:
            if news_count >= count:
                try:
                    post_on_twitter(content["title"], content['url'], content["source"]["name"])
                    print (f"successful post from category:{category}")
                    time.sleep(300)
                    count += 1
                except Exception as e:
                    print(f"unable to post the news from - {category}, error msg: {str(e)}")
            else:
                break