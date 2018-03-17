# -*- coding: utf-8 -*-
#  sql 数据操作
#  2018.3.13
# 参考 https://github.com/Nooobita/ToolKit/blob/master/mysql_manager.py

import pymysql

# # 打开数据库连接
# db = pymysql.connect("127.0.0.1", "root", "fred123456", "house",use_unicode=True, charset="utf8")
#
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
#
# # SQL 插入语句
# sql = "INSERT INTO USER (name,phone,type , verify, company_name,company_addr) VALUES ('fred', '13808545254', 0, 0, '苹果公司','加利福尼亚')"
#
# try:
#     # 执行sql语句
#     cursor.execute(sql)
#     # 提交到数据库执行
#     db.commit()
# except  db.Error as e :
#     # 如果发生错误则回滚
#     print("Error %d: %s" % (e.args[0], e.args[1]))
#
#     db.rollback()
#
# # 关闭数据库连接
# db.close()


class MysqlManager(object):
    '''mysql管理器'''

    def __init__(self, db, user, passwd, host='127.0.0.1', port=3306, charset='utf8'):
        '''初始化数据库'''
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__port = port
        self.__charset = charset
        self.__connect = None
        self.__cursor = None

    def _connect_db(self):
        """
            dbManager._connect_db()
        连接数据库
        """
        params = {
            "db": self.__db,
            "user": self.__user,
            "passwd": self.__passwd,
            "host": self.__host,
            "port": self.__port,
            "charset": self.__charset,
            "cursorclass":pymysql.cursors.DictCursor # 设置结果显示成字典
        }
        self.__connect = pymysql.connect(**params)
        self.__cursor = self.__connect.cursor()

    def _close_db(self):
        '''
            dbManager._close_db()
        关闭数据库
        '''
        self.__cursor.close()
        self.__connect.close()

    def _deal_values(self, value):
        """
        self._deal_values(value) -> str or list
            处理传进来的参数

        """
        # 如果是字符串则加上''
        if isinstance(value, str):
            value = ("'{value}'".format(value=value))
        # 如果是字典则变成key=value形式
        elif isinstance(value, dict):
            result = []
            for key, value in value.items():
                value = self._deal_values(value)
                res = "{key}={value}".format(key=key, value=value)
                result.append(res)
            return result
        else:
            value = (str(value))
        return value

    def delete(self, table, condition):
        '''
            dbManager.delete(table, condition)
        删除数据库中的数据
        str -> table 字符串类型
        dict -> condition 字典类型
        '''
        self._connect_db()

        # 处理删除的条件
        condition_list = self._deal_values(condition)
        condition_data = ' and '.join(condition_list)

        # 构建sql语句
        sql = "delete from {table} where {condition}".format(table=table, condition=condition_data)

        self.__cursor.execute(sql)
        self.__connect.commit()
        self._close_db()

    def update(self, table, data, condition=None):
        """
            dbManager.update(table, data, [condition])
        更新数据
        str -> table 字符串类型
        dict -> data 字典类型
        dict -> condition 字典类型
        """
        self._connect_db()

        # 处理传入的数据
        update_list = self._deal_values(data)
        update_data = ",".join(update_list)
        # 判断是否有条件
        if condition is not None:
            # 处理传入的条件
            condition_list = self._deal_values(condition)
            condition_data = ' and '.join(condition_list)
            sql = "update {table} set {values} where {condition}".format(table=table, values=update_data,
                                                                         condition=condition_data)
        else:
            sql = "update {table} set {values}".format(table=table, values=update_data)

        print(sql)

        self.__cursor.execute(sql)
        self.__connect.commit()
        self._close_db()

    def exec_sql(self,sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        self._connect_db()
        self.__cursor.execute(sql)

        result = self._rows2array(self.__cursor.fetchall())

        self._close_db()

        return result

    def get(self, table, show_list, condition=None, get_one=False):
        """
            dbManager.get(table, show_list, [condition, get_one]) -> tupe
        获取数据 返回一个元祖
        str -> table 字符串类型
        list -> show_list 列表类型
        dict -> condition 字典类型
        boolean -> get_one 布尔类型

        """
        self._connect_db()

        # 处理显示的数据
        show_list = ",".join(show_list)
        print(show_list)
        sql = "select {key} from {table}".format(key=show_list, table=table)
        print(sql)
        # 处理传入的条件
        if condition:
            condition_list = self._deal_values(condition)
            condition_data = 'and'.join(condition_list)
            sql = "select {key} from {table} where{condition}".format(key=show_list, table=table,
                                                                      condition=condition_data)

        self.__cursor.execute(sql)

        # 返回一条数据还是所有数据
        if get_one:
            result = self.__cursor.fetchone()
        else:
            result = self._rows2array(self.__cursor.fetchall())
        self._close_db()
        return result

    def _rows2array(self, data):
        '''transfer tuple to array.'''
        result = []
        for da in data:
            if type(da) is not dict:
               raise Exception('Format Error: data is not a dict.')
            result.append(da)
        return result

    def insert(self, table, insert_data):
        '''
            dbManager.insert(table, insert_data)
        添加数据到数据库
        str -> table 为字符串
        [{},{}] -> 为列表中嵌套字典类型
        '''
        # 用户传入数据字典列表数据，根据key, value添加进数据库
        # 连接数据库
        self._connect_db()

        try:
            for data in insert_data:
                # 提取插入的字段
                key = ','.join(data.keys())
                # 提取插入的值
                values = map(self._deal_values, data.values())
                insert_data = ', '.join(values)
                # 构建sql语句
                sql = "insert into {table}({key}) values ({val})".format(table=table, key=key, val=insert_data)
                print(sql)
                self.__cursor.execute(sql)
                self.__connect.commit()
        except Exception as error:
            print(error)
        finally:
            self._close_db()

dbManager = MysqlManager("house", 'root', 'fred123456')
if __name__ == '__main__':

    insert_data = [{
       "name": 'fred',
        "phone": '13808545254',
        "verify": 0,
        "company_name":'苹果公司',
        "company_addr":'加利福尼亚'

    }]
    #dbManager.insert('user',insert_data=insert_data)
    a = dbManager.get(table="user",show_list = ['*'])
    print(a)