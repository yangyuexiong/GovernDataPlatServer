# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 2:12 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

from .demo_api.demo_api import TestApi, TestCeleryAsyncTaskApi
from .index_api.index_api import IndexApi
from .dashboard_api.dashboard_api import DashboardApi
from .auth_api.auth_api import AuthApi
from .login_api.login_api import LoginApi
from .user_api.user_api import TouristApi, UserApi, UserPasswordApi, UserPageApi, UserProfileApi
from .case_env_api.case_env_api import CaseEnvApi, CaseEnvPageApi
from .case_db_api.case_db_api import CaseDBApi, CaseDBPageApi, CaseDBPingApi
from .mail_api.mail_api import MailApi, MailPageApi
from .dingding_api.dingding_api import DingDingPushConfApi, DingDingPushConfPageApi
from .project_api.project_api import ProjectApi, ProjectPageApi

api = Blueprint('api', __name__)
crm = Blueprint('crm', __name__)

api.add_url_rule('/test', view_func=TestApi.as_view('test_api'))
api.add_url_rule('/test_celery', view_func=TestCeleryAsyncTaskApi.as_view('test_celery'))

api.add_url_rule('/index', view_func=IndexApi.as_view('index_api'))
api.add_url_rule('/index/<version_id>', view_func=IndexApi.as_view('index_version_api'))

api.add_url_rule('/dashboard', view_func=DashboardApi.as_view('dashboard_api'))

api.add_url_rule('/auth', view_func=AuthApi.as_view('auth_api'))
api.add_url_rule('/login', view_func=LoginApi.as_view('login_api'))
api.add_url_rule('/tourist', view_func=TouristApi.as_view('tourist_api'))

api.add_url_rule('/user', view_func=UserApi.as_view('user_api'))
api.add_url_rule('/user/<user_id>', view_func=UserApi.as_view('user_detail'))
api.add_url_rule('/user_pwd', view_func=UserPasswordApi.as_view('user_pwd'))
api.add_url_rule('/user_profile', view_func=UserProfileApi.as_view('user_profile'))
api.add_url_rule('/user_profile/<user_id>', view_func=UserProfileApi.as_view('user_profile_detail'))
api.add_url_rule('/user_page', view_func=UserPageApi.as_view('user_page'))

api.add_url_rule('/case_env', view_func=CaseEnvApi.as_view('case_env'))
api.add_url_rule('/case_env/<env_id>', view_func=CaseEnvApi.as_view('case_env_detail'))
api.add_url_rule('/case_env_page', view_func=CaseEnvPageApi.as_view('case_env_page'))

api.add_url_rule('/case_db', view_func=CaseDBApi.as_view('case_db'))
api.add_url_rule('/case_db/<db_id>', view_func=CaseDBApi.as_view('case_db_detail'))
api.add_url_rule('/case_db_page', view_func=CaseDBPageApi.as_view('case_db_page'))
api.add_url_rule('/case_db_ping/<db_id>', view_func=CaseDBPingApi.as_view('case_db_ping'))

api.add_url_rule('/mail_conf', view_func=MailApi.as_view('mail_conf'))
api.add_url_rule('/mail_conf_page', view_func=MailPageApi.as_view('mail_conf_page'))

api.add_url_rule('/dd_push_conf', view_func=DingDingPushConfApi.as_view('dd_push_conf'))
api.add_url_rule('/dd_push_conf_page', view_func=DingDingPushConfPageApi.as_view('dd_push_conf_page'))

api.add_url_rule('/project', view_func=ProjectApi.as_view('project'))
api.add_url_rule('/project/<project_id>', view_func=ProjectApi.as_view('project_detail'))
api.add_url_rule('/project_page', view_func=ProjectPageApi.as_view('project_page'))
