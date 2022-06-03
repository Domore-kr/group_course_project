from vk_methods import *
import json
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType

# with open('information.json') as f:
#     data: dict = json.load(f)
# token: str = data['Token']
# access_token: str = data['AccessToken']
token = '1fd5bbc8500c761628e07ae6ff8f2a61d7a36f3845d9381cba30e95a9f12949ad30bdda04e991b57cf17b'
access_token = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
bot = VkBot(token=token)
app = VkApp(token=access_token)
longpoll = VkLongPoll(bot)
keyboard = VkKeyboard()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if request == 'Начать':
                bot.write_msg(event.user_id, f"Привет, Я чат-бот для знакомств", keyboard)
            elif request == 'Обо мне':
                data = bot.get_userdata(event.user_id)
                bot.write_msg(event.user_id, f"""
                Вас зовут {data['first_name']} {data['last_name']},
                Ваш пол в виде id {data['sex']}
                Вы из {data['city_title']}
                Родились {data['bdate']}"""
                              , keyboard)
            elif request == 'Ищи':
                parse = app.get_users(bot.get_userdata(event.user_id))['items'][randint(0, 1000)]
                name_list = [parse['first_name'], parse['last_name']]  # Список из имени и фамилли
                photo = app.get_photo(parse["id"])['items'][0]['sizes'][-1]['url']
                message = ' '.join(name_list) + str(f'\nvk.com/id{parse["id"]}\n')\
                          + ' '.join(app.give_url(app.get_photo(parse["id"])['items']))  # Сообщение для отправки ботом
                bot.write_msg(event.user_id, message, keyboard)
            elif request == "Привет":
                bot.write_msg(event.user_id, f"Хай, {event.user_id}", keyboard)
            elif request == "Пока":
                bot.write_msg(event.user_id, "Пока((", keyboard)
            else:
                bot.write_msg(event.user_id, "Не поняла вашего ответа...", keyboard)

