from newsapi import NewsApiClient
import tweepy
from constants import *
import schedule
import time
import os

newsap = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

auth = tweepy.OAuthHandler(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                           consumer_secret=os.environ["TWITTER_CONSUMER_SECRET_KEY"])
auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"])
api = tweepy.API(auth)


def post_on_twitter(title, body, source):
    """
    :param title: Title for the post
    :param body: Url of the post
    :param source: credits for the source
    :return: None
    """
    api.update_status(f"{title}\nSource: {source}\n{body}")
    return


def get_today_news(language='en', category='business', country='in'):
    """
    :param language: language of news
    :param category: category of news
    :param country: news based on country
    :return:
    """
    top_headlines = newsap.get_top_headlines(language=language, category=category, country=country)
    return top_headlines


def get_news_with_category():
    """
    get the news category and update them in a list
    :return: news dict
    """

    news = {}
    for category in categories.keys():
        try:
            gtn = get_today_news(language='en', category=category, country='in')
            news[category] = gtn
        except:
            print(f"No news collected from : {category}")
    return news


def task():
    """
    Executes the News api and Twitter
    :return: None
    """

    news_headlines = get_news_with_category()
    print(news_headlines)
    for category in news_headlines.keys():
        news_count = categories[category]
        count = 1
        for content in news_headlines[category]["articles"]:
            if news_count >= count:
                try:
                    post_on_twitter(content["title"], content['url'], content["source"]["name"])
                    print(f"successful post from category:{category}")
                    time.sleep(300)
                    count += 1
                except Exception as e:
                    print(f"unable to post the news from - {category}, error msg: {str(e)}")
            else:
                break


schedule.every().day.at("16:40").do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
