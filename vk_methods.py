import vk_api
from random import randrange
from pprint import pprint


class VkBot(vk_api.VkApi):

    def write_msg(self, user_id: int, message: str) -> None:
        """Метод для отправки сообщений"""
        self.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

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


class VkApp(vk_api.VkApi):

    def get_users(self, user_data: dict) -> dict:
        """Метод для поиска людей из того же города, что и пользователь,
        принимает аргумент с словарем полученным из метода get_userdata"""
        sex_table: dict = {  # это не про секс на столе
            1: 2,
            2: 1
        }
        user_sex: int = user_data['sex']
        required_sex: int = sex_table[user_sex]
        city_id: int = user_data['city_id']
        results: list = self.method('users.search', {
            'count': 1000,
            'offset': 0,
            'status': 1,
            'city': city_id,
            'sex': required_sex,
            'has_photo': 1
        }
                                    )
        # pprint(results)
        return results

    def get_photo(self, id) -> list: # Дает всю информацию о фото
        results: list = self.method('photos.get', {
            'owner_id': id,
            'album_id': 'profile',
            'offset': 0,
            'extended': 1,
            'count': 1000,
            'photo_sizes': 1
        }
                                    )
        # pprint(results)
        return results

    def give_url(self, get_photo) -> list: # Возвращает список url с наибольшим количеством лайков
        url = []
        count = 0
        id_dict = {}

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        for i in get_photo:
            id_dict[count] = i['likes']['count']
            count += 1

        while len(url) < 3:
            url.append(get_photo[get_key(id_dict, max(id_dict.values()))]['sizes'][-1]['url'])
            id_dict.pop(get_key(id_dict, max(id_dict.values())), max(id_dict.values()))
        return url
