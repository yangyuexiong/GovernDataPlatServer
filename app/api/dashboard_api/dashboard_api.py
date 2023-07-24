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

        total_size_sql = """
        SELECT 
            table_schema AS `Database`,
            round(SUM(data_length + index_length) / 1024 / 1024, 2) AS `TotalSize(MB)`
        FROM 
            information_schema.TABLES
        WHERE 
            table_schema = 'exiletestplatform';
        """
        query_db_total_size = project_db.select(total_size_sql, only=True)
        db_name = query_db_total_size.get('Database')
        db_total_size = query_db_total_size.get('TotalSize(MB)')

        # 启动时间
        query_db_uptime = project_db.select("SHOW GLOBAL STATUS LIKE 'Uptime';", only=True)
        db_uptime = int(query_db_uptime.get('Value', 0))
        current_timestamp = int(time.time())
        current_datetime = datetime.datetime.fromtimestamp(current_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        timestamp = current_timestamp - db_uptime
        db_server_start_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # 运行时长
        dt1 = datetime.datetime.strptime(current_datetime, '%Y-%m-%d %H:%M:%S')
        dt2 = datetime.datetime.strptime(db_server_start_time, '%Y-%m-%d %H:%M:%S')
        dt_result = dt1 - dt2
        days = dt_result.days
        hours, remainder = divmod(dt_result.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        run_time = f"{days}天 {hours}个小时 {minutes}分钟"

        # 用户连接数，执行中语句数
        query_user_connections = project_db.select("SHOW PROCESSLIST;")
        user_list = list(filter(lambda obj: obj.get("Info") != 'SHOW PROCESSLIST', query_user_connections))
        user_connections = len(user_list)
        sql_list = [{"user": q.get('User'), "sql": q.get('Info')} for q in user_list if q.get('Info')]
        executing_sql = len(sql_list)
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
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=data)
