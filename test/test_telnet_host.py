# -*- coding: utf-8 -*-
# @Time    : 2023/8/7 13:50
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_telnet_host.py
# @Software: PyCharm

from common.libs.db_data_count import DBDataCount, ping_host, telnet_host

if __name__ == '__main__':
    telnet, telnet_message = telnet_host('10.192.67.32', 3307, 10)
    print(telnet, telnet_message)