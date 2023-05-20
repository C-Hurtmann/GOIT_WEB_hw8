import configparser
from mongoengine import connect


config_file = '/home/czagorodnyi/git/homeworks/GOIT_WEB_hw8/part_1/config.ini'

config = configparser.ConfigParser()
config.read(config_file)

user = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

connect(db=db_name,
        username=user,
        password=password,
        host=f'mongodb+srv://{user}:{password}@{domain}.{db_name}.mongodb.net/?retryWrites=true&w=majority',
        ssl=True)
