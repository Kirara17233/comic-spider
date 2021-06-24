from sqlalchemy import Column, SMALLINT, VARCHAR

from comic_spider.orm.constants import Base, DBSession
from comic_spider.orm.dictionaries import Comic, Category, ComicCategory, Chapter


class URL(Base):
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


def has_chapter(source, comic_id, chapter_info):
    result = False
    chapter = None
    session = DBSession()
    if isinstance(chapter_info, int):
        chapter = session.query(Chapter[source]).filter_by(comic_id=comic_id, id=chapter_info).first()
    elif isinstance(chapter_info, str):
        chapter = session.query(Chapter[source]).filter_by(comic_id=comic_id, name=chapter_info).first()
    if chapter:
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
    else:
        session.add(Comic[source](id=comic['id'],
                                  name=comic['name'],
                                  author=comic['author'],
                                  update=comic['update']))
    session.commit()
    session.close()


def save_category(source, category):
    session = DBSession()
    if session.query(Category[source]).filter_by(id=category['id']).first():
        if not session.query(ComicCategory[source]).filter_by(comic_id=category['comic_id'], category_id=category['id']).first():
            session.add(ComicCategory[source](comic_id=category['comic_id'], category_id=category['id']))
    else:
        session.add(Category[source](id=category['id'], name=category['name']))
        session.add(ComicCategory[source](comic_id=category['comic_id'], category_id=category['id']))
    session.commit()
    session.close()


def save_chapter(source, chapter):
    session = DBSession()
    if not session.query(Chapter[source]).filter_by(comic_id=chapter['comic_id'], id=chapter['id']).first():
        session.add(Chapter[source](comic_id=chapter['comic_id'],
                                    id=chapter['id'],
                                    name=chapter['name'],
                                    size=chapter['size'],
                                    code=chapter['code']))
    session.commit()
    session.close()
