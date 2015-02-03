import random, json, datetime, tweepy
from  sqlalchemy.sql.expression import func
from apps.main import models, db
from sqlalchemy.ext.declarative import DeclarativeMeta
from m_hero.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, N

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x not in ['metadata', 'query', 'query_class']]:
                data = obj.__dict__[field]
                try:
                    if type(data) == datetime.datetime:
                        data = data.strftime('%h %d, %y')
                        json.dumps(data)
                    else:
                        json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

def get_word(word_list, n):
    queries = models.Srt.query.all()
    query_list = list()
    for query in queries:
        if set(word_list) <= set(query.set_of_words.split()):
            query_list.append(query.list_of_words.split())
    if query_list:
        text = list()
        for lst in query_list:
            text.extend(lst)
        indexies = [i+n for i, j in enumerate(text[:-n]) if text[i:i+n] == word_list[len(word_list)-n:]]
        word = text[random.choice(indexies)]
        return word
    else: 
        return False

def add_word(word_list, n):
    if not word_list:
        word = db.session.query(models.UpperWords).order_by(func.random()).first().word #postgre
    elif len(word_list) <= n:
        word = get_word(word_list, len(word_list))
    else:
        word = get_word(word_list, n)
    if word:
        word_list.append(word)
        return True
    else:
        return False

def get_twit():
    word_list = list()
    n = N
    while len(' '.join(word_list))<140:
        if not add_word(word_list, n):
            break
        if len(' '.join(word_list))>140:
            word_list.pop()
            break
    while word_list[-1][-1] not in '.?!':
        word_list.pop()
    return ' '.join(word_list)

def twit():
    phrase = get_twit()
    twited = models.Phrases(phrase=phrase)
    db.session.add(twited)
    db.session.commit()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    api.update_status(status=phrase)
