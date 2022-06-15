import vk_api
import datetime
from random import randrange
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from pprint import pprint


class VkBot(vk_api.VkApi):

    def write_msg(self, user_id: int, message: str, keyboard) -> None:
        """Метод для отправки сообщений"""
        keyboard = VkKeyboard()
        keyboard.add_button('Привет', VkKeyboardColor.POSITIVE)
        keyboard.add_button('Обо мне', VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Ищи', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Пока', VkKeyboardColor.NEGATIVE)
        self.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'keyboard': keyboard.get_keyboard()
        }
                    )

    def get_userdata(self, user_id: int) -> dict:
        """Метод получает информацию о текущем пользователе, который обращается к боту.
        user_id удобнее заполнять через события получаемые в vk_api.longpoll
        см. код в main.py"""
        response: list = self.method('users.get', {
            'user_id': user_id,
            'fields': 'sex, city, relation, bdate'}
                                     )
        response: dict = response[0]
        userdata: dict = {
            'user_id': user_id,  # пускай будет, да
            'first_name': response['first_name'],
            'last_name': response['last_name'],
            'sex': response['sex'],
            'city_id': response['city']['id'],
            'city_title': response['city']['title'],
            'bdate': response['bdate']
        }
        return userdata

    def send_attachment(self, user_id: int, photos: list) -> None:
        """Принимает в себя список фотографий, высылает их как вложение"""
        if len(photos) == 3:
            first_photo = 'photo' + str(photos[0]['owner_id']) + '_' + str(photos[0]['id'])
            second_photo = 'photo' + str(photos[1]['owner_id']) + '_' + str(photos[1]['id'])
            third_photo = 'photo' + str(photos[2]['owner_id']) + '_' + str(photos[2]['id'])
            self.method('messages.send', {
                'user_id': user_id,
                'attachment': f'{first_photo},{second_photo},{third_photo}',
                'random_id': randrange(10 ** 7)
            }
                        )
        elif len(photos) == 2:
            first_photo = 'photo' + str(photos[0]['owner_id']) + '_' + str(photos[0]['id'])
            second_photo = 'photo' + str(photos[1]['owner_id']) + '_' + str(photos[1]['id'])
            self.method('messages.send', {
                'user_id': user_id,
                'attachment': f'{first_photo},{second_photo}',
                'random_id': randrange(10 ** 7)
            }
                        )
        elif len(photos) == 1:
            first_photo = 'photo' + str(photos[0]['owner_id']) + '_' + str(photos[0]['id'])
            self.method('messages.send', {
                'user_id': user_id,
                'attachment': f'{first_photo}',
                'random_id': randrange(10 ** 7)
            }
                        )
        else:
            pass


class VkApp(vk_api.VkApi):

    def get_users(self, user_data: dict) -> dict:
        """Метод для поиска людей из того же города, что и пользователь,
        принимает аргумент с словарем полученным из метода get_userdata"""
        sex_table: dict = {  # таблица для того, чтобы поиск шел по противоположному полу
            1: 2,
            2: 1
        }
        try: # если есть дата рождения, то идёт распарсинг
            bdate: str = user_data['bdate']
            splitted_bdate: list = bdate.split(sep='.')
            if len(splitted_bdate) == 3:
                bdate: int = int(splitted_bdate[2])
        except KeyError:
            bdate: None = None
        user_sex: int = user_data['sex']
        required_sex: int = sex_table[user_sex]
        city_id: int = user_data['city_id']
        search_params: dict = {
            'count': 1000,
            'offset': 0,
            'status': 1,
            'city': city_id,
            'sex': required_sex,
            'has_photo': 1
        }
        if bdate is None:
            pass
        else:
            current_date: int = datetime.date.today().year
            difference = current_date - bdate
            min_age = difference - 3
            if min_age < 18:
                min_age = 18
            max_age = difference + 3
            search_params.update({'age_from': min_age, 'age_to': max_age})
            # посчитать минимальный и максимальный возраст, вставить их в search_params
        results: list = self.method('users.search', search_params)
        return results

    def get_photo(self, id: int) -> dict:
        """Метод возвращает список фотографий в профиле по id пользователя"""
        results: list = self.method('photos.get', {
            'owner_id': id,
            'album_id': 'profile',
            'offset': 0,
            'extended': 1,
            'count': 1000,
            'photo_sizes': 1
        }
                                    )
        return results

    def get_top_three(self, photos: dict) -> list:
        """Метод принимает список с фотографиями пользователя,
        возвращает список из трех с наибольшим числом лайков"""
        top_three: list = []
        count: int = 0 # Счетчик для записи фото в словарь
        id_dict: dict = {} # словарь, где ключ - порядковый номер в списке фото, а значение - количество лайков

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        for i in photos['items']:
            #Перебирает фотки и создает словарь, где ключ - порядковый номер в списке фото, а значение - количество лайков
            id_dict[count] = i['likes']['count']
            count += 1

        if len(id_dict) < 3:
            photos: list = photos['items']
            top_three: list = []
            first_entry: dict = photos.pop(0)
            top_three.append(first_entry)
            for entry in photos:
                if entry['likes']['count'] >= top_three[0]['likes']['count']:
                    top_three.insert(0, entry)
                if len(top_three) == 4:
                    top_three.pop(3)
            return top_three
        else:
            while len(top_three) < 3:
                '''
                Перебирает словарь с лайками и добавляет в список на возврат самые залайканые фото 
                '''
                top_three.append(photos['items'][get_key(id_dict, max(id_dict.values()))])
                id_dict.pop(get_key(id_dict, max(id_dict.values())), max(id_dict.values()))
            return top_three
