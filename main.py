from http.client import responses
from random import randrange

import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
with open ('information.json') as f:
    data: dict = json.load(f)
token: str = data['Token']

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

vk = VkBot(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            
            if request == 'Начать':
                vk.write_msg(event.user_id, f"Привет, Я чат-бот для знакомств")
            elif request == 'Обо мне':
                data = vk.get_userdata(event.user_id)
                vk.write_msg(event.user_id, f"""
                Вас зовут {data['first_name']} {data['last_name']},
                Ваш пол в виде id {data['sex']}
                Вы из {data['city_title']}
                Родились {data['bdate']}"""
                )
            elif request == "привет":
                vk.write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                vk.write_msg(event.user_id, "Пока((")
            else:
                vk.write_msg(event.user_id, "Не поняла вашего ответа...")