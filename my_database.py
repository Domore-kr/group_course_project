import psycopg2
from config import host, user, password, db_name


def create_table_db() -> None:
    '''

    Метод для заполнения базы данныз таблицами

    '''
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                '''
                CREATE TABLE if not exists Favorites (
                id_favorites serial primary key,
                Name VARCHAR(20) NOT NULL,
                Surname VARCHAR(20) NOT NULL,
                URL VARCHAR(40) NOT NULL
                );

                CREATE TABLE if not exists Users (
                id serial primary key,
                user_id integer not null,
                favorite_id integer references Favorites(id_favorites)
                );

                CREATE TABLE if not exists Photos (
                favorite_id integer references Favorites(id_favorites),
                photo_id integer,
                photo_owner_id integer
                );
                '''
            )
            connection.commit()

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()


def insert_db(information: list, user_id: int) -> None:
    '''
    Метод для заполнения БД данным об избранных фаворитах
    Parameters
    ----------
    information: список, содержащий данные о фаворите
    user_id: id текущего пользователя

    Returns
    -------

    '''
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                INSERT INTO Favorites(id_favorites, Name, Surname, URL)
                values(
                        {information[1]['id']},
                        '{information[0][0]}',
                        '{information[0][1]}',
                        'vk.com/id{information[1]["id"]}'
                        );
                
                INSERT INTO Users(user_id, favorite_id)
                values(
                        {user_id},
                        {information[1]['id']}
                        );
                        
                INSERT INTO Photos(favorite_id, photo_id, photo_owner_id)
                values
                        (
                        {information[1]['id']},
                        {information[2][0]['id']},
                        {information[2][0]['owner_id']}
                        ),
                        (
                        {information[1]['id']},
                        {information[2][1]['id']},
                        {information[2][1]['owner_id']}
                        ),
                        (
                        {information[1]['id']},
                        {information[2][2]['id']},
                        {information[2][2]['owner_id']}
                        );
                
                '''
            )
            connection.commit()

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()


def select_db(user_id) -> list:
    '''
    Метод для вывода информации из БД об избранных фаворитов
    Parameters
    ----------
    user_id: id текущего пользователя

    Returns
    -------

    '''
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT *
                FROM users AS u
                JOIN favorites AS f ON u.favorite_id = f.id_favorites
                WHERE user_id = {user_id}
                '''
            )
            return cursor.fetchall()


    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()


def select_db_photos(favorite_id) -> list:
    '''
    Метод для вывода ключевой информации к фотографиям
    Parameters
    ----------
    favorite_id: id фаворита

    Returns
    -------

    '''
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT photo_id, photo_owner_id
                FROM photos AS p
                JOIN favorites AS f ON p.favorite_id = f.id_favorites
                WHERE favorite_id = {favorite_id}
                '''
            )

            photos = []
            for photo in cursor.fetchall():
                photos.append({'id': photo[0], 'owner_id': photo[1]})
            return photos


    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()
