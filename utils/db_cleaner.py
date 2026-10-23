import yaml
import logging

from config.config import YAML_FILE
from utils.db import execute_sql


def run_cleanup():
    # 统一执行清理 SQL
    # 1. 读取配置
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sql_list = config.get("cleanup_sql", [])

    # 2. 循环执行
    for sql in sql_list:
        try:
            execute_sql(sql)
        except Exception as e:
            logging.error(f"清理数据失败，SQL: {sql}, 错误: {e}")