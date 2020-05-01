"""
Модуль описывает константы
используемые сервисом
"""

import os

PORT = int(os.getenv("SERVICE_PORT") or 8000) # Порт на котором работает сервис
MAIN_URL = "https://news.ycombinator.com/" # Url для получения новостей
USER_AGENT = r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
MONGO_URL = "mongodb://{}:{}".format("172.16.0.14", 27017) # Url для подключения к БД mongo
BACKGROUND_TASK_INTERVAL = 20 # Время повтора задачи по получению новостей в секундах
