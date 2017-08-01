#! /usr/bin/env python3

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

import os.path

Base = declarative.declarative_base()

class Source(Base):
    __tablename__ = 'sources'

    id              = sql.Column(sql.Integer, primary_key = True)
    title           = sql.Column(sql.Text)
    author          = sql.Column(sql.Text)
    journal         = sql.Column(sql.Text)
    booktitle       = sql.Column(sql.Text)
    volume          = sql.Column(sql.Text)
    number          = sql.Column(sql.Text)
    pages           = sql.Column(sql.Text)
    year            = sql.Column(sql.Text)
    additional      = sql.Column(sql.Text)
    entry_type      = sql.Column(sql.Text)


session = None
def init():
    create_new = os.path.isfile('bib.db')
    print(create_new)

    engine = sql.create_engine('sqlite:///bib.db')

    if create_new:
        Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    DBSession = orm.sessionmaker(bind = engine)

    global session
    session = DBSession()
