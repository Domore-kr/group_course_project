"""Создание БД"""
from models.database import create_database, Session
from models.users import Users_list
from models.favorite import Favorites_list
from models.photoes import Photo_list


create_database()