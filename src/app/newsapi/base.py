
class BaseNewsAPI(object):

    def get_standard_field_names(self):
        return [
            'article_id',
            'author_name',
            'headline',
            'publish_date',
            'source',
            'url',
        ]

    def make_standard_format(self, news, many=False):
        ''' All news sites may not have same API format, so we
            need to convert different sources to one consistent
            format
            @param Dictionary news. Or List of [Dictionary news_item]
            @param Boolean many. Is news an object or list?
        '''
        raise Exception('''
            make_standard_format() function must be implemented
            to return objects with fields of {fields}
        '''.format(fields = ', '.join(self.get_standard_field_names())))


    def get_articles(self, search_term, limit=10):
        raise Exception('get_articles() function must be implemented')
