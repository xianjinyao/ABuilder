# -*- coding: utf-8 -*-
'''
@author jinyao.xian
@filename mongo_client_cmd_creator
'''

import com.cn.utils.property_kit as property_kit
from com.cn import nosql


class BaseMongo:
    def __init__(self):
        pass

    def get_content(self, **content_map):
        return content_map


class QueryCmdCreator(BaseMongo):
    def __init__(self, collection):
        self.collection = collection
        self.query = None
        self.is_pretty = False

    def clone(self):
        obj = QueryCmdCreator(self.collection)
        obj.query = self.query
        obj.is_pretty = self.is_pretty
        return obj

    def compile(self):
        template = nosql.nosqlLookup.get_template("mongo_find.cmd")
        data = {
            "collection": self.collection,
            "query": self.query,
            "is_pretty": self.is_pretty
        }
        return template.render(**data)

    def pretty(self):
        obj = self.clone()
        obj.is_pretty = True
        return obj

    def find(self, **query):
        obj = self.clone()
        if obj.query is None:
            obj.query = query
        else:
            if type(obj.query) == dict:
                obj.query = dict(obj.query, **query)
            else:
                obj.query = query
        return obj


if __name__ == "__main__":
    query = QueryCmdCreator("aaa")
    print(query.find(id=3, name="hahaha").find(password="123").pretty().compile())
