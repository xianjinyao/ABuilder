# -*- coding: utf-8 -*-
'''
@author jinyao.xian
PS: This module support properties named way is Camel Case
'''

import com.cn.utils.property_kit as property_kit
from com.cn.constants import sql_sth
from com.cn import sql


def build_insert_presql(table_name, properties_list):
    properties_str = ", ".join(properties_list)
    sql = "INSERT INTO " + table_name + " ( " + properties_str + " ) VALUES ( "
    is_first = True
    for property in properties_list:
        if is_first:
            sql += "?"
            is_first = False
        elif property_kit.is_equal(property, "create_time"):
            sql += ", now()"
        else:
            sql += ", ?"
    sql += " )"
    return sql


def build_update_presql(table_name, properties_list, need_id=True, need_status=True):
    sql = "UPDATE " + table_name + " SET "
    plist = list(map(lambda str: str + " = ?", properties_list))
    sql += ", ".join(plist)
    if need_id or need_status:
        sql += " WHERE "
    if need_id:
        sql += properties_list[0] + " = ?"
    if need_status and "status" in list(map(lambda str: str.lower(), properties_list)):
        if need_id and need_status:
            sql += " AND "
        sql += "status = ?"
    return sql


def build_select_presql(table_name, properties_list=None, cond_list=None, group_by_list=None, order_by_map=None):
    sql = "SELECT "
    if len(properties_list) is None:
        sql += "*"
    else:
        sql += ", ".join(properties_list)
    sql += " FROM " + table_name
    if cond_list is not None:
        sql += " WHERE " + " AND ".join(list(map(lambda name: name + " = ?", cond_list)))
    if group_by_list is not None:
        sql += " GROUP BY " + ", ".join(group_by_list)
    if order_by_map is not None:
        sql += " ORDER BY " + ", ".join(list(map(lambda name: name + " " + order_by_map[name], order_by_map.keys())))
    return sql


class CreateQuerySQL:
    def __init__(self, table_name, is_pre=False):
        self.properties_list = []
        self.table_name = table_name
        self.cond_map = None
        self.group_by_list = None
        self.order_by_map = None
        self.limit_offset = None
        self.is_pre = is_pre

    def compile(self):
        template = sql.sqlLookup.get_template("select.sql")
        data = {
            "properties_list": self.properties_list,
            "table_name": self.table_name,
            "cond_map": self.cond_map,
            "group_by_list": self.group_by_list,
            "order_by_map": self.order_by_map,
            "limit_offset": self.limit_offset,
            "is_pre": self.is_pre
        }
        return template.render(**data)

    def clone(self):
        obj = CreateQuerySQL(self.table_name, is_pre=self.is_pre)
        obj.properties_list = self.properties_list
        obj.cond_map = self.cond_map
        obj.group_by_list = self.group_by_list
        obj.order_by_map = self.order_by_map
        obj.limit_offset = self.limit_offset
        obj.is_pre = self.is_pre
        return obj

    def convert(self, property_name):
        return property_kit.camel_case2under_score_case(property_name)

    def property(self, *property):
        obj = self.clone()
        self.properties_list.extend(list(map(lambda str: self.convert(str), property)))
        return obj

    def cond(self, **cond_map):
        obj = self.clone()
        _cond_map = dict(zip(list(map(lambda str: obj.convert(str), cond_map.keys())),
                            list(map(lambda s: str(s) if type(s) == int else "\"" + s + "\"", cond_map.values()))))
        if obj.cond_map is None:
            obj.cond_map = _cond_map
        else:
            if type(obj.cond_map) == dict:
                obj.cond_map = dict(obj.cond_map, **_cond_map)
            else:
                obj.cond_map = _cond_map
        return obj

    def group_by(self, *group):
        obj = self.clone()
        if obj.group_by_list is None:
            obj.group_by_list = []
        obj.group_by_list.extend(list(map(obj.convert, group)))
        return obj

    '''
    1 for asc, 0 for desc
    '''
    def order_by(self, **order_map):
        obj = self.clone()
        if obj.order_by_map is None:
            obj.order_by_map = dict()
        for key, value in order_map.items():
            obj.order_by_map[obj.convert(key)] = sql_sth.ORDER_ASC if value == 1 else sql_sth.ORDER_DESC
        return obj

    '''
    limit need a tuple ( from, count ), and offset need a int
    PS: if you use offset, please set limit int
    '''
    def limit_offset(self, limit=(), offset=0):
        obj = self.clone()
        if type(limit) != tuple:
            limit = (int(limit),)
        if obj.limit_offset is None:
            obj.limit_offset = {}
        obj.limit_offset["limit"] = tuple(map(lambda i: str(i), limit))
        if len(limit) == 1:
            obj.limit_offset["offset"] = str(offset)
        return obj

    def __dict__(self):
        return {
            "properties_list": self.properties_list,
            "table_name": self.table_name,
            "cond_map": self.cond_map,
            "group_by_list": self.group_by_list,
            "order_by_map": self.order_by_map,
            "limit_offset": self.limit_offset,
            "is_pre": self.is_pre
        }


if __name__ == "__main__":
    # print build_update_presql("a", ["helloId", "1", "2", "createTime", "statu"])
    # print(build_select_presql("table_name", properties_list=["id", "name", "password", "status"], cond_list=["id", "status"], order_by_map={"id": ORDER_BY_ASC, "name": ORDER_BY_DESC}))
    # print(path_kit.is_file("templates/select.sql"))
    create_query_sql = CreateQuerySQL("tableName")
    print(create_query_sql.compile())
    print(create_query_sql.__dict__)
