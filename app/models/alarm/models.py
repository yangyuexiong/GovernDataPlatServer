# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:02 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class Alarm(BaseModel):
    __tablename__ = 'zw_alarm'
    __table_args__ = {'comment': '告警日志'}

    organs_id = db.Column(BIGINT(20, unsigned=True), comment='单位id')
    organs_name = db.Column(db.String(255), nullable=False, comment='单位名称')
    ip = db.Column(db.String(32), comment='ip')
    port = db.Column(db.String(32), comment='port')
    ping = db.Column(db.String(32), comment='ping')
    telnet = db.Column(db.String(32), comment='telnet')
    ping_fail = db.Column(BIGINT(20, unsigned=True), comment='ping失败次数')
    telnet_fail = db.Column(BIGINT(20, unsigned=True), comment='telnet失败次数')

    def add_ping_fail(self, flag):
        """增加ping错误数"""

        if not flag:
            self.ping_fail = self.ping_fail + 1

    def add_telnet_fail(self, flag):
        """增加telnet错误数"""

        if not flag:
            self.telnet_fail = self.telnet_fail + 1

    def __repr__(self):
        return 'Alarm 模型对象-> 单位名称:{}'.format(self.organs_name)
