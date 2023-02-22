import asyncio
import json
from contextlib import suppress

import aiohttp
from loguru import logger


class VkApi:
    def __init__(self, username: str, password: str) -> None:
        self.host = 'https://oauth.vk.com/token'
        self.params = {"v": 5.131}
        self.username = username
        self.password = password

    async def get_token(self) -> tuple[bool, str | dict]:
        self.params["client_id"] = 6146827
        self.params["grant_type"] = "password"
        self.params["username"] = self.username
        self.params["password"] = self.password
        self.params["client_secret"] = "qVxWRF1CwHERuIrKBnqe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.host, params=self.params) as response:
                json_response = await response.json()
                if 'error' in json_response:
                    return False, json_response["error_description"]
                else:
                    return True, json_response


def load_data(filename: str) -> list[str]:
    with open(filename, encoding='utf-8') as file:
        return file.readlines()


def dump_data(filename: str, data: dict) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


async def main() -> None:
    output_data = {}
    data = load_data('data.txt')
    for index, user in enumerate(data):
        username, password = user.strip('\n').split(':')
        vk_api = VkApi(username, password)
        result = await vk_api.get_token()
        if result[0]:
            user_data = dict(
                user_id=result[1]["user_id"],
                username=username,
                password=password,
                url_profile=f'https://vk.com/id{result[1]["user_id"]}',
                access_token=result[1]["access_token"]
            )
            output_data[str(index)] = user_data
            logger.success(f'Получен токен страницы - {user_data["url_profile"]}')
        else:
            logger.error(f'Возникла проблема "{result[1]}"')

    dump_data('data.json', output_data)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
