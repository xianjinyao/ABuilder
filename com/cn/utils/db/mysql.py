# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

import MySQLdb

from com.cn.utils.map_kit import *
from com.cn.utils.path_kit import *
from com.cn.utils.string_kit import *
from com.cn.utils.property_kit import *
from pyquery import PyQuery as pq

MYSQL_CONFIG_PATH = get_file_path(CONFIG_PATH, "mysql_config.xml")


class MysqlObject:
    _tables_map = None

    def __init__(self):
        self.name = ""
        self.host = ""
        self.port = 0
        self.db = ""
        self.username = ""
        self.password = ""
        self.charset = ""
        self._mysql_cursor = None
        self.init()

    def get_cursor(self):
        config = {
            "host": self.host,
            "port": str2int(self.port),
            "user": self.username,
            "passwd": self.password,
            "db": self.db,
            "charset": self.charset
        }
        try:
            conn = MySQLdb.connect(**config)
            cursor = conn.cursor()
            return cursor
        except Exception, e:
            print("Built connection error: " + e.message)
            exit(-1)

    def init(self):
        template = pq(filename=MYSQL_CONFIG_PATH)
        alias = template("alias")
        self.name = alias.text()
        connect_url = template("connect-url")
        self.host = connect_url.text()
        port = template("port")
        self.port = port.text()
        db = template("db")
        self.db = db.text()
        username = template("username")
        self.username = username.text()
        password = template("password")
        self.password = password.text()
        charset = template("charset")
        self.charset = charset.text()
        if self._mysql_cursor is None:
            self._mysql_cursor = self.get_cursor();

    def show_tables(self):
        list = []
        result = self._mysql_cursor.execute("SHOW TABLES;")
        for table in self._mysql_cursor.fetchall():
            list.append(table[0])
        return list

    '''
    return {"column_name": (column_detail)[, "column_name".....]}
        column_detail:  1. name 2. type 3. comment
    '''
    def get_table_columns_detail_list(self, db_name, table_name, data_type=True, column_comment=False):
        sql = "SELECT column_name"
        if data_type:
            sql += ",data_type"
            if column_comment:
                sql += ","
        if column_comment:
            sql += "column_comment"
        sql += " FROM information_schema.columns WHERE table_name='" + table_name + "' AND table_schema='" + db_name + "'"
        result = self._mysql_cursor.execute(sql)
        return fetch2list(self._mysql_cursor.fetchall())

    '''
    return {"table_name": [column_name]}
    '''
    def get_table_map(self, db_name, table_name):
        table_map = dict()
        result_map = self.get_table_columns_detail_map(db_name, table_name)
        table_map[table_name] = result_map.keys()
        return table_map

    def get_tables_map(self):
        if self._tables_map is None:
            self._tables_map = dict()
        for table_name in self.show_tables():
            map = self.get_table_map(self.db, table_name)
            self._tables_map[table_name] = map[table_name]
        return self._tables_map

    def __del__(self):
        try:
            self._mysql_cursor.close()
        except:
            print("Close mysql connection error")
            exit(-1)


if __name__ == "__main__":
    mysql_object = MysqlObject()
    print(mysql_object.get_tables_map())#mysql_object.get_table_columns_detail_map("contract_type", "dms"))