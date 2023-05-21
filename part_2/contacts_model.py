from mongoengine import Document
from mongoengine import StringField, BooleanField


class Contacts(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent_message = BooleanField(default=False)