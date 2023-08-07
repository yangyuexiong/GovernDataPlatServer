# -*- coding: utf-8 -*-
# @Time    : 2023/7/31 21:37
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : alarm_dd_push.py
# @Software: PyCharm


import os, sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='Asia/Shanghai')

from common.libs.db import MyPyMysql, MYSQL_CONF
from common.libs.db_data_count import ping_host, telnet_host
from common.tools.message_push import MessagePush
from common.libs.data_dict import F

project_db = MyPyMysql(**MYSQL_CONF, debug=False)

is_push = {}


# minutes 分
# seconds 秒
@sched.scheduled_job('interval', start_date='2023-1-1', end_date='2033-1-1', seconds=8)
def interval_task1():
    """dd push"""

    sql = f"""SELECT * FROM zw_alarm WHERE status = 0;"""
    result = project_db.select(sql)

    for res in result:
        alarm_id = res.get('id')
        host = res.get('ip')
        port = res.get('port')
        ping_bool, ping_message = ping_host(host=host)
        telnet_bool, telnet_message = telnet_host(host=host, port=port, timeout=5)

        query_push = is_push.get(alarm_id)
        if query_push:
            print(f'已经推送过...{query_push}')
            continue

        if not ping_bool or not telnet_bool:
            sql = f"""SELECT * FROM zw_ding_ding_conf WHERE id=1;"""
            query_dd_conf = project_db.select(sql, only=True)
            ding_talk_url = query_dd_conf.get('ding_talk_url')
            first_text = f"#### 告警:{F.gen_datetime()} \n  >"
            ping_text = f"Ping:{ping_message}  \n  >"
            telnet_text = f"Telnet:{telnet_message}  \n"
            markdown_text = f"{first_text}{ping_text if not ping_bool else ''}{telnet_text if not telnet_bool else ''}"
            MessagePush.ding_ding_push(
                ding_talk_url=ding_talk_url,
                markdown_text=markdown_text
            )
            is_push[alarm_id] = True


if __name__ == '__main__':
    print('check log push start...')
    print(datetime.now())
    sched.start()
