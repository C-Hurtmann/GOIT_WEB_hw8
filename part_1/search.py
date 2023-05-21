import re
from redis import StrictRedis
from redis_lru import RedisLRU

import connection
from models import Quotes, Authors


client = StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)

@cache(ttl=3600)
def get_mongo_keys():
    notes = []
    authors = set()
    for i in Quotes.objects:
        notes.extend(i.tags)
        authors.add(i.author.fullname)
    return [notes, list(authors)]

def confirm_key(key, keys):
    pattern = re.compile(fr'{key}.*')
    return filter(lambda x: re.match(pattern, x), keys)

@cache(ttl=3600)
def execute_query(command: str, value: str):
    notes, authors = get_mongo_keys()
    if command == 'name':
        value = confirm_key(value, authors)
        author = Authors.objects.get(fullname__in=value)
        result = Quotes.objects(author=author)

    elif command == 'tag':
        value = value.split(',')
        value = list(map(lambda x: confirm_key(x, notes), value))
        value = [x for l in value for x in l]
        result = Quotes.objects.filter(tags__in=value)
    return result

def main():
    while True:
        stop_word = 'exit'
        query = input('> ')
        if query in stop_word:
            break
        query = query.split(':')
        try:   
            result = execute_query(*query)
        except:
            print('search by pattern command:value\nSuch as name:Steve Martin or tag:life,live')
        else:
            for i in result:
                print(i)
            print('-' * 80)


if __name__ =='__main__':
    main()