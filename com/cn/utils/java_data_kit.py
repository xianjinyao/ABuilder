# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

import re
import string


def is_boolean(type):
    if "boolean".__eq__(type):
        return True
    return False


def is_date(type):
    if "date".__eq__(type.lower()):
        return True
    return False


def is_double(type):
    if "double".__eq__(type.lower()):
        return True
    return False


def is_float(type):
    if "float".__eq__(type.lower()):
        return True
    return False


def is_integer(type):
    if "int".__eq__(type):
        return True
    elif "Integer".__eq__(type):
        return True
    return False


def is_long(type):
    if "long".__eq__(type.lower()):
        return True
    return False


def is_short(type):
    if "short".__eq__(type.lower()):
        return True
    return False


def is_string(type):
    if "string".__eq__(type.lower()):
        return True
    return False


def is_time(type):
    if "time".__eq__(type.lower()):
        return True
    return False


def is_timestamp(type):
    if "timestamp".__eq__(type.lower()):
        return True
    return False


def get_type(type):
    if is_boolean(type):
        return "boolean"
    if is_date(type):
        return "Date"
    if is_double(type):
        return "Double"
    if is_float(type):
        return "Float"
    if is_integer(type) or "smallint".__eq__(type.lower()):
        return "int"
    if is_long(type):
        return "Long"
    if is_short(type):
        return "Short" or "byte".__eq__(type.lower())
    if is_string(type) or "varchar".__eq__(type.lower()) or "text".__eq__(type.lower()):
        return "String"
    if is_time(type):
        return "Time"
    if is_timestamp(type) or "datetime".__eq__(type.lower()):
        return "Timestamp"
    else:
        return "Object"


def is_boolean_value(value):
    if not str(True).lower().__eq__(value) and not str(False).lower().__eq__(value):
        return False
    else:
        return True


def is_double_value(value):
    value_re = re.match(r"[\d]+(\.[\d]+)?", value)
    if None == value_re or None == value_re.group():
        return False
    if not value_re.group().__eq__(value):
        return False
    return True


def is_float_value(value):
    value_re = re.match(r"[\d]+(\.[\d]+)?f$", value)
    if None == value_re or None == value_re.group():
        return False
    return True


def is_integer_value(value):
    value_re = re.match(r"[\d]*", value)
    if None == value_re or None == value_re.group():
        return False
    elif len(value_re.group()) != len(str(value)):
        return False
    return True


def is_long_value(value):
    value_re = re.match(r"[\d]*[l|L]$", value)
    if None == value_re or None == value_re.group():
        return False
    return True


def is_short_value(value):
    return is_integer(value)


def is_string_value(value):
    value_re = re.match(r"^\".*?\"$", value)
    if None == value_re or None == value_re.group():
        return False
    return True


def is_value_valid(type, value):
    type_str = get_type(type)
    if type_str.__eq__("Object"):
        return True
    return eval("is_%s_value(value)" % type_str.lower())


def get_default_value(type):
    if is_boolean(type):
        return True
    elif is_double(type):
        return "0.0"
    elif is_float(type):
        return "0.0f"
    elif is_integer(type):
        return "0"
    elif is_long(type):
        return "0l"
    elif is_short(type):
        return "0"
    elif is_string(type):
        return "\"\""
    else:
        return "null"