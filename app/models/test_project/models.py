# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 9:49 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestProject(BaseModel):
    __tablename__ = 'zw_test_project'
    __table_args__ = {'comment': '项目表'}

    project_name = db.Column(db.String(128), nullable=False, unique=True, comment='项目名称')
    project_auth = db.Column(db.JSON, default=0, comment='是否公开:1-是;0-否')
    project_user = db.Column(db.JSON, default=[], comment='项目用户:project_auth为是的情况下使用')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestProject 模型对象-> ID:{} 项目名称:{}'.format(self.id, self.project_name)
