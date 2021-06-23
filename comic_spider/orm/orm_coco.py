from sqlalchemy import Column, SMALLINT, VARCHAR, DATE

from comic_spider.source import coco
from comic_spider.orm.constants import Base, _comic, _category, _chapter


class Comic(Base):
    __tablename__ = coco

    id = Column(SMALLINT, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False)
    author = Column(VARCHAR, nullable=True)
    update = Column(DATE, nullable=False)


class Category(Base):
    __tablename__ = coco + _category

    id = Column(SMALLINT, primary_key=True, nullable=False)
    name = Column(VARCHAR, primary_key=True, nullable=False)


class ComicCategory(Base):
    __tablename__ = coco + _comic + _category

    comic_id = Column(SMALLINT, primary_key=True, nullable=False)
    category_id = Column(SMALLINT, primary_key=True, nullable=False)


class Chapter(Base):
    __tablename__ = coco + _chapter

    comic_id = Column(SMALLINT, primary_key=True, nullable=False)
    id = Column(SMALLINT, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False)
    size = Column(SMALLINT, nullable=False)
    code = Column(VARCHAR, nullable=False)
