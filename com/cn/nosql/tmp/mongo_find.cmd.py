# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1535104189.060636
_enable_loop = True
_template_filename = 'templates/mongo_find.cmd'
_template_uri = 'mongo_find.cmd'
_source_encoding = 'ascii'
_exports = []


from com.cn.filters.nosql import mongo_filters 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        query = context.get('query', UNDEFINED)
        is_pretty = context.get('is_pretty', UNDEFINED)
        collection = context.get('collection', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'db.')
        __M_writer(unicode( collection ))
        __M_writer(u'.find(')
        __M_writer(unicode( mongo_filters.map2str(query) if query else "" ))
        __M_writer(u')')
        __M_writer(unicode( ".pretty()" if is_pretty else "" ))
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"37": 31, "16": 1, "18": 0, "26": 1, "27": 1, "28": 1, "29": 1, "30": 1, "31": 1}, "uri": "mongo_find.cmd", "filename": "templates/mongo_find.cmd"}
__M_END_METADATA
"""
