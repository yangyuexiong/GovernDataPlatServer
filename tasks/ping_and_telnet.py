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
@sched.scheduled_job('interval', start_date='2023-1-1', end_date='2033-1-1', seconds=8)
def interval_task1():
    """ping and telnet"""

    sql = f"""SELECT A.id, organs_name, db_connection FROM zw_organs AS A INNER JOIN zw_test_databases AS B ON A.db_id=B.id WHERE A.is_deleted=0;"""
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
            ping_fail = 1 if not ping_bool else 0
            telnet_fail = 1 if not telnet_bool else 0

            query_alarm = f"""SELECT * FROM `GovernData`.`zw_alarm` WHERE ip='{host}' and status=0;"""
            alarm_result = project_db.select(query_alarm, only=True)
            if alarm_result:
                current_pf = alarm_result.get('ping_fail', 0)
                current_tf = alarm_result.get('telnet_fail', 0)
                alarm_id = alarm_result.get('id', 0)
                update_alarm = f"""UPDATE `GovernData`.`zw_alarm` SET `ping_fail` = {current_pf + ping_fail}, `telnet_fail` = {current_tf + telnet_fail} WHERE `id` = {alarm_id};"""
                project_db.update(update_alarm)
            else:
                create_alarm = f"""
                    INSERT INTO `GovernData`.`zw_alarm` (`organs_id`, `organs_name`, `ip`, `port`, `ping`, `telnet`, `create_time`, `create_timestamp`, `status`, `ping_fail`, `telnet_fail`)
                    VALUES('{organs_id}', '{organs_name}', '{host}', '{port}', '{ping_message}', '{telnet_message}', '{F.gen_datetime()}', '{int(time.time())}', '0', {ping_fail}, {telnet_fail});"""

                project_db.insert(create_alarm)

            d[host] = True

        else:
            if d.get(host):
                update_alarm = f"""UPDATE `GovernData`.`zw_alarm` SET `status` = 1 WHERE `ip` = '{host}';"""
                project_db.update(update_alarm)
                del d[host]

    print(d)


if __name__ == '__main__':
    print('ping and telnet start...')
    print(datetime.now())
    sched.start()
