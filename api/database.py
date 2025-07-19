import pymysql
import pymysql.cursors

connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='house',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
# 创建连接

def data_select():
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            sql = "SELECT name , password FROM user_info"
            cursor.execute(sql)

            # 获取查询结果
            result = cursor.fetchall()

            #打印结果
            print(result)
            return result

        #关闭连接
        connection.close()


def add_data(name, password, email):
    try:
        # 创建游标对象
        with connection.cursor() as cursor:

            # 插入数据
            sql = "INSERT INTO user_info (name , password, email)VALUES(%s , %s , %s)"
            rows = cursor.execute(sql, (name, password, email))
            print(rows)

            # 提交事务
            connection.commit()
            return rows

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        connection.rollback() # 如果出错则回滚
        return 0