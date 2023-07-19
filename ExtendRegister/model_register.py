# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : model_register.py
# @Software: PyCharm


from app.models.admin.models import Admin
from app.models.test_project.models import TestProject
from app.models.test_env.models import TestEnv
from app.models.test_case_db.models import TestDatabases
from app.models.push_reminder.models import MailConfModel, DingDingConfModel, DingDingPushLogsModel
from app.models.organs.models import Organs