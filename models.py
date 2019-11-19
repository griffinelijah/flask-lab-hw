import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('plants.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE


class Plant(Model):
	name = CharField()
	alias = CharField()
	origin = CharField()
	owner = ForeignKeyField(User, backref='plants')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Plant], safe=True)
	print('TABLES CREATED')
	DATABASE.close()

