from vk_methods import *
import json
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
from create_batabase import create_database, _load_fake_data

with open('information.json') as f:
    data: dict = json.load(f)
token: str = data['Token']
access_token: str = data['AccessToken']
bot = VkBot(token=token)
app = VkApp(token=access_token)
longpoll = VkLongPoll(bot)
keyboard = VkKeyboard()


def user_info():
    '''Отправляет пользователю сообщение с информацией, доступной на его странице'''

    data = bot.get_userdata(event.user_id)
    message = f"""Вас зовут {data['first_name']} {data['last_name']},
Ваш пол в виде id {data['sex']}
Вы из {data['city_title']}
Родились: {data['bdate']}"""
    bot.write_msg(event.user_id, message, keyboard)


def basic_search_scenario() -> list:
    '''Отправляет пользователю сообщения, содержащие имя, ссылку и три фото кандидатуры для знакомства'''

    parse: list = app.get_users(bot.get_userdata(event.user_id))['items']
    upper_barrier: int = len(parse) - 1
    parsed_person: dict = parse[randint(0, upper_barrier)]
    while parsed_person['is_closed']:
        parsed_person = parse[randint(0, upper_barrier)]
        # Затычка, если профиль скрыт
    name_list: list = [parsed_person['first_name'], parsed_person['last_name']]  # Список из имени и фамилли
    photo: dict = app.get_photo(parsed_person['id'])
    top_three: list = app.get_top_three(photo)
    message: str = ' '.join(name_list) + str(
        f'\nvk.com/id{parsed_person["id"]}\n')  # Сообщение для отправки ботом
    bot.write_msg(event.user_id, message, keyboard)
    bot.send_attachment(event.user_id, top_three)
    return [parsed_person, top_three]


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if request == 'Начать':
                bot.write_msg(event.user_id, f"Привет, Я чат-бот для знакомств", keyboard)
            elif request == 'Обо мне':
                user_info()
            elif request == 'Ищи':
                info = []
                info.append(basic_search_scenario())
                # Сюда по идее записывается информация для БД и дальше крутится в модуле create_batabase
            if request == "Добавить в избранное":
                create_database(user_info=info[0][0], user_photos=info[0][1])
                bot.write_msg(event.user_id, "Ну вроде записал", keyboard)
            elif request == "Показать избранное":
                bot.write_msg(event.user_id, "Пока((", keyboard)
            else:
                bot.write_msg(event.user_id, "Не поняла вашего ответа...", keyboard)
