# -*- coding: utf-8 -*-
# @Time    : 2022/9/21 16:29
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : dashboard_api.py
# @Software: PyCharm


from all_reference import *


class DashboardApi(MethodView):
    """
    仪表盘 Api
    """

    def post(self):
        """仪表盘数据"""

        data = request.get_json()
        data = {
            "user_connections": 3,
            "executing_sql": 10,
            "cup_use": 70,
            "memory_use": 57,
        }
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=data)
