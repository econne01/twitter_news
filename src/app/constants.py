class CommonWords(object):
    ''' Document common English filler words (ie, 'and', 'to', 'in')
        as a way to know they are not useful repeated terms
    '''
    # General lists
    filler_types = [
        'abbreviations', 'amounts', 'articles',
        'conjunctions',
        'prepositions', 'profanity', 'pronouns',
        'questions', 'simple_verbs', 'simple_description',
        'tobe', 'twitter_terms',
    ]
    punctuations = ['?', '!', ':', '.', ',', '\'', '"']

    # Filler word lists
    abbreviations = [
        'haha', 'lol', 'omg', 'wtf',
    ]
    amounts = [
        'first', 'last',
        'much', 'many', 'more', 'most',
        'no', 'none', 'only',
        'one', 'two', 'three',
        'some',
    ]
    articles = ['a', 'an', 'the']
    conjunctions = ['-', '--', 'and', '&', '&amp;', 'as', 'but', 'neither', 'nor', 'or', 'so',
                    'than', 'that', 'which']
    prepositions = [
        'about', 'above', 'across', 'after',
        'against', 'along', 'among', 'around',
        'at', 'before', 'behind', 'below',
        'beneath', 'beside', 'between', 'beyond',
        'by', 'despite', 'down', 'during',
        'except', 'for', 'from', 'in',
        'inside', 'into', 'like', 'near',
        'of', 'off', 'on', 'onto',
        'out', 'outside', 'over', 'past',
        'since', 'through', 'throughout', 'til',
        'till', 'to', 'toward', 'under',
        'underneath', 'until', 'up', 'upon',
        'with', 'within', 'without'
    ]
    profanity = [
        'cock', 'cunt', 'dick',
        'fuck', 'fucking', 'fucker',
        'shit', 'shitting',
    ]
    pronouns = [
        'all', 'anybody', 'anyone',
        'every', 'everybody', 'everyone',
        'he', 'his', 'her', 'hers',
        'here', 'heres',
        'i', 'im', 'it', 'its',
        'me', 'mine', 'my',
        'our', 'ours',
        'she', 'they', 'there', 'theres',
        'their', 'theirs', 'theyre', 'them',
        'this', 'that',
        'u', 'ur', 'us',
        'we',
        'you', 'your', 'yours',
    ]
    questions = ['who', 'what', 'where', 'why', 'when', 'how']
    simple_description = [
        'new', 'now',
    ]
    simple_verbs = [
        'age', 'aged',
        'can', 'cant', 'could', 'couldnt',
        'die', 'dies', 'died', 'dead', 'dying',
        'do', 'done', 'doing', 'did', 'didnt',
        'get', 'getting', 'got', 'gotten',
        'go', 'gone', 'going', 'went',
        'have', 'had', 'has', 'having', 'hasnt', 'hadnt',
        'help', 'helps', 'helped', 'helping',
        'shall', 'should', 'shouldnt',
        'say', 'says', 'said',
    ]
    time = [
        'today', 'tomorrow', 'yesterday',
        'tonight', 'tonights',
        'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday',
    ]
    tobe = [
        'am', 'are', 'be', 'being',
        'is', 'isnt',
        'not',
        'was', 'wasnt', 'wont', 'were', 'will',
    ]
    twitter_terms = [
        'rt',
    ]

    def depunctuate_word(self, word):
        ''' Remove any confusing/optional punctuation from a
            word and return it (at least punctuation is optional
            for tweeters)
        '''
        for punct in self.punctuations:
            word = word.replace(punct, '')
        return word

    def is_filler_word(self, word):
        ''' Return true if given word is listed in one of
            this class's filler_word lists
        '''
        word = self.depunctuate_word(word)
        is_filler = False

        if word != '':
            for word_type in self.filler_types:
                if word.lower() in getattr(self, word_type):
                   is_filler = True
                   break
        return is_filler
