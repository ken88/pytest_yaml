import pymysql
from pymysql.cursors import DictCursor

from config.config import USER, HOST, PORT, PASSWORD, DATABASE,CHARSET


def get_db_conn():

    # 数据库信息，改成你本地的
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
def query_one(sql, args=None,index=0):
    conn = get_db_conn()
    cursor = conn.cursor()
    # cursor = conn.cursor(DictCursor) # 返回字典，方便直接取字段
    cursor.execute(sql, args or [])
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[index]

# 查询多条
def query_all(sql, args=None):
    conn = get_db_conn()
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql, args or [])
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

# 执行增删改（insert/update/delete）
def execute_sql(sql, args=None):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args or [])
        conn.commit() # 提交事务
        return cursor.rowcount # 返回影响行数
    except Exception as e:
        conn.rollback() # 出错回滚
        raise e
    finally:
        cursor.close()
        conn.close()