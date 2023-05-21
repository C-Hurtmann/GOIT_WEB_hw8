from datetime import datetime
from pathlib import Path
import json

import connection
from models import Authors, Quotes


def fetch_data_from_json(path: Path) -> list[dict]:
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def main():
    authors_json = fetch_data_from_json(Path('part_1/jsons/authors.json'))
    quotes_json = fetch_data_from_json(Path('part_1/jsons/quotes.json'))
    Authors.objects().delete()
    for i in authors_json:
        date = datetime.strptime(i['born_date'], '%B %d, %Y')
        i['born_date'] = date
        doc = Authors(**i)
        doc.save()

    Quotes.objects.delete()
    for i in quotes_json:
        i['author'] = Authors.objects(fullname=i['author'])[0]
        doc = Quotes(**i)
        doc.save()

if __name__ == '__main__':
    main()