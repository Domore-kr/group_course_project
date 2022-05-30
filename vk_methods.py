import vk_api
from random import randrange


class VkBot(vk_api.VkApi):
    def write_msg(self, user_id: int, message: str) -> None:
        """Метод для отправки сообщений"""
        self.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
    
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
            'user_id': user_id, # пускай будет, да
            'first_name': response['first_name'],
            'last_name': response['last_name'],
            'sex': response['sex'],
            'city_id': response['city']['id'],
            'city_title': response['city']['title'],
            'bdate': response['bdate']
        }
        return userdata
    

    
    def get_users(self, user_data: dict) -> dict:
        """Метод для поиска людей из того же города, что и пользователь,
        принимает аргумент с словарем полученным из метода get_userdata"""
        sex_table: dict = { # это не про секс на столе
            '1': 2,
            '2': 1
        }
        user_sex: str = user_data['sex']
        required_sex: str = sex_table[user_sex]
        city_id: str = user_data['city_id']
        results: list = self.method('users.search', {
            'city': city_id, 
            'sex': required_sex, 
            'has_photo': 1}
            )
        return results
        # перечитать с утра, дописать, отдебажить
        