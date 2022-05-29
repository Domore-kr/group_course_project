import vk_api
from random import randrange

class VkBot(vk_api.VkApi):
    def write_msg(self, user_id: int, message: str) -> None:
        self.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
    
    def get_userdata(self, user_id: int) -> dict:
        response: list = self.method('users.get', {'user_id': user_id, 'fields': 'sex, city, relation, bdate'})
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