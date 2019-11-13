import datetime
from peewee import *

DATABASE = SqliteDatabase('plants.sqlite')

class Plant(Model):
	name = CharField()
	alias = CharField()
	origin = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([PLANT], safe=True)
	print('TABLES CREATED')
	DATABASE.close()	