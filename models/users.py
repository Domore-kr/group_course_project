#Таблица Пользователи
import sqlalchemy as sq
from sqlalchemy.orm import relationship

from models.database import Base


class Users_list(Base):
    __tablename__ = 'users_list'

    id_key = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    user_URL = sq.Column(sq.String, nullable=False, unique=True)
    user_name = sq.Column(sq.String, nullable=False, unique=False)
    user_surname = sq.Column(sq.String, nullable=False, unique=False)
    users_favorite = relationship('Favorites_list', backref='users_list')
    users_photo = relationship('Photo_list', backref='users_list')
