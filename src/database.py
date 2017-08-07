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
        return '{}, {}{}'.format(self.author_surnames(), self.display_title(), ', {}'.format(self.year) if self.year else '')

    def author_surnames(self):
        surnames = [x.split(',')[0] for x in self.author.split(' and ')]
        if len(surnames) == 1:
            return surnames[0]
        return ' and '.join([', '.join(surnames[:-1]), surnames[-1]])

    def display_title(self):
        return re.sub('([^a-zA-Z0-9\-: ])+', '', self.title)

    def pdf_file_name(self):
        return re.sub('([^a-zA-Z0-9\- ])+', '', self.title) + '.pdf'

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

def query_author(author):
    return session.query(Source).filter(Source.author.ilike('%{}%'.format(author))).all()

def query_title(title):
    return session.query(Source).filter(Source.title.ilike('%{}%'.format(title))).all()

def query_keyword(keyword):
    return session.query(Source).filter(Source.keywords.ilike('%{}%'.format(keyword))).all()

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
