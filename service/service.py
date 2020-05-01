#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль запуска сервиса
"""

# built-in
from aiohttp import web

# service
import task
import const
import background_task

routes = web.RouteTableDef()


def init():
    """
    Запускаем веб приложение для
    обслуживания пославленных задач
    """

    app = web.Application()
    app.on_startup.append(background_task.start_background_tasks)
    app.on_cleanup.append(background_task.cleanup_background_tasks)
    app.router.add_get("/posts", task.get_posts)
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(init(), port=const.PORT)
