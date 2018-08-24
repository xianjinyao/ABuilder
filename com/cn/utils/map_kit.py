# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''


def fetch2map(fetch):
    map = dict()
    for item in fetch:
        map[item[0]] = item
    return map


def fetch2list(fetch):
    list = []
    for item in fetch:
        list.append(item)
    return list