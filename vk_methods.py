import vk_api
from random import randrange
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from pprint import pprint
import urllib.request


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
            'keyboard': keyboard.get_keyboard(),
            'attachment': f'photo{user_id}_https://sun9-west.userapi.com/sun9-52/s/v1/if1/lkMZBVuZF6Z-04ilvDS8KYBBBVSSviHS7Fxf3gl78ZsuvYCtySrKGjOmB_6cE-02izh-gQ.jpg?size=720x480&quality=96&type=album_a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
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
            'has_photo': 1,
            'fields': {'is_closed': False},
            'can_access_closed': False,
            'is_closed': False
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

    def download_photo(self, url):
        count = 1
        for i in url:
            img = urllib.request.urlopen(i).read()
            out = open(f"img{count}.jpg", "wb")
            out.write(img)
            out.close()
            count += 1
