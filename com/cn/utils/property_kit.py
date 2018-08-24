# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

from string_kit import first_char_upper


def camel_strcat(str_1, str_2):
    return str_1 + first_char_upper(str_2)


def under_score_case2camel_case(str):
    sub_strs = str.split("_")
    return reduce(camel_strcat, sub_strs)


def under_score_case2whole_camel_case(str):
    return first_char_upper(under_score_case2camel_case(str))


def camel_case2under_score_case(str):
    def make_it_easy(c):
        if ord(c) <= 90:
            return "_" + c.lower()
        return c
    return "".join(list(map(make_it_easy, str)))


'''
source must be under score case
'''
def is_equal(target, source):
    if source.__eq__(target.lower()):
        return True
    if under_score_case2camel_case(source).__eq__(target):
        return True
    if under_score_case2whole_camel_case(source).__eq__(target):
        return True
    return False
