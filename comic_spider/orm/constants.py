from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_category = '_category'
_chapter = '_chapter'
_mapping = '_mapping'

engine = create_engine('mysql+pymysql://walker:0@192.168.1.108:3306/Comics?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)
