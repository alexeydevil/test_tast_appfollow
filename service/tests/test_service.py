#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import json
import pytest
import random
import aiohttp

import const
import background_task


FAILED_PARAMS = [
    "?limit=pi",
    "?limit=-1",
    "?limit=-1.9",
    "?limit=-1000000000",
    "?offset=pi",
    "?offset=-1",
    "?offset=-1.9",
    "?order=test",
    "?order=123",
    "?sort=test"

]

SUCCESS_PARAMS = [
    "?limit=10",
    "?offset=10",
    "?limit=10&offset=10",
    "?sort=id",
    "?order=desc",
    "?sort=id&order=desc",
    "?sort=created&order=desc&limit=10&offset=10",
]

@pytest.mark.asyncio
async def test_params():
    async with aiohttp.ClientSession() as client:
        for item in FAILED_PARAMS:
            async with client.get("http://127.0.0.1:{}/posts{}".format(const.PORT, item)) as resp:
                assert resp.status == 422
        for item in SUCCESS_PARAMS:
            async with client.get("http://127.0.0.1:{}/posts{}".format(const.PORT, item)) as resp:
                assert resp.status == 200


@pytest.mark.asyncio
async def test_result_consist():
    async with aiohttp.ClientSession() as client:
        async with client.get("http://127.0.0.1:{}/posts{}".format(const.PORT, SUCCESS_PARAMS[2])) as resp:
            result = await resp.json()
            max_id = max([int(item["id"]) for item in result])
            assert resp.status == 200
            assert len(result) == 10
            assert max_id >= 10

        async with client.get("http://127.0.0.1:{}/posts{}".format(const.PORT, SUCCESS_PARAMS[0])) as resp:
                    assert resp.status == 200
                    assert len(await resp.json()) == 10


@pytest.mark.asyncio
async def test_consist_bd():
    posts = await background_task.news()
    await background_task.update_news()
    async with aiohttp.ClientSession() as client:
        params = "?sort=created&order=desc&limit={}".format(len(posts))
        async with client.get("http://127.0.0.1:{}/posts{}".format(const.PORT, params)) as resp:
            result = await resp.json()
            urls = [item["url"] for item in result]
            assert random.choice(posts)["url"] in urls
