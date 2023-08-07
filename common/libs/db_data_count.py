# -*- coding: utf-8 -*-
# @Time    : 2023/7/28 16:05
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : db_data_count.py
# @Software: PyCharm

import time
import datetime
import subprocess
import telnetlib


class DBDataCount:
    """数据统计"""

    def __init__(self, db_example=None):
        self.db_example = db_example
        self.db_total_size = 0
        self.current_datetime = None
        self.db_server_start_time = None
        self.start_timestamp = None
        self.run_time = None
        self.user_list = []
        self.user_connections = []
        self.sql_list = []
        self.executing_sql = []

    def gen_db_total_size(self, table_schema="exiletestplatform"):
        """db磁盘占用"""

        total_size_sql = f"""
        SELECT 
            table_schema AS `Database`,
            round(SUM(data_length + index_length) / 1024 / 1024, 2) AS `TotalSize(MB)`
        FROM 
            information_schema.TABLES
        WHERE 
            table_schema = "{table_schema}";
        """

        query_db_total_size = self.db_example.select(total_size_sql, only=True)
        db_name = query_db_total_size.get('Database')
        self.db_total_size = query_db_total_size.get('TotalSize(MB)')
        return db_name, self.db_total_size

    def gen_db_start_time(self):
        """db启动时间"""

        query_db_uptime = self.db_example.select("SHOW GLOBAL STATUS LIKE 'Uptime';", only=True)
        db_uptime = int(query_db_uptime.get('Value', 0))
        current_timestamp = int(time.time())
        self.current_datetime = datetime.datetime.fromtimestamp(current_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        timestamp = current_timestamp - db_uptime
        self.db_server_start_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return self.db_server_start_time

    def gen_db_run_time(self):
        """db运行时长"""

        dt1 = datetime.datetime.strptime(self.current_datetime, '%Y-%m-%d %H:%M:%S')
        dt2 = datetime.datetime.strptime(self.db_server_start_time, '%Y-%m-%d %H:%M:%S')
        dt_result = dt1 - dt2
        days = dt_result.days
        hours, remainder = divmod(dt_result.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.run_time = f"{days}天 {hours}个小时 {minutes}分钟"
        return self.run_time

    def gen_user_connections_and_execute_sql(self):
        """db用户连接数以及执行中sql语句"""

        query_user_connections = self.db_example.select("SHOW PROCESSLIST;")
        self.user_list = list(filter(lambda obj: obj.get("Info") != 'SHOW PROCESSLIST', query_user_connections))
        self.user_connections = len(self.user_list)
        self.sql_list = [{"user": q.get('User'), "sql": q.get('Info')} for q in self.user_list if q.get('Info')]
        self.executing_sql = len(self.sql_list)
        return self.user_list, self.user_connections, self.sql_list, self.executing_sql


def ping_host(host):
    """ping ip"""

    try:
        # 使用subprocess.run来运行ping命令
        result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)

        # 检查返回值，通常，返回值为0表示成功，非0表示失败
        if result.returncode == 0:
            print(f"Ping to {host} was successful.")
            # print(result.stdout)  # 输出ping的结果
            return True, "OK"
        else:
            print(f"Ping to {host} failed.")
            # print(result.stderr)  # 输出错误信息
            return False, "FAIL"

    except subprocess.TimeoutExpired:
        print(f"Timeout while pinging {host}.")
        return False, "FAIL"


def telnet_host(host, port, timeout=3):
    """telnet ip port"""

    try:
        tn = telnetlib.Telnet(host, port=port, timeout=timeout)
        telnet = tn.read_some().decode("utf-8", errors='ignore')
        telnet_message = 'OK' if telnet else 'FAIL'
        return bool(telnet), telnet_message
    except BaseException as e:
        return False, 'FAIL'


if __name__ == '__main__':
    from common.libs.db import project_db

    dc = DBDataCount(db_example=project_db)

    # db磁盘占用
    db_name, db_total_size = dc.gen_db_total_size()
    print(db_name, db_total_size)
