#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль содержит в себе набор
методов для взаимодействия с API
"""

# built-in
import json
import pymongo
from aiohttp import web


async def get_posts(request):
    """
    Метод отдает имеющуюся информацию
    о новостях по внешнему запросу
    """

    cursor = request.app["db"].news.find({}, {'_id': False})

    # По-умолчанию вызвращаем 5 крайних записей
    cursor.sort("_id", pymongo.DESCENDING)
    cursor.limit(5)

    params = request.rel_url.query
    if params:
        order_type = pymongo.ASCENDING
        if "order" in params:
            if params["order"] not in ("asc", "desc"):
                return web.json_response(
                    text="Failed request. Order params must be asc or desc",
                    status=422)
            if params["order"] == "desc":
                order_type = pymongo.DESCENDING
        if "sort" in params:
            if params["sort"] not in ("id", "url", "title", "created"):
                return web.json_response(
                    text="Sorting is possible only by fields (id, url, title, created)",
                    status=422)
            cursor.sort(params["sort"], order_type)
        if "offset" in params:
            if not params["offset"].isdigit() or int(params["offset"]) > 1000:
                return web.json_response(
                    text="Failed. Parameter offset must be non-negative integer",
                    status=422)
            cursor.skip(int(params["offset"]))
        if "limit" in params:
            if not params["limit"].isdigit():
                return web.json_response(
                    text="Failed. Parameter limit must be non-negative integer",
                    status=422)
            if int(params["limit"]) > 1000:
                return web.json_response(
                    text="Failed. Parameter limit is very big( >1000 )",
                    status=422)
            cursor.limit(int(params["limit"]))

    result = [item async for item in cursor]
    return web.json_response(
        dumps=json.dumps,
        content_type='application/json',
        body=json.dumps(result),
        status=200)
