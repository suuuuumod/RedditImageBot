# Импортируем необходимые библиотеки
import requests
import time
from datetime import datetime, timedelta
import telebot
import json

# Инициализируем бота с помощью токена
bot = telebot.TeleBot('YOU_BOT_TOKEN_HERE')

# ID чата, в который бот будет отправлять изображения
chat_id = 'YOU_CHAT_ID_HERE'

# Пытаемся загрузить уже отправленные изображения из файла
try:
    with open('sent_memes.json', 'r') as file:
        sent_memes = set(json.load(file))
except FileNotFoundError:
    # Если файл не найден, используем пустое множество
    sent_memes = set()

# Бесконечный цикл для проверки новых изображений
while True:
    try:
        # Получаем новые посты с Reddit
        response = requests.get('https://www.reddit.com/r/memes/new.json', headers={'User-agent': 'Mozilla/5.0'})
        data = response.json()

        # Проверяем каждый пост
        for post in data['data']['children']:
            # Получаем URL изображения
            meme_url = post['data']['url']

            # Получаем дату публикации поста
            meme_date = datetime.fromtimestamp(post['data']['created_utc'])

            # Если пост был опубликован не более недели назад и его URL еще не был отправлен в чат
            if meme_date > datetime.now() - timedelta(weeks=1) and meme_url not in sent_memes:
                # Отправляем изображение в чат
                bot.send_photo(chat_id, meme_url)

                # Добавляем URL изображения в множество отправленных изображений
                sent_memes.add(meme_url)

                # Сохраняем множество отправленных изображений в файл
                with open('sent_memes.json', 'w') as file:
                    json.dump(list(sent_memes), file)

                # Пауза в 5 минут после каждого отправленного изображения
                time.sleep(300)  # 5 минуты = 300 секунд

    except Exception as e:
        # Выводим информацию об ошибке, если она возникла
        print(f'Error: {e}')
