from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

connect(f'mongodb+srv://{user}:{password}@{domain}.{db_name}.mongodb.net/?retryWrites=true&w=majority', ssl=True)
