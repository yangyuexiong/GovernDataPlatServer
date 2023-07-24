# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:02 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class Organs(BaseModel):
    __tablename__ = 'zw_organs'
    __table_args__ = {'comment': '单位'}

    organs_name = db.Column(db.String(255), nullable=False, comment='单位名称')
    example = db.Column(db.String(255), nullable=True, comment='实例')
    ip_port = db.Column(db.String(255), nullable=True, comment='ip+端口')
    ip = db.Column(db.String(255), nullable=True, comment='ip')
    port = db.Column(db.Integer, nullable=True, comment='端口')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'Organs 模型对象-> ID:{} 单位名称:{} 实例:{} ip:{} 端口:{}'.format(
            self.id, self.organs_name, self.example, self.ip, self.port
        )
