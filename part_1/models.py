from mongoengine import Document
from mongoengine import StringField, DateField, EmbeddedDocumentField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors)
    quote = StringField()




