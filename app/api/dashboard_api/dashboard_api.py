# -*- coding: utf-8 -*-
# @Time    : 2022/9/21 16:29
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : dashboard_api.py
# @Software: PyCharm

import psutil

from all_reference import *


class DashboardApi(MethodView):
    """
    仪表盘 Api
    """

    def post(self):
        """仪表盘数据"""

        data = request.get_json()

        """
        dc = DBDataCount(db_example=project_db)

        # db磁盘占用
        db_name, db_total_size = dc.gen_db_total_size()

        # 启动时间
        db_server_start_time = dc.gen_db_start_time()

        # 运行时长
        run_time = dc.gen_db_run_time()

        # 用户连接数，执行中语句数
        user_list, user_connections, sql_list, executing_sql = dc.gen_user_connections_and_execute_sql()

        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        data = {
            "db_name": db_name,
            "db_server_start_time": db_server_start_time,
            "run_time": run_time,
            "db_total_size": f"{db_total_size} MB",
            "user_connections": user_connections,
            "executing_sql": executing_sql,
            "user_list": user_list,
            "sql_list": sql_list,
            "cup_use": f"{cpu_usage}%",
            "memory_use": f"{memory_usage}%"
        }
        """

        query_user_organs = """
        SELECT
            B.id
        FROM
            zw_auth_admin AS A
            INNER JOIN zw_organs AS B ON A.id = B.creator_id;
        """
        user_organs_ids = project_db.select(query_user_organs)
        ids = tuple([obj.get('id') for obj in user_organs_ids])

        if not ids:
            data = {
                "telnet_success": 0,
                "telnet_fail": 0,
                "ping_success": 0,
                "ping_fail": 0
            }
            return data

        if len(ids) > 1:
            sql = f"""SELECT * FROM zw_alarm WHERE status = 0 and organs_id in {ids};"""
        else:
            sql = f"""SELECT * FROM zw_alarm WHERE status = 0 and organs_id = {ids[0]};"""

        result = project_db.select(sql)

        telnet_success = 0
        telnet_fail = 0
        ping_success = 0
        ping_fail = 0

        for res in result:
            ping = res.get('ping')
            telnet = res.get('telnet')
            pf = res.get('ping_fail', 0)
            tf = res.get('telnet_fail', 0)

            ping_fail += pf
            telnet_fail += tf

            # if telnet == "OK":
            #     telnet_success += 1
            # else:
            #     telnet_fail += 1
            #
            # if ping == "OK":
            #     ping_success += 1
            # else:
            #     ping_fail += 1

        data = {
            "telnet_success": telnet_success,
            "telnet_fail": telnet_fail,
            "ping_success": ping_success,
            "ping_fail": ping_fail
        }
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=data)
