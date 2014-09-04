from base import BaseNewsAPI
from nyt import NewYorkTimesAPI

def get_all_articles(search_terms, limit=10):
    ''' Function to compile articles from all available API sources
    '''
    if limit <= 0:
        raise Exception('Please select a limit greater than zero')

    sources = [
        NewYorkTimesAPI,
    ]

    articles = {}
    for source in sources:
        api = source()
        for search_term in search_terms:
            news = api.get_articles(search_term)
            news = api.make_standard_format(news)

            for news_item in news:
                article_id = ':'.join([news_item['source'], news_item['article_id']])
                if article_id not in articles:
                    articles[article_id] = news_item
                if 'search_terms' not in articles[article_id]:
                    articles[article_id]['search_terms'] = []
                articles[article_id]['search_terms'].append(search_term)

                if len(articles) > limit:
                    break

            if len(articles) > limit:
                break

    return articles
