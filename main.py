from vk_methods import *
import json
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
from my_database import insert_db, select_db, select_db_photos, create_table_db

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


def parsed_person() -> list:
    '''Функция формирует словарь, содержащий информацию о фаворите, а также три лучшие фотографии'''
    parse: list = app.get_users(bot.get_userdata(event.user_id))['items']
    upper_barrier: int = len(parse) - 1
    parsed_person: dict = parse[randint(0, upper_barrier)]
    while parsed_person['is_closed']:
        parsed_person = parse[randint(0, upper_barrier)]
        # Затычка, если профиль скрыт
    name_list: list = [parsed_person['first_name'], parsed_person['last_name']]  # Список из имени и фамилли
    photo: list = app.get_photo(parsed_person['id'])
    top_three: list = app.get_top_three(photo)
    return [name_list, parsed_person, top_three]


def basic_search_scenario(information):
    '''Отправляет пользователю сообщения, содержащие имя, ссылку и три фото кандидатуры для знакомства

    param information: словарь, содержащий информацию о пользователе, а также три лучшие фотографии

    '''
    message: str = ' '.join(information[0]) + str(
        f'\nvk.com/id{information[1]["id"]}\n')  # Сообщение для отправки ботом
    bot.write_msg(event.user_id, message, keyboard)
    bot.send_attachment(event.user_id, information[2])


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if request == 'Начать':
                bot.write_msg(event.user_id, f"Привет, Я чат-бот для знакомств", keyboard)
            elif request == 'Обо мне':
                user_info()
            elif request == 'Ищи':
                information = parsed_person()
                basic_search_scenario(information)
            elif request == "Добавить в избранное":
                create_table_db()
                insert_db(information, bot.get_userdata(event.user_id)['user_id'])
                bot.write_msg(event.user_id, "Ну вроде записал", keyboard)
            elif request == "Показать избранное":
                for favorites in select_db(bot.get_userdata(event.user_id)['user_id']):
                    message: str = ' '.join(favorites[4:6]) + str(
                        f'\n{favorites[6]}\n')
                    bot.write_msg(event.user_id, message, keyboard)
                    bot.send_attachment(bot.get_userdata(event.user_id)['user_id'], select_db_photos(favorites[2]))
            else:
                bot.write_msg(event.user_id, "Не поняла вашего ответа...", keyboard)
