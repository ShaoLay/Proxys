#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Hamdi
class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经空了!')

class ResourceDepletionError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理资源已用尽!')