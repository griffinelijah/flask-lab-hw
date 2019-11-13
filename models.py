import datetime
from peewee import *

DATABASE = SqliteDatabase('students.sqlite')

class Student(Model):
	name = CharField()
	home_town = CharField()
	age = IntegerField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([STUDENT], safe=True)
	print('TABLES CREATED')
	DATABASE.close()