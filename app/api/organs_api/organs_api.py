# -*- coding: utf-8 -*-
# @Time    : 2023/7/19 11:31
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : organs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.organs.models import Organs


class OrgansApi(MethodView):
    """
    单位Api
    GET: 单位详情
    POST: 单位新增
    PUT: 单位编辑
    DELETE: 单位删除
    """

    def get(self, organs_id):
        """单位详情"""

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位不存在')

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_organs.to_json())

    def post(self):
        """单位新增"""

        data = request.get_json()
        organs_name = data.get('organs_name')
        example = data.get('example')
        ip_port = data.get('ip_port')
        remark = data.get('remark')

        query_organs = Organs.query.filter_by(organs_name=organs_name, is_deleted=0).first()
        if query_organs:
            return api_result(code=UNIQUE_ERROR, message=f'单位: {env_url} 已经存在')

        new_organs = Organs(
            organs_name=organs_name,
            example=example,
            ip_port=ip_port,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_organs.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    def put(self):
        """单位编辑"""

        data = request.get_json()
        organs_id = data.get('id')
        organs_name = data.get('organs_name')
        example = data.get('example')
        ip_port = data.get('ip_port')
        remark = data.get('remark')

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位地址不存在')

        if query_organs.organs_name != organs_name:
            if Organs.query.filter_by(organs_name=organs_name, is_deleted=0).all():
                return api_result(code=UNIQUE_ERROR, message=f'单位: {organs_name} 已经存在')

        query_organs.organs_name = organs_name
        query_organs.example = example
        query_organs.ip_port = ip_port
        query_organs.remark = remark
        query_organs.modifier = g.app_user.username
        query_organs.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """单位删除"""

        data = request.get_json()
        organs_id = data.get('id')

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位地址不存在')

        query_organs.modifier_id = g.app_user.id
        query_organs.modifier = g.app_user.username
        query_organs.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class OrgansPageApi(MethodView):
    """
    POST: 单位分页模糊查询
    """

    def post(self):
        """单位分页模糊查询"""

        data = request.get_json()
        organs_id = data.get('id')
        organs_name = data.get('organs_name')
        example = data.get('example')
        ip_port = data.get('ip_port')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        where_dict = {
            "id": organs_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id,
        }

        result_data = general_query(
            model=Organs,
            field_list=['organs_name', 'example', 'ip_port'],
            query_list=[organs_name, example, ip_port],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
