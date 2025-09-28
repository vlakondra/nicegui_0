from peewee import *
from peewee import SqliteDatabase

db = SqliteDatabase("ursei.db")


class BaseModel(Model):
    class Meta:
        database = db


class Department(BaseModel):
    name = CharField(unique=True)


class Group(BaseModel):
    name = CharField()
    department = ForeignKeyField(Department, backref="groups")


class Student(BaseModel):  # переименование полей модели
    fam = TextField(column_name="surname")
    studname = TextField(column_name="name")
    sex = CharField(column_name="gender")  # 'M' или 'F'
    age = IntegerField()
    studgroup = ForeignKeyField(Group, column_name="group_id", backref="students")
