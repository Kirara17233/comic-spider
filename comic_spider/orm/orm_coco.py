from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, SMALLINT, VARCHAR, DATE, CHAR

from comic_spider.source import coco
from comic_spider.orm.constants import _category, _chapter, _mapping


class Comic(declarative_base()):
    __tablename__ = coco

    id = Column(SMALLINT, primary_key=True, nullable=True)
    name = Column(VARCHAR, nullable=True)
    author = Column(VARCHAR)
    update = Column(DATE, nullable=True)
    category = Column(CHAR, nullable=True)


class Category(declarative_base()):
    __tablename__ = coco + _category

    name = Column(VARCHAR, primary_key=True, nullable=True)
    id = Column(SMALLINT, primary_key=True, nullable=True, autoincrement=True)


class Chapter(declarative_base()):
    __tablename__ = coco + _chapter

    comic_id = Column(SMALLINT, primary_key=True, nullable=True)
    id = Column(SMALLINT, primary_key=True, nullable=True)
    name = Column(VARCHAR)


class Mapping(declarative_base()):
    __tablename__ = coco + _mapping

    name = Column(VARCHAR, primary_key=True, nullable=True)
    code = Column(VARCHAR, primary_key=True, nullable=True)
