#Таблица Фотографии
import sqlalchemy as sq

from models.database import Base


class Photo_list(Base):
    __tablename__ = 'photo_list'

    id_key = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users_list.id_key'), nullable=False, unique=True)
    photo_URL = sq.Column(sq.String, nullable=False, unique=True)