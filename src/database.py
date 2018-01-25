import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

import os.path, re

Base = declarative.declarative_base()

class Source(Base):
    __tablename__ = 'sources'

    id          = sql.Column(sql.Integer, primary_key = True)
    title       = sql.Column(sql.Text)
    author      = sql.Column(sql.Text)
    journal     = sql.Column(sql.Text)
    booktitle   = sql.Column(sql.Text)
    volume      = sql.Column(sql.Text)
    number      = sql.Column(sql.Text)
    pages       = sql.Column(sql.Text)
    year        = sql.Column(sql.Text)
    note        = sql.Column(sql.Text)
    school      = sql.Column(sql.Text)
    entry_type  = sql.Column(sql.Text)
    keywords    = sql.Column(sql.Text)
    summary     = sql.Column(sql.Text)

    def list_entry(self):
        return '{}, {}{}'.format(self.author_surnames(), strip_for_display(self.title), ', {}'.format(self.year) if self.year else '')

    def author_surnames(self):
        surnames = [strip_for_display(x.split(',')[0]) for x in self.author.split(' and ')]
        if len(surnames) == 1:
            return surnames[0]
        return ' and '.join([', '.join(surnames[:-1]), surnames[-1]])

    def pdf_file_name(self):
        return strip_for_filename(self.title) + '.pdf'

    def cite_name(self):
        author_low = re.sub('([^a-zA-Z0-9])+', '', self.author.split(',')[0]).lower()
        if self.year != None:
            return author_low + self.year
        return author_low

    def bibtex(self):
        bib = '@{}{{{},\n'.format(self.entry_type, self.cite_name())
        for field in fields:
            if getattr(self, field) != None:
                bib += '    {} = "{}",\n'.format(field, getattr(self, field))
        return bib + '}\n'

    def is_deleted(self):
        return sql.inspect(self).detached

fields =   [
                'title',
                'author',
                'journal',
                'booktitle',
                'volume',
                'number',
                'pages',
                'year',
                'note',
                'school'
            ]

def strip_for_display(text):
    return re.sub('([^a-zA-Z0-9\-: ])+', '', text)

def strip_for_filename(text):
    return re.sub(':', ' -', strip_for_display(text))

def query_author(author):
    return session.query(Source).filter(Source.author.ilike('%{}%'.format(author))).all()

def query_title(title):
    return session.query(Source).filter(Source.title.ilike('%{}%'.format(title))).all()

def query_keyword(keywords):
    result = session.query(Source)
    for key in keywords:
        if key[0] != '!':
            result = result.filter(Source.keywords.ilike('%{}%'.format(key)))
        else:
            result = result.filter(~Source.keywords.ilike('%{}%'.format(key[1:])))
    return result.all()

def contains(source):
    return len(session.query(Source).filter_by(title = source.title).filter_by(author = source.author).all()) > 0

def get_all():
    return session.query(Source).order_by(Source.author).all()

session = None
def init():
    engine = sql.create_engine('sqlite:///bib.db')

    if not os.path.isfile('bib.db'):
        Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    DBSession = orm.sessionmaker(bind = engine)

    global session
    session = DBSession()
