from sqlalchemy import Column, SMALLINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

from comic_spider.orm.constants import DBSession
from comic_spider.orm.dictionaries import Comic, Category, Chapter, Mapping


class URL(declarative_base()):
    __tablename__ = 'source'

    id = Column(SMALLINT, primary_key=True, nullable=True, autoincrement=True)
    code = Column(VARCHAR, primary_key=True, nullable=True)
    name = Column(VARCHAR, nullable=True)
    protocol = Column(VARCHAR, nullable=True)
    third_level_domain = Column(VARCHAR, nullable=True)
    domain = Column(VARCHAR, nullable=True)


def get_source(source):
    session = DBSession()
    url = session.query(URL).filter_by(code=source).first()
    session.close()
    return url


def get_categories(source):
    session = DBSession()
    categories = {}
    for category in session.query(Category[source]).all():
        categories[category.name] = category.id
    session.close()
    return categories


def add_category(source, category_name):
    session = DBSession()
    category = Category[source](name=category_name)
    session.add(category)
    session.commit()
    category_id = category.id
    session.close()
    return category_id


def has_mapping(source, chapter_name):
    result = False
    session = DBSession()
    if session.query(Mapping[source]).filter_by(name=chapter_name).first():
        result = True
    session.close()
    return result


def save_comic(source, comic):
    session = DBSession()
    old_comic = session.query(Comic[source]).filter_by(id=comic['id']).first()
    if old_comic:
        old_comic.name = comic['name']
        old_comic.author = comic['author']
        old_comic.update = comic['update']
        old_comic.category = comic['category']
        session.commit()
    else:
        session.add(Comic[source](id=comic['id'], name=comic['name'], author=comic['author'], update=comic['update'], category=comic['category']))
        session.commit()
    session.close()


def save_chapter(source, chapter):
    session = DBSession()
    if not session.query(Chapter[source]).filter_by(comic_id=chapter['comic_id'], id=chapter['id']).first():
        session.add(Chapter[source](comic_id=chapter['comic_id'], id=chapter['id'], name=chapter['name']))
        session.commit()
    session.close()


def save_mapping(source, mapping):
    session = DBSession()
    session.add(Mapping[source](name=mapping['name'], code=mapping['code']))
    session.commit()
    session.close()
