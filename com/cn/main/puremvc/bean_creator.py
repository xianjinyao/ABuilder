# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

import com.cn.constants.package_path as constants
from com.cn.utils import path_kit
from com.cn.utils import property_kit
from com.cn.utils.db.mysql import MysqlObject
from com.cn.utils import java_data_kit
from com.cn.main import puremvc

MYSQL_MODE = "mysql"
MONGODB_MODE = "mongodb"


class CreateBean():
    def __init__(self, mode=MYSQL_MODE):
        self.package_path = ""
        self.remote_packages = []
        self.class_name = ""
        self.properties = []
        self.bean_methods = []
        self.mysql_obj = None
        if mode == MYSQL_MODE:
            self._get_mysql_object()

    def _get_mysql_object(self):
        if self.mysql_obj is None:
            self.mysql_obj = MysqlObject()

    def render_bean(self):
        template = puremvc.beanLookup.get_template("bean.java")
        args_map = {
            "packagePath": self.package_path,
            "remotePackages": self.remote_packages,
            "className": self.class_name,
            "properties": self.properties,
            "beanMethods": self.bean_methods
        }
        return template.render(**args_map)

    def set_package_path(self, package_path):
        self.package_path = package_path

    def set_class_name(self, class_name):
        self.class_name = class_name + "Bean"

    def add_property(self, name, authority="private", type="String"):
        properties_map = dict()
        properties_map["authority"] = authority
        properties_map["type"] = type
        properties_map["name"] = property_kit.under_score_case2camel_case(name)
        properties_map["defaultValue"] = self.get_default_value(type)
        self.properties.append(properties_map)

    def add_method(self, property_name, authority="public", return_type="String"):
        bean_method_map = dict()
        bean_method_map["authority"] = authority
        bean_method_map["returnType"] = return_type
        bean_method_map["propertyName"] = property_kit.under_score_case2camel_case(property_name)
        self.bean_methods.append(bean_method_map)

    def get_default_value(self, type):
        return java_data_kit.get_default_value(type)

    def create_bean_in_mysql(self, package_path, db_name, table_name, need_method=True):
        self.set_package_path(package_path)

        properties_list = self.mysql_obj.get_table_columns_detail_list(db_name, table_name)
        for detail in properties_list:
            type = java_data_kit.get_type(str(detail[1]))
            if "Timestamp".__eq__(type):   # the datetime also timestamp
                if not self.is_package_import(constants.TIMESTAMP_PACKAGE):
                    self.remote_packages.append(constants.TIMESTAMP_PACKAGE)
            elif "Date".__eq__(type):
                if not self.is_package_import(constants.DATE_PACKAGE):
                    self.remote_packages.append(constants.DATE_PACKAGE)
            elif "Time".__eq__(type):
                if not self.is_package_import(constants.TIME_PACKAGE):
                    self.remote_packages.append(constants.TIME_PACKAGE)
            self.set_class_name(property_kit.under_score_case2whole_camel_case(table_name))
            self.add_property(str(detail[0]), type=type)
            if need_method:
                self.add_method(str(detail[0]), return_type=type)
        return self.render_bean()

    def is_package_import(self, remote_package):
        if remote_package in self.remote_packages:
            return True
        else:
            return False

    def get_bean_properties_map(self):
        return self.properties


def print_bean_java(package_path, db_name, table_name):
    create_bean = CreateBean()
    result = eval("create_bean.create_bean_in_" + MYSQL_MODE + "(package_path, db_name, table_name)")#, need_method=False)
    print(result)


def save_bean_java(package_path, db_name, table_name):
    create_bean = CreateBean()
    result = create_bean.create_bean_in_mysql(package_path, db_name, table_name)
    filename = property_kit.under_score_case2whole_camel_case(table_name) + "Bean.java"
    path = path_kit.get_file_path(path_kit.OUTPUT_PATH, "bean", filename)
    path_kit.make_it_exist(path)
    f = open(path, "a+")
    f.write(result)
    f.close()


if __name__ == "__main__":
    print(path_kit.is_file("templates/bean.java"))
    # print_bean_java("com.cn", "", "")