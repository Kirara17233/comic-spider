from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_comic = '_comic'
_category = '_category'
_chapter = '_chapter'
_mapping = '_mapping'

Base = declarative_base()
engine = create_engine('mysql://walker:0@192.168.1.108:3306/Comics?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)
