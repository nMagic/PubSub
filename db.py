import os
from peewee import *

if os.environ.get('SQL_DIALECT') == 'POSTGRESQL':
    pass
else:
    db = SqliteDatabase('app.db')


class Publication(Model):
    title = CharField(max_length=256)
    content = TextField()
    it_posted = BooleanField(default=False)

    class Meta:
        database = db
