"""
对数据库查询结果做处理的工具
"""


def result_to_list(query_set):
    sql_result_list = []
    for data in query_set:
        data_dict = {}
        for field in query_set.columns:
            data_dict[field] = getattr(data, field)
        sql_result_list.append(data_dict)
    return sql_result_list
