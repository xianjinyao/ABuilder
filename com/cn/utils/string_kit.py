# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

import string


def first_char_upper(str):
    return str[0].upper() + str[1:]


def str2int(str):
    return string.atoi(str)


def is_valid(str):
    if str is None or "".__eq__(str):
        return False
    return True


def str_join(str_list, pattern):
    return pattern.join(str_list)


def map2str(map):
    list = []
    for key, value in map.items():
        str = "\"%s\": " % key + ("%d" % value if type(value) == int else "\"%s\"" % value)
        list.append(str)
    return "{" + str_join(list, ", ") + "}"
