from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, SequenceField, BooleanField, DateTimeField, ListField
from odm.author import Author


class LoggingData(EmbeddedDocument):
  summary = StringField()
  description = StringField()
  created_at = DateTimeField()


class Logging(Document):
  number = SequenceField()
  identifier = StringField(required=True)
  environment = StringField(required=True)

  data = EmbeddedDocumentField(LoggingData)

  tags = ListField()
  binds = ListField()

  author = EmbeddedDocumentField(Author)
  system = BooleanField(default=False)

  created_at = DateTimeField()
  deleted_at = DateTimeField()
