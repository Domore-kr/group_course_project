from vk_methods import *
import json
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType

with open('information.json') as f:
    data: dict = json.load(f)
token: str = data['Token']
access_token: str = data['AccessToken']
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
                while parse['is_closed'] == True:
                    parse = app.get_users(bot.get_userdata(event.user_id))['items'][randint(0, 1000)]
                    '''
                    Затычка, если профиль скрыт
                    '''
                url = app.give_url(app.get_photo(parse["id"])['items'])
                app.download_photo(url)
                name_list = [parse['first_name'], parse['last_name']]  # Список из имени и фамилли
                photo = app.get_photo(parse["id"])['items'][0]['sizes'][-1]['url']
                message = ' '.join(name_list) + str(f'\nvk.com/id{parse["id"]}\n') \
                          + ' '.join(url)  # Сообщение для отправки ботом
                bot.write_msg(event.user_id, message, keyboard)
            elif request == "Привет":
                bot.write_msg(event.user_id, f"Хай, {event.user_id}", keyboard)
            elif request == "Пока":
                bot.write_msg(event.user_id, "Пока((", keyboard)
            else:
                bot.write_msg(event.user_id, "Не поняла вашего ответа...", keyboard)
