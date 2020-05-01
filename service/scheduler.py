#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Модуль содержит в себе методы планировщика
"""

# built-in
import asyncio


def run(interval):
    """
    Данный декоратор позволяет выполнять
    метод с указанной периодичностью в секундах
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            while True:
                await func(*args, **kwargs)
                await asyncio.sleep(interval)
        return wrapper
    return decorator
