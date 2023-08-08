# -*- coding: utf-8 -*-
# @Time    : 2023/8/8 17:16
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : clear_logs.py
# @Software: PyCharm


import os, sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone='Asia/Shanghai')


def clear_file_content():
    file_path = '/Users/yangyuexiong/Desktop/xcv123.txt'
    with open(file_path, 'w') as file:
        file.truncate(0)
    print(f"文件 {file_path} 内容已清空")


# 使用 cron 调度方式，每天晚上 12 点 15 分 30 秒执行任务
@sched.scheduled_job('cron', hour=18, minute=7, second=10)
def clear_logs_job():
    """清除日志"""

    clear_file_content()


if __name__ == '__main__':
    print('clear logs start...')
    print(datetime.now())
    sched.start()
