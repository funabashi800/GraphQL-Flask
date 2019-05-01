import sqlalchemy
from db import db
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class DepartmentModel(Base):
  __tablename__ = 'department'
  id = db.Column(sqlalchemy.Integer, primary_key=True)
  name = db.Column(sqlalchemy.String)

class EmployeeModel(Base):
  __tablename__ = 'employee'
  id = db.Column(sqlalchemy.Integer, primary_key=True)
  name = db.Column(sqlalchemy.String)
  hiread_on = db.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
  department_id = db.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('department.id'))
  department = relationship(
    DepartmentModel,
    backref=backref('employee', uselist=True, cascade='delete,all')
  )
