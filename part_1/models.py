from mongoengine import Document
from mongoengine import StringField, DateField, EmbeddedDocumentField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()
    
    def __str__(self):
        return f'{self.fullname}'

class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, dbref = True)
    quote = StringField()

    def __str__(self):
        return f'{self.author} | {self.tags} | {self.quote[:20]}...\n'




