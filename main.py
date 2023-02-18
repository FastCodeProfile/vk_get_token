import json
import asyncio
from contextlib import suppress

import aiohttp


class VK:
    """
    Класс для взаимодействия с ВК
    """
    def __init__(self, username: str, password: str) -> None:
        """
        Метод инициализации класса

        :param username: Логин аккаунта
        :param password: Пароль аккаунта
        """
        self.username = username
        self.password = password

    async def get_token(self) -> tuple[bool, dict | str]:
        """
        Метод для получения токена страницы ВК

        :return: tuple[bool, dict | str]
        """
        host = 'https://oauth.vk.com/token'
        params = dict(
            grant_type='password',
            client_id=6146827,
            client_secret='qVxWRF1CwHERuIrKBnqe',
            username=self.username,
            password=self.password,
            v=5.130
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url=host, params=params) as response:
                json_response = await response.json()
                if 'error' in json_response:
                    return False, json_response["error_description"]
                else:
                    return True, json_response


def file_input() -> dict:
    """
    Функция читает и возвращает словарь с логинами и паролями

    :return: dict
    """
    with open('./input.json', 'r') as file:
        return json.load(file)


def file_output(output_data: dict) -> None:
    """
    Функция записывает полученный список в файл

    :param output_data:
    :return: None
    """
    with open('./output.json', 'w') as file:
        json.dump(output_data, file)


async def main() -> None:
    """
    Главная функция запуска

    :return: None
    """
    output_data = {}
    input_data = file_input()  # Получаем словарь с логинами и паролями
    for key in input_data.keys():  # Перебираем словарь по его ключам
        account = input_data[key]
        vk = VK(username=account['username'], password=account['password'])  # Инициализируем класс
        status, response = await vk.get_token()  # Получаем токен страницы ВК
        if status:  # Если получение токена удалось
            data = dict(
                username=account['username'],
                password=account['password'],
                url_profile=f'https://vk.com/id{response["user_id"]}',
                access_token=response["access_token"]
            )
            output_data[key] = data
            print(f'Получен токен страницы - {data["url_profile"]}')
        else:  # Если получение токена не удалось
            print(f'Возникла ошибка аккаунта: {response}')

    file_output(output_data=output_data)  # Записываем полученные данные в файл


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):  # Игнорирование ошибок при остановке
        asyncio.run(main())  # Запуск асинхронной функции из синхронного контекста
