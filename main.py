from vk_methods import *
import json

from vk_api.longpoll import VkLongPoll, VkEventType
with open ('information.json') as f:
    data: dict = json.load(f)
token: str = data['Token']
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