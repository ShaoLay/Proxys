#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Hamdi
import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent, FakeUserAgentError
import random


def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN, zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    print('正在获取中.....', url)
    try:
        r = requests.get(url, headers=headers)
        print('获取结果:', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('爬虫失败！', url)
        return None

class Downloader(object):
    """
    一个一部下载器, 可以对代理源异步抓取, 但是容易被BAN
    """
    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls