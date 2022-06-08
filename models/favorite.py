"""Таблица Избранные"""
import sqlalchemy as sq

from models.database import Base


class Favorites_list(Base):
    __tablename__ = 'favorites_list'

    id_key = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users_list.id_key'), nullable=False, unique=True)