"""Создание подключения к БД и объявление базы"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.config import host, user, password, db_name

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{db_name}', pool_pre_ping=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_database():
    Base.metadata.create_all(engine)
