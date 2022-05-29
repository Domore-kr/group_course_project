import datetime
import requests
from information import *


class User:
    def __init__(self, URL: str, param: dict):
        self.url = URL
        self.params = param

    def results(self) -> dict:
        res = requests.get(self.url, params=self.params)
        return res.json()

    def age(self) -> int or None:
        try:
            return datetime.datetime.today().date().year - \
                   datetime.datetime.strptime(self.results()['response'][0]['bdate'], "%d.%m.%Y").year
        except:
            return None

    def first_name(self) -> str:
        return self.results()['response'][0]['first_name']

    def last_name(self) -> str:
        return self.results()['response'][0]['last_name']

    def sex(self) -> str:
        if self.results()['response'][0]['sex'] == 1:
            return 'Woman'
        elif self.results()['response'][0]['sex'] == 2:
            return 'Man'
        else:
            return 'Пол не указан'

    def city(self) -> str or None:
        try:
            return self.results()['response'][0]['city']['title']
        except:
            return None

    def relation(self) -> str or None:
        try:
            if self.results()['response'][0]['relation'] == 0:
                return 'Не указано'
            elif self.results()['response'][0]['relation'] == 1:
                return 'Не женат/Не замужем'
            elif self.results()['response'][0]['relation'] == 2:
                return 'Есть друг/Есть подруга;'
            elif self.results()['response'][0]['relation'] == 3:
                return 'Помолвлен/Помолвлена'
            elif self.results()['response'][0]['relation'] == 4:
                return 'Женат/Замужем'
            elif self.results()['response'][0]['relation'] == 5:
                return 'Всё сложно'
            elif self.results()['response'][0]['relation'] == 6:
                return 'В активном поиске'
            elif self.results()['response'][0]['relation'] == 7:
                return 'Влюблён/Влюблена'
            elif self.results()['response'][0]['relation'] == 8:
                return 'В гражданском браке'
        except:
            return None


if __name__ == '__main__':
    main = User(URL, params)
