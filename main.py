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

def user_info():
    data = bot.get_userdata(event.user_id)
    message = f"""Вас зовут {data['first_name']} {data['last_name']},
Ваш пол в виде id {data['sex']}
Вы из {data['city_title']}
Родились {data['bdate']}"""
    bot.write_msg(event.user_id, message, keyboard)

def basic_search_scenario():
    parse: list = app.get_users(bot.get_userdata(event.user_id))['items']
    upper_barrier: int = len(parse) - 1
    parsed_person: dict = parse[randint(0, upper_barrier)]
    while parsed_person['is_closed'] == True:
        parsed_person = parse[randint(0, upper_barrier)]
        # Затычка, если профиль скрыт
    name_list: list = [parsed_person['first_name'], parsed_person['last_name']]  # Список из имени и фамилли
    photo: dict = app.get_photo(parsed_person['id'])
    top_three: list = app.get_top_three(photo)
    message: str = ' '.join(name_list) + str(
        f'\nvk.com/id{parsed_person["id"]}\n')  # Сообщение для отправки ботом
    bot.write_msg(event.user_id, message, keyboard)
    bot.send_attachment(event.user_id, top_three)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if request == 'Начать':
                bot.write_msg(event.user_id, f"Привет, Я чат-бот для знакомств", keyboard)
            elif request == 'Обо мне':
                user_info()
            elif request == 'Ищи':
                basic_search_scenario()
            elif request == "Привет":
                bot.write_msg(event.user_id, f"Хай, {event.user_id}", keyboard)
            elif request == "Пока":
                bot.write_msg(event.user_id, "Пока((", keyboard)
            else:
                bot.write_msg(event.user_id, "Не поняла вашего ответа...", keyboard)
