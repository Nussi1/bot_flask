from mongoengine import EmbeddedDocument, StringField


class Author(EmbeddedDocument):
  name = StringField()
  identifier = StringField()
  ipv4 = StringField()
  ipv6 = StringField()
  
