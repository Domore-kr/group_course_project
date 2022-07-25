"""Создание БД"""
from models.database import create_db, Session
from models.users import Users_list
from models.favorite import Favorites_list
from models.photoes import Photo_list

# create_database()


from faker import Faker


def create_database(user_info, user_photos, load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        _load_fake_data(Session(), user_info, user_photos)


def _load_fake_data(session: Session, user_info: dict, user_photos: list):

    user_list = [user_info['id'], f'vk.com/id{user_info["id"]}', user_info['first_name'], user_info['last_name']]

    user_favorite = Users_list(
        user_id=user_list[0],
        user_URL=user_list[1],
        user_name=user_list[2],
        user_surname=user_list[3]
    )
    session.add(user_favorite)

    favorites = Favorites_list(user_id=user_list[0])
    session.add(favorites)

    for photo in user_photos:
        session.add(Photo_list(user_id=user_list[0], photo_URL=f'photo{photo["owner_id"]}_{photo["id"]}'))

    session.commit()
    session.close()
