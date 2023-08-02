# -*- coding: utf-8 -*-
# @Time    : 2023/7/31 20:22
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : alarm_api.py
# @Software: PyCharm


from all_reference import *
from app.models.alarm.models import Alarm


class AlarmLogsApi(MethodView):
    """
    告警Api
    POST: 获取告警
    """

    def post(self):
        """获取告警"""

        data = request.get_json()
        page = data.get('page')
        size = data.get('size')

        current_user = g.app_user.username
        current_user_id = g.app_user.id

        where_dict = {
            "status": 0
        }

        if current_user != 'admin':
            where_dict['creator_id'] = current_user_id

        result_data = general_query(
            model=Alarm,
            where_dict=where_dict,
            in_field_list=[],
            in_value_list=[],
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
