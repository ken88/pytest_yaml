import pymysql
from pymysql.cursors import DictCursor

from config.config import USER, HOST, PORT, PASSWORD, DATABASE,CHARSET


def get_db_conn():

    # 数据库信息
    conn = pymysql.connect(
        host = HOST,
        port = PORT,
        user = USER,
        password = PASSWORD,
        database = DATABASE,
        charset = CHARSET
    )
    return conn

# 查询单条（用来校验新增/编辑后的数据）
def query_one(sql, args=None):
    conn = get_db_conn()
    cursor = conn.cursor(DictCursor) # 返回字典，方便直接取字段
    try:
        cursor.execute(sql, args or [])
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 查询多条
def query_all(sql, args=None):
    conn = get_db_conn()
    cursor = conn.cursor(DictCursor)
    try:
        cursor.execute(sql, args or [])
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 执行增删改（insert/update/delete）
def execute_sql(sql, args=None):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        conn.commit() # 提交事务
        return cursor.rowcount # 返回影响行数
    except Exception as e:
        conn.rollback() # 出错回滚
        raise e
    finally:
        cursor.close()
        conn.close()