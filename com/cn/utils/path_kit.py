# -*- coding: utf-8 -*-
'''
@author jinyao.xian
'''

import re
import os
import platform
import com.cn.utils.string_kit as string_kit


def get_separator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


def get_file_path(path, *args):
    return os.path.join(path, *args)


def is_path_exist(path):
    paths = os.path.split(path)
    if len(paths) == 2 and "." in paths[1]:
        path = paths[0]
    return os.path.exists(path)


def is_file(path):
    return os.path.isfile(path)


def get_father_path(path):
    return os.path.split(path)[0]


def make_it_exist(path):
    if MAIN_PATH not in path:
        return False
    paths = os.path.split(path)
    if len(paths) == 2 and "." in paths[1]:
        path = paths[0]
    path_re = re.match(MAIN_PATH+"(.*)", path)
    if path_re is None:
        return False
    path_name = path_re.group(1).split(get_separator())
    main_path = MAIN_PATH
    for name in path_name:
        if string_kit.is_valid(name):
            main_path = get_file_path(main_path, name)
            if is_path_exist(main_path) is False:
                os.mkdir(main_path)
                print('Successfully created directory: \"%s\"' % path)
    return True


MAIN_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
CONFIG_PATH = os.path.join(MAIN_PATH, "config")
UTILS_PATH = os.path.join(MAIN_PATH, "com", "cn", "utils")
OUTPUT_PATH = os.path.join(MAIN_PATH, "output")
