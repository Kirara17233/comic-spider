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
        session.add(Comic[source](id=comic['id'], name=comic['name'], author=comic['author'], update=comic['update']))
    save_category(source, comic['id'], comic['category_id'], session)


def save_category(source, comic_id, categories, session=DBSession()):
    for category in categories:
        old_category = session.query(Category[source]).filter_by(name=category['name']).first()
        if old_category:
            old_category.id = category['id']
            old_category.name = category['name']
            old_comic_category = session.query(ComicCategory[source]).filter_by(comic_id=comic_id, category_id=category['id'])
            if old_comic_category:
                old_comic_category.comic_id = comic_id
                old_comic_category.category_id = category['id']
            else:
                session.add(ComicCategory[source](comic_id=comic_id, category_id=category['id']))
        else:
            session.add(Category[source](id=category['id'], name=category['name']))
            session.add(ComicCategory[source](comic_id=comic_id, category_id=category['id']))
    session.commit()
    session.close()


def save_chapter(source, chapter):
    session = DBSession()
    new_chapter = session.query(Chapter[source]).filter_by(comic_id=chapter['comic_id'], id=chapter['id']).first()
    if new_chapter:
        new_chapter.comic_id = chapter['comic_id']
        new_chapter.id = chapter['id']
        new_chapter.name = chapter['name']
        new_chapter.size = chapter['size']
        new_chapter.code = chapter['code']
    else:
        session.add(Chapter[source](comic_id=chapter['comic_id'], id=chapter['id'], name=chapter['name'], size=chapter['size'], code=chapter['code']))
    session.commit()
    session.close()
