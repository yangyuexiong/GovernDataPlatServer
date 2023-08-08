# -*- coding: utf-8 -*-
# @Time    : 2023/7/19 11:31
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : organs_api.py
# @Software: PyCharm

from all_reference import *
from app.models.organs.models import Organs
from app.models.alarm.models import Alarm


class OrgansApi(MethodView):
    """
    单位Api
    GET: 单位详情
    POST: 单位新增
    PUT: 单位编辑
    DELETE: 单位删除
    """

    def get(self, organs_id):
        """单位详情"""

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位不存在')

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_organs.to_json())

    def post(self):
        """单位新增"""

        data = request.get_json()
        organs_name = data.get('organs_name')
        example = data.get('example')
        db_id = data.get('db_id')
        remark = data.get('remark')

        # query_organs = Organs.query.filter_by(organs_name=organs_name, is_deleted=0).first()
        # if query_organs:
        #     return api_result(code=UNIQUE_ERROR, message=f'单位: {organs_name} 已经存在')

        new_organs = Organs(
            organs_name=organs_name,
            example=example,
            db_id=db_id,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_organs.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    def put(self):
        """单位编辑"""

        data = request.get_json()
        organs_id = data.get('id')
        organs_name = data.get('organs_name')
        example = data.get('example')
        db_id = data.get('db_id')
        remark = data.get('remark')

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位地址不存在')

        # if query_organs.organs_name != organs_name:
        #     if Organs.query.filter_by(organs_name=organs_name, is_deleted=0).all():
        #         return api_result(code=UNIQUE_ERROR, message=f'单位: {organs_name} 已经存在')

        query_organs.organs_name = organs_name
        query_organs.example = example
        query_organs.db_id = db_id
        query_organs.remark = remark
        query_organs.modifier = g.app_user.username
        query_organs.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """单位删除"""

        data = request.get_json()
        organs_id = data.get('id')

        query_organs = Organs.query.get(organs_id)
        if not query_organs:
            return api_result(code=NO_DATA, message='单位地址不存在')

        query_organs.modifier_id = g.app_user.id
        query_organs.modifier = g.app_user.username
        query_organs.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class OrgansPageApi(MethodView):
    """
    POST: 单位分页模糊查询
    """

    def post(self):
        """单位分页模糊查询"""

        data = request.get_json()
        organs_id = data.get('id')
        organs_name = data.get('organs_name')
        db_name = data.get('db_name')
        db_id = data.get('db_id')
        ip = data.get('ip')
        port = data.get('port')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')
        limit = page_size(page=page, size=size)

        current_user = g.app_user.username
        current_user_id = g.app_user.id

        sql = f"""
        SELECT
            *
        FROM
            zw_organs AS A
            INNER JOIN zw_test_databases AS B ON A.db_id = B.id
        WHERE
            A.is_deleted = 0
            {f'AND A.creator_id={current_user_id}' if current_user != 'admin' else ''}
            {f'AND db_id={db_id}' if db_id else ''}
            {f'AND A.creator_id={creator_id}' if creator_id else ''}
            {f'AND organs_name LIKE "%{organs_name}%"' if organs_name else ''}
            {f'AND db_name LIKE "%{db_name}%"' if db_name else ''}
            {f'AND db_connection LIKE "%{ip}%"' if ip else ''}
        LIMIT {limit[0]},{limit[1]}
            ;
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            zw_organs AS A
            INNER JOIN zw_test_databases AS B ON A.db_id = B.id
        WHERE
            A.is_deleted = 0
            {f'AND A.creator_id={current_user_id}' if current_user != 'admin' else ''}
            {f'AND db_id={db_id}' if db_id else ''}
            {f'AND A.creator_id={creator_id}' if creator_id else ''}
            {f'AND organs_name LIKE "%{organs_name}%"' if organs_name else ''}
            {f'AND db_name LIKE "%{db_name}%"' if db_name else ''}
            {f'AND db_connection LIKE "%{ip}%"' if ip else ''}
            ;
        """

        result_list = project_db.select(sql)
        result_count = project_db.select(sql_count)

        result_data = {
            'records': result_list if result_list else [],
            'now_page': page,
            'total': result_count[0].get('COUNT(*)')
        }

        for res in result_data.get('records'):
            db_connection = res.get('db_connection')
            # db_example = MyPyMysql(**db_connection, debug=False)
            # db_dc = DBDataCount(db_example=db_example)
            # try:
            #     db_dc.gen_db_start_time()
            #     db_dc.gen_db_run_time()
            #     run_time = db_dc.run_time
            # except:
            #     run_time = '未启动'
            host = db_connection.get('host')
            port = db_connection.get('port')

            telnet, telnet_message = telnet_host(host, port, 10)

            res['ip'] = host
            res['port'] = port
            res['telnet'] = telnet_message
            # try:
            #     db_example.ping()
            #     ping = 'OK'
            # except:
            #     ping = 'FALSE'
            ping, ping_message = ping_host(host=host)
            res['ping'] = ping_message
            # res['run_time'] = run_time

            if not ping or not telnet:
                query_alarm = Alarm.query.filter_by(ip=host, status=0).first()
                if not query_alarm:
                    status = 0
                    organs_id = res.get("id")
                    organs_name = res.get("organs_name")
                    new_alarm = Alarm(
                        organs_id=organs_id, organs_name=organs_name, ip=host, port=port, ping=ping_message,
                        telnet=telnet_message, status=status, ping_fail=0, telnet_fail=0
                    )
                    new_alarm.save()
                else:
                    query_alarm.add_ping_fail(ping)
                    query_alarm.add_telnet_fail(telnet)
                    db.session.commit()

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
