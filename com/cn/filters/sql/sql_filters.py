# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

from com.cn.utils.property_kit import camel_case2under_score_case
from com.cn.utils import string_kit


'''
build str for build sql
'''
def build_properties_str(properties_list):
    if properties_list is None or len(properties_list) <= 0:
        return "*"
    else:
        return string_kit.str_join(properties_list, ", ")


def build_cond_str(cond_map, is_pre):
    if cond_map is None or len(cond_map.keys()) <= 0:
        return ""
    if is_pre:
        str_list = list(map(lambda str: str + " = ?", cond_map.keys()))
    else:
        str_list = list(map(lambda str: str + " = " + cond_map[str], cond_map.keys()))
    return " WHERE " + string_kit.str_join(str_list, " AND ")


def build_group_str(group_by_list):
    if group_by_list is None or len(group_by_list) <= 0:
        return ""
    return " GROUP BY " + string_kit.str_join(group_by_list, ", ")


def build_order_str(order_by_map):
    if order_by_map is None or len(order_by_map.keys()) <= 0:
        return ""
    return " ORDER BY " + string_kit.str_join(list(map(lambda name: name + " " + order_by_map[name], order_by_map.keys())), ", ")


def build_limit_str(limit_offset_map):
    if limit_offset_map is None or "limit" not in limit_offset_map.keys():
        return ""
    return " LIMIT " + string_kit.str_join(limit_offset_map["limit"], ", ")


def build_offset_str(limit_offset_map):
    if limit_offset_map is None or "offset" not in limit_offset_map.keys():
        return ""
    return " OFFSET " + limit_offset_map["offset"]
