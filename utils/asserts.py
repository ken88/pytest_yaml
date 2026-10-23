import logging
import allure
import jsonpath
import pytest

from utils.db import query_one


@allure.step("3.HTTP响应断言")
def http_assert(case,res_http):

    # 获取用例中的断言路径字典和期望值字典，如果没有配置则默认为空字典
    check_dict = case.get("check", {})
    expected_dict = case.get("expected", {})

    # 如果没写 check，用例失败
    if not check_dict:
        pytest.fail(f"用例格式错误: 用例ID={case.get('id')} 缺少 check 字段，无法执行断言！")

    # 遍历 check 字典中的每一个待断言字段
    for key, value in check_dict.items():
        # 1. 获取提取结果
        jsonpath_res = jsonpath.jsonpath(res_http.json(), value)
        actual_val = jsonpath_res[0] if jsonpath_res else None

        # 2. 获取期望值
        expected_val = expected_dict.get(key)

        logging.info(f'3.HTTP响应断言内容:实际结果({actual_val}) == 预期结果({expected_val})')
        # 3. 写断言
        assert actual_val == expected_val, f"断言失败: 字段[{key}] 期望={expected_val}, 实际={actual_val}"

def jdbc_assert(case):
    sql_check = case.get("sql_check")
    sql_expected = case.get("sql_expected")

    # 1.如果 YAML 里没写 sql_check，说明不需要查库，直接返回
    if not sql_check:
        return

    with allure.step("3.JDBC数据库断言"):
        # 2. 执行 SQL 查库
        res_db = query_one(sql_check)

        # 3.如果查不到数据，直接报错失败
        if not res_db:
            pytest.fail(f"数据库断言失败：未查询到数据 -> {sql_check}")

        logging.info(f'3.JDBC响应断言内容:实际结果({res_db})== 预期结果({sql_expected})')

        # 兼容单值比对和多字段字典比对
        if isinstance(sql_expected, dict):
            # 如果是字典（多字段验证），遍历比对
            for k, v in sql_expected.items():
                assert str(res_db.get(k)) == str(v), f"数据库断言失败: 字段[{k}] 期望={v}, 实际={res_db.get(k)}"
        else:
            # 如果是单值，把字典里的值抽出来比
            actual_val = list(res_db.values())[0] if res_db else None
            assert str(actual_val) == str(sql_expected), f"数据库断言失败: SQL[{sql_check}] 期望={sql_expected}, 实际={actual_val}"