<%! from com.cn.filters.nosql import mongo_filters %>db.${ collection }.find(${ mongo_filters.map2str(query) if query else "" })${ ".pretty()" if is_pretty else "" }