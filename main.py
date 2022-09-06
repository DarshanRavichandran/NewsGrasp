from newsapi import NewsApiClient
import tweepy
from constants import *
import time
import os

newsap = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

auth = tweepy.OAuthHandler(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                           consumer_secret=os.environ["TWITTER_CONSUMER_SECRET_KEY"])
auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"])
api = tweepy.API(auth)


def post_on_twitter(title, body, source, tags):
    """
    :param title: Title for the post
    :param body: Url of the post
    :param source: credits for the source
    :return: None
    """
    api.update_status(f"{title}\nSource: {source}\n{tags}\n{body}")
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


def get_arranged_news_list(categories_of_news):
    """

    :param categories_of_news: raw data of news
    :return: return processed list for news
    """
    cat_len = {}
    total_news_count = 0
    for category in categories_of_news.keys():
        cat_len[category] = {}
        cat_len[category]["current_index"] = 0
        cat_len[category]["last_index"] = len(categories_of_news[category]['articles']) - 1
        total_news_count += len(categories_of_news[category]['articles'])
    print(cat_len)
    print(total_news_count)
    final_news_list = []
    current_news_count = 0
    while total_news_count > current_news_count:
        for category in categories_of_news.keys():
            if cat_len[category]["current_index"] <= cat_len[category]["last_index"]:
                index = cat_len[category]["current_index"]
                # add category in article
                categories_of_news[category]['articles'][index]['category'] = category
                # append article details in final list
                final_news_list.append(categories_of_news[category]['articles'][index])
                cat_len[category]["current_index"] = cat_len[category]["current_index"] + 1
                current_news_count += 1
    print(final_news_list)
    return final_news_list


def task():
    """
    Executes News api and Tweets
    :return: None
    """

    news_headlines = get_news_with_category()
    news_list = get_arranged_news_list(news_headlines)
    print(news_headlines)
    for content in news_list:
        try:
            tags = f"#LatestNews #{content['category'].title()} #today #NewsGrasp"
            post_on_twitter(content["title"], content['url'], content["source"]["name"], tags)
            print(f"successful post from category:{content['category']}")
            time.sleep(300)
        except Exception as e:
            print(f"unable to post the news from - {content['category']}, error msg: {str(e)}")


while True:
    task()
    time.sleep(3600)
