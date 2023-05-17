from mongoengine import EmbeddedDocument, Document
from mongoengine import StringField, DateField, EmbeddedDocumentField, ListField

class Authour(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(EmbeddedDocument):
    tags = ListField()
    author = StringField(EmbeddedDocumentField(Authour))
    quote = StringField()




