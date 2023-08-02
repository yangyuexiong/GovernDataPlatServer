# -*- coding: utf-8 -*-
# @Time    : 2023/7/31 22:00
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ping_and_telnet.py
# @Software: PyCharm


import os, sys
import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='Asia/Shanghai')

from common.libs.db import MyPyMysql, MYSQL_CONF
from common.libs.db_data_count import ping_host, telnet_host
from common.libs.data_dict import F

project_db = MyPyMysql(**MYSQL_CONF, debug=False)

d = {}


# minutes 分
# seconds 秒
@sched.scheduled_job('interval', start_date='2023-1-1', end_date='2033-1-1', seconds=5)
def interval_task1():
    """ping and telnet"""

    sql = f"""SELECT A.id, organs_name, db_connection FROM zw_organs AS A INNER JOIN zw_test_databases AS B ON A.db_id=B.id;"""
    result = project_db.select(sql)

    for res in result:
        organs_id = res.get("id")
        organs_name = res.get("organs_name")
        db_connection = res.get("db_connection")
        host = db_connection.get('host')
        port = db_connection.get('port')
        print(organs_id, organs_name, host, port)
        if not db_connection:
            continue

        ping_bool, ping_message = ping_host(host=host)
        telnet_bool, telnet_message = telnet_host(host=host, port=port, timeout=5)

        print(ping_bool, ping_message)
        print(telnet_bool, telnet_message)

        if not ping_bool or not telnet_bool:
            create_alarm = f"""
                INSERT INTO `GovernData`.`zw_alarm` (`organs_id`, `organs_name`, `ip`, `port`, `ping`, `telnet`, `create_time`, `create_timestamp`, `status`)
		        VALUES('{organs_id}', '{organs_name}', '{host}', '{port}', '{ping_message}', '{telnet_message}', '{F.gen_datetime()}', '{int(time.time())}', '0');"""

            project_db.insert(create_alarm)


if __name__ == '__main__':
    print('ping and telnet start...')
    print(datetime.now())
    sched.start()
