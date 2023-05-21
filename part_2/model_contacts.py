from mongoengine import Document
from mongoengine import StringField, BooleanField


class Contacts(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    address = StringField()
    phone = StringField()
    how_to_contact = StringField()
    sent_message = BooleanField(default=False)