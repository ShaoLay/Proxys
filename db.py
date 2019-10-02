#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Lay Shao
import redis

from error import PoolEmptyError
from settings import HOST, PORT, PASSWORD


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        从redis数据库中获取代理池
        :param count:
        :return:
        """
        proxies = self._db.lrange("proxies:", 0, count - 1)
        self._db.ltrim("proxies:", count, -1)
        return proxies

    def put(self, proxy):
        """
        往redis添加代理
        :param proxy:
        :return:
        """
        self._db.rpush("proxies：", proxy)

    def pop(self):
        """
        获取代理
        :return:
        """
        try:
            return self._db.rpop("proxies:").decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        获取队列长度
        :return:
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        清空数据库
        :return:
        """
        self._db.flushall()

if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())


