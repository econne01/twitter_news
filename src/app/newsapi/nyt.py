import requests

from app.newsapi import BaseNewsAPI

class NewYorkTimesAPI(BaseNewsAPI):
    base_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'
    request_key = '79513be5ca634cebcf8cc5252fa91358:6:63003812'
    source_name = 'New York Times'

    page_size = 10 # This is a NYT default value

    def get_author_name(self, nyt_person):
        ''' Convert the NYT API's person object to an author name
        '''
        author_names = []
        if 'firstname' in nyt_person:
            author_names.append(nyt_person['firstname'])
        if 'lastname' in nyt_person:
            author_names.append(nyt_person['lastname'])
        return ' '.join([name[0].upper() + name[1:].lower() for name in author_names])

    def make_standard_format(self, news, many=False):
        if many or isinstance(news, list):
            return [self.make_standard_format(news_item, many=False) for news_item in news]
        else:
            try:
                #@todo - note that there could be multiple authors. For now
                # we just take the first one
                author = news['byline']['person'][0]
            except Exception:
                author_name = ''
            else:
                author_name = self.get_author_name(author)

            headline = news['headline']
            for attempted_label in ['print_headline', 'main']:
                if attempted_label in headline:
                    headline = headline[attempted_label]
                    break

            return {
                'article_id': news['_id'],
                'author_name': author_name,
                'headline': headline,
                'publish_date': news['pub_date'],
                'source': self.source_name,
                'url': news['web_url'],
            }



    def get_articles(self, search_term, limit=10):
        ''' Get recent articles from NYT API,
            by default sort by most recent and only get required fields
        '''
        r = requests.get(
            self.base_url,
            params = {
                'api-key': self.request_key,
                'q': search_term,
                'sort': 'newest',
                'fl': '_id,web_url,headline,pub_date,byline',
            }
        )

        articles = []
        if r.ok:
            articles = r.json()['response']['docs']
        return articles
