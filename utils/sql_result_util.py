"""
对数据库查询结果做处理的工具
"""
from django.db.models import QuerySet
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def result_to_list(query_set):
    sql_result_list = []
    for data in query_set:
        data_dict = {}
        for field in query_set.columns:
            data_dict[field] = getattr(data, field)
        sql_result_list.append(data_dict)
    return sql_result_list


def list_to_dict(obj_list, pop_fields=None, foreign_key_field=None, foreign_key_field_rename=None,
                 pop_foreign_key_fields=None):
    '''
    :param obj_list: 需要转换成字典的QuerySet集合
    :param pop_fields: 需要移除的key的列表
    :param foreign_key_field: 外键关联的对象key
    :param foreign_key_field_rename: 转换为字典时，外键关联的对象起一个新的名字（没有新名字时则使用旧名字）
    :param pop_foreign_key_fields: 外键关联的对象key下需要移除的key的列表
    :return:
    '''
    tmp_list = list()
    for obj in obj_list:
        tmp_dict = obj.__dict__
        if foreign_key_field:
            assert hasattr(obj, foreign_key_field)
            tmp_dict_field = getattr(obj, foreign_key_field).__dict__
            tmp_dict_field.pop("_state")
            if pop_foreign_key_fields:
                for field in pop_foreign_key_fields:
                    tmp_dict_field.pop(field)
            if foreign_key_field_rename:
                tmp_dict[foreign_key_field_rename] = tmp_dict_field
            else:
                tmp_dict[foreign_key_field] = tmp_dict_field
        tmp_dict.pop("_state")

        if pop_fields:
            for field in pop_fields:
                tmp_dict.pop(field)
        tmp_list.append(tmp_dict)
    return tmp_list
