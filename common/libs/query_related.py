# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:59 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : query_related.py
# @Software: PyCharm

import sqlalchemy
from sqlalchemy import or_, and_, func
from flask_sqlalchemy.model import DefaultMeta

from common.libs.set_app_context import set_app_context


def page_size(page: int = None, size: int = None, **kwargs) -> (int, int):
    """

    :param page: -> int
    :param size: -> int
    :param kwargs: {"page":1,"size":20}
    :return:
    """
    page = page if page and isinstance(page, int) else int(kwargs.get('page', 0))
    size = size if size and isinstance(size, int) else int(kwargs.get('size', 10))
    page = (page - 1) * size if page != 0 else 0
    return page, size


@set_app_context
def general_query(model: type, page: int, size: int, like_rule: str = "and_", field_list: list = [],
                  query_list: list = [], where_dict: dict = {}, in_field_list: list = None, in_value_list: list = None,
                  field_order_by: str = None) -> dict:
    """
    通用分页模糊查询
    :param model: -> DefaultMeta
    :param field_list: 模糊查询的字段列表 如: ['id','username'], 结合如下`query_list`使用
    :param query_list: 模糊查询入参列表,对应表字段的位置 如: ['id','username'] 对应 [1,'yyx']
    :param where_dict: where条件, {"id":1,"username":"yyx"...} 即: select ... where id=1 and username="yyx";
    :param like_rule: like规则,目前仅支持使用其中一个 -> and_; or_;
    :param in_field_list: in语句的字段列表 如: ['id','username'], 结合如下`in_value_list`使用
    :param in_value_list: in语句的入参列表 如: ['id','username'] 即: [[1,2,3],['y1','y2','y3']] select ... where id in (1,2,3) and username in ('y1','y2','y3')";
    :param field_order_by: order_by字段名称
    :param page: 页数 -> {"page":1,"size":20}
    :param size: 条数 -> {"page":1,"size":20}
    :return:

    """

    if not isinstance(model, DefaultMeta):
        raise TypeError('类型错误 -> model 应该是 -> flask_sqlalchemy.model.DefaultMeta')

    if not isinstance(page, int) or not isinstance(size, int):
        raise TypeError('类型错误 -> page 和 size 应该是 -> int')

    if like_rule not in ['and_', 'or_']:
        raise TypeError('参数错误 -> like_rule 应该是 -> and_ 或者 or_')

    if not isinstance(field_list, list):
        raise TypeError('类型错误 -> field_list 应该是 -> list ')

    if not isinstance(query_list, list):
        raise TypeError('类型错误 -> query_list 应该是 -> list')

    in_list = []

    if in_field_list and isinstance(in_field_list, list) and in_value_list and isinstance(in_value_list, list):
        for i in in_value_list:
            if not isinstance(i, list) or not i:
                raise TypeError('类型错误 -> in_value_list 里面的值应该是 -> list 而且不能为空')

        for index, field in enumerate(in_field_list):
            in_list.append(getattr(model, str(field)).in_(in_value_list[index]))

    like_rule_func = getattr(sqlalchemy, like_rule)

    like_list = []
    for index, field in enumerate(field_list):
        query_var = query_list[index]
        _like = getattr(model, str(field)).ilike("%{}%".format(query_var if query_var else ''))
        like_list.append(_like)

    # 忽略null或空字符串的查询
    where_list = [getattr(model, key) == val for key, val in where_dict.items() if val or isinstance(val, int)]

    result = getattr(model, 'query').filter(
        like_rule_func(*like_list) if like_list else and_(True),  # 模糊查询
        *where_list,  # where 条件
        *in_list  # in 条件
    ).order_by(
        getattr(model, 'update_time').desc() if not field_order_by else getattr(model, field_order_by).desc()
    ).paginate(
        page=int(page),
        per_page=int(size),
        error_out=False
    )
    result_list = [res.to_json() for res in result.items]
    total = result.total
    result_data = {
        'records': result_list,
        'now_page': page,
        'total': total
    }
    return result_data