import re
from redis import StrictRedis
from redis_lru import RedisLRU

import connection
from models import Quotes, Authors


client = StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)

@cache()
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

@cache
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
    n = 0
    while n < 3:
        stop_word = 'exit'
        if n == 0:
            query = 'name:St'.split(':')
        elif n == 1:
            query = 'tag:li'.split(':')
        elif n == 2:
            query = 'tag:li,chan'.split(':')        
        result = execute_query(*query)
        for i in result:
            print(i)
        print('-' * 80)
        n += 1

if __name__ =='__main__':
    main()