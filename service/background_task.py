#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль содержит в себе middleware методы
"""

# built-in
from datetime import datetime

import asyncio
import pymongo
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient

# service
import const
import scheduler



async def update_news():
    """
    Данный метод вставляет в
    базу новости которых там еще нет
    """

    posts = await news()

    # Получаем id крайнего элемента в коллекции,
    # для его корректной итерации для новых записей
    current_db = AsyncIOMotorClient(const.MONGO_URL).appfollow
    lost_document = await current_db.news.find_one({}, sort=[('_id', pymongo.DESCENDING)])
    lost_id = 1
    if lost_document:
        lost_id = lost_document.get("id", 1)

    # Вставлять записи будем по одной,
    # т.к. на коллекции стоит ограничивающий индекс
    for pos, item in enumerate(posts):
        item["id"] = pos + lost_id
        try:
            await current_db.news.insert_one(item)
        except pymongo.errors.DuplicateKeyError:
            continue


async def news():
    """
    Метод получает указанную страницу новостей,
    вытягивает из нее новости со ссылками
    и отправляет на запись в БД полученные новости
    """
    async with ClientSession(headers={'User-Agent': const.USER_AGENT}) as session:
        async with session.get(const.MAIN_URL) as response:
            content = await response.content.read()

    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table")

    posts = []
    for row in table.findAll("a", {"class": "storylink"}, href=True):
        posts.append({
            "url": row.get("href"),
            "title": row.get_text(),
            "created": datetime.now().replace(microsecond=0).isoformat()
        })

    return posts


@scheduler.run(const.BACKGROUND_TASK_INTERVAL)
async def autoupdate_news():
    await update_news()


async def start_background_tasks(app):
    """
    Middleware task.
    Метод инициализирует все необходимые
    для сервиса соединения и задачи
    """
    app["mongodb_instance"] = AsyncIOMotorClient(const.MONGO_URL)
    app["db"] = app["mongodb_instance"].appfollow
    app["db"].news.create_index(
        [("url", pymongo.DESCENDING), ("title", pymongo.DESCENDING)],
        unique=True)
    app["periodic_task"] = asyncio.create_task(autoupdate_news())


async def cleanup_background_tasks(app):
    """
    Graceful shutdown
    """
    print("cleanup background tasks...")

    # gracefully closing underlying connection
    app["mongodb_instance"].close()
    app["periodic_task"].cancel()
