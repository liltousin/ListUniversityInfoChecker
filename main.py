from config import TOKEN
from aiogram import Dispatcher, Bot, executor, types
from bs4 import BeautifulSoup
import requests
import re


def checker(src):
    soup = BeautifulSoup(src, "lxml")
    src_name = soup.find('h3', class_='display-6').text
    items = soup.find_all('tr', {'class': 'table-warning'})
    my_id = int(soup.find('td', text=re.compile('184-339-743 00')).find_parent().find('td').text)
    pre_items = []
    for i in items:
        if int(i.find('td').text) < my_id:
            pre_items.append(i)
    return f'{src_name}\t Человек выше меня: {len(pre_items)}'


def downloader(url):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    return requests.get(url, headers=headers).text


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
urls = [
    'https://lists.rosnou.ru/64/1/1222',
    'https://lists.rosnou.ru/64/1/1224',
    'https://lists.rosnou.ru/64/1/1234'
]


@dp.message_handler(commands='start')
async def start(message: types.Message):
    messages = []
    for URL in urls:
        source = downloader(URL)
        message = checker(source)
        messages.append(message)
    await message.reply('\n'.join(messages))


if __name__ == '__main__':
    executor.start_polling(dp)
